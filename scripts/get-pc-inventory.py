#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get-pc-inventory.py

Script semplice per estrarre un inventario base da Nutanix Prism Central (v4 API)
- Clusters
- VMs (con nome, cluster, power_state, categories, IPs se disponibili)
- Categorie associate (opzionale)

Output:
- inventory.json
- inventory.yml  (formato compatibile Ansible)

Utilizzo:
  export PC_HOST="10.38.10.50"
  export PC_USER="admin"
  export PC_PASS="yourpassword"

  python3 get-pc-inventory.py [--categories] [--output-dir ./]

Requisiti:
  - Python 3.8+
  - requests
  - pyyaml (pip install requests pyyaml)

Avvertenze:
  - Usa --insecure solo in lab (disabilita verifica SSL)
  - Non committare credenziali in chiaro!
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime
from typing import Dict, List, Optional

import requests
import yaml
from requests.auth import HTTPBasicAuth

# ────────────────────────────────────────────────
# Configurazione di default
# ────────────────────────────────────────────────

DEFAULT_PC_PORT = 9440
DEFAULT_TIMEOUT = 30
DEFAULT_PAGE_SIZE = 500  # max per pagina API v4

# Ignora warning SSL in ambiente lab
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_api_client(
    host: str,
    user: str,
    password: str,
    port: int = DEFAULT_PC_PORT,
    insecure: bool = False,
) -> Dict:
    """Restituisce un client requests preconfigurato"""
    base_url = f"https://{host}:{port}/api/nutanix/v4"
    auth = HTTPBasicAuth(user, password)
    session = requests.Session()
    session.auth = auth
    session.verify = not insecure
    session.headers.update({"Accept": "application/json"})
    return {"session": session, "base_url": base_url}


def api_get(client: Dict, endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Esegue GET con paginazione automatica"""
    url = f"{client['base_url']}/{endpoint.lstrip('/')}"
    all_results = []
    next_offset = 0

    while True:
        p = params.copy() if params else {}
        p["offset"] = next_offset
        p["length"] = DEFAULT_PAGE_SIZE

        resp = client["session"].get(url, params=p, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        entities = data.get("entities", data.get("data", []))
        all_results.extend(entities)

        if len(entities) < DEFAULT_PAGE_SIZE:
            break

        next_offset += DEFAULT_PAGE_SIZE

    return {"entities": all_results, "metadata": data.get("metadata", {})}


def get_clusters(client: Dict) -> List[Dict]:
    """Recupera tutti i cluster registrati in PC"""
    data = api_get(client, "clusters")
    clusters = []
    for c in data["entities"]:
        clusters.append(
            {
                "name": c.get("name", "Unknown"),
                "ext_id": c.get("extId"),
                "uuid": c.get("extId"),  # spesso coincide
                "status": c.get("status", {}).get("state", "UNKNOWN"),
                "hypervisor": c.get("hypervisor", {}).get("type"),
                "nodes_count": len(c.get("nodes", [])),
            }
        )
    return clusters


def get_vms(client: Dict) -> List[Dict]:
    """Recupera tutte le VM gestite da PC (AHV)"""
    data = api_get(client, "vms")
    vms = []
    for vm in data["entities"]:
        power_state = vm.get("status", {}).get("power_state", "OFF")
        ips = []
        for nic in vm.get("status", {}).get("resources", {}).get("nic_list", []):
            for ip in nic.get("ip_endpoint_list", []):
                if ip.get("ip"):
                    ips.append(ip["ip"])

        categories = []
        for cat in vm.get("categories", []):
            categories.append(f"{cat.get('key')}:{cat.get('value')}")

        vms.append(
            {
                "name": vm.get("name", "Unnamed"),
                "ext_id": vm.get("extId"),
                "cluster_ext_id": vm.get("cluster", {}).get("extId"),
                "power_state": power_state,
                "ip_addresses": ips,
                "categories": categories,
                "memory_mb": vm.get("memory_size_bytes", 0) // (1024**2),
                "vcpus": vm.get("num_cores_per_socket", 0) * vm.get("num_sockets", 1),
            }
        )
    return vms


def get_categories(client: Dict) -> List[Dict]:
    """Recupera tutte le categorie definite (key + values)"""
    data = api_get(client, "categories")
    cats = []
    for c in data["entities"]:
        key = c.get("key")
        for val in c.get("values", []):
            cats.append(
                {
                    "key": key,
                    "value": val.get("value"),
                    "description": val.get("description", ""),
                    "ext_id": val.get("extId"),
                }
            )
    return cats


def save_output(data: Dict, output_dir: str = "."):
    """Salva in JSON e YAML"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"pc-inventory_{timestamp}"

    json_path = os.path.join(output_dir, f"{base_name}.json")
    yaml_path = os.path.join(output_dir, f"{base_name}.yml")

    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Salvato JSON: {json_path}")

    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Salvato YAML: {yaml_path}")


def main():
    parser = argparse.ArgumentParser(description="Estrae inventario da Nutanix Prism Central")
    parser.add_argument("--host", help="Prism Central IP/FQDN", default=os.getenv("PC_HOST"))
    parser.add_argument("--user", help="Username", default=os.getenv("PC_USER"))
    parser.add_argument("--pass", dest="password", help="Password", default=os.getenv("PC_PASS"))
    parser.add_argument("--port", type=int, default=DEFAULT_PC_PORT)
    parser.add_argument("--insecure", action="store_true", help="Disabilita verifica SSL")
    parser.add_argument("--categories", action="store_true", help="Includi anche lista categorie")
    parser.add_argument("--output-dir", default=".", help="Directory di output")

    args = parser.parse_args()

    if not all([args.host, args.user, args.password]):
        parser.error("Specifica --host, --user, --pass oppure setta variabili PC_HOST, PC_USER, PC_PASS")

    print(f"Connessione a Prism Central: {args.host}:{args.port}")
    print("Attenzione: " + ("SSL NON verificato" if args.insecure else "SSL verificato"))

    client = get_api_client(args.host, args.user, args.password, args.port, args.insecure)

    inventory = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "clusters": get_clusters(client),
        "vms": get_vms(client),
    }

    if args.categories:
        inventory["categories"] = get_categories(client)

    print(f"Trovati {len(inventory['clusters'])} cluster")
    print(f"Trovati {len(inventory['vms'])} VM")

    save_output(inventory, args.output_dir)


if __name__ == "__main__":
    main()
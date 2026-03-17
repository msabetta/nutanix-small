# create_nutanix_project.py
import os
import re

# ────────────────────────────────────────────────
#   Struttura ad albero (copia-incolla qui sotto)
# ────────────────────────────────────────────────

TREE = """
nutanix-small-project/
├── README.md
├── .gitignore
│
├── terraform/
│   ├── provider.tf
│   ├── variables.tf
│   ├── terraform.tfvars.example
│   ├── main.tf
│   ├── outputs.tf
│   └── modules/
│       └── vm_simple/
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
│
├── ansible/
│   ├── ansible.cfg
│   ├── inventory.yml
│   ├── group_vars/
│   │   └── all.yml
│   ├── vault/
│   │   └── secrets.yml       # .gitignore questo!
│   └── playbooks/
│       ├── 00_create_categories.yml
│       ├── 10_tag_vms.yml
│       └── 20_configure_vms.yml
│
├── docs/
│   └── quick-start.md
│
└── scripts/
    └── get-pc-inventory.py
""".strip()

# ────────────────────────────────────────────────
#   Configurazione
# ────────────────────────────────────────────────

ROOT_DIR = "nutanix-small"                   # nome cartella radice da creare
CREATE_EMPTY_FILES = True                    # crea anche i file vuoti?
SKIP_IF_EXISTS = True                        # non sovrascrive se già esiste

# Caratteri da ignorare / pulire
PREFIX_CHARS = r"│├└─│ \t"

# ────────────────────────────────────────────────

def parse_tree_line(line: str) -> tuple[str, bool]:
    """Ritorna (percorso_relativo, è_directory)"""
    # Rimuove prefissi grafici
    cleaned = re.sub(rf"^[{PREFIX_CHARS}]+", "", line.rstrip("/")).rstrip()
    if not cleaned:
        return "", False

    is_dir = line.strip().endswith("/") or "/" in cleaned
    name = cleaned.rstrip("/").strip()

    return name, is_dir


def create_structure(tree_text: str, root: str = "."):
    current_path = [root]
    created = []

    for line in tree_text.splitlines():
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        name, is_dir = parse_tree_line(line)
        if not name:
            continue

        # Conta quanti livelli di indent (approssimativo)
        indent = len(line) - len(line.lstrip(" ├└│─ \t"))
        level = indent // 4   # assumiamo 4 spazi o 1 carattere grafico ≈ 1 livello

        # Torniamo indietro nella gerarchia se necessario
        while len(current_path) > level + 1:
            current_path.pop()

        # Percorso completo
        full_path = os.path.join(*current_path, name)

        try:
            if is_dir:
                if SKIP_IF_EXISTS and os.path.exists(full_path):
                    print(f"  Esiste già → {full_path}/")
                else:
                    os.makedirs(full_path, exist_ok=True)
                    print(f"  Creata cartella → {full_path}/")
                current_path.append(name)
            else:
                # è un file
                dir_part = os.path.dirname(full_path)
                if dir_part and not os.path.exists(dir_part):
                    os.makedirs(dir_part, exist_ok=True)

                if SKIP_IF_EXISTS and os.path.exists(full_path):
                    print(f"  File esiste → {full_path}")
                else:
                    if CREATE_EMPTY_FILES:
                        open(full_path, "a", encoding="utf-8").close()
                        print(f"  Creato file vuoto → {full_path}")
                    else:
                        print(f"  Saltato file (empty creation off) → {full_path}")

            created.append(full_path)

        except Exception as e:
            print(f"Errore su {full_path}: {e}")

    print(f"\nCompletato. Creati {len(created)} elementi.")


if __name__ == "__main__":
    print(f"Creazione struttura in: ./{ROOT_DIR}\n")
    os.makedirs(ROOT_DIR, exist_ok=True)
    os.chdir(ROOT_DIR)

    create_structure(TREE)

    print("\nFatto!")
    print("Puoi ora:")
    print("  cd", ROOT_DIR)
    print("  git init   # se vuoi versionare")
    print("  # e iniziare a riempire i file")
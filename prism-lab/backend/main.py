import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

PRISM_HOST = os.getenv("PRISM_HOST")
PRISM_USER = os.getenv("PRISM_USER")
PRISM_PASS = os.getenv("PRISM_PASS")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 funzione generica Prism
def prism_post(endpoint, payload):
    url = f"{PRISM_HOST}{endpoint}"

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(PRISM_USER, PRISM_PASS),
        verify=False  # lab only
    )

    return response.json()


# 📊 VM LIST (reale)
@app.get("/api/v1/vms")
def get_vms():
    data = prism_post(
        "/api/nutanix/v3/vms/list",
        {"kind": "vm", "length": 50}
    )

    vms = []

    for vm in data.get("entities", []):
        vms.append({
            "name": vm["spec"]["name"],
            "status": vm["status"]["resources"]["power_state"]
        })

    return {"vms": vms}


# 📊 SUMMARY
@app.get("/api/v1/summary")
def summary():
    data = prism_post(
        "/api/nutanix/v3/vms/list",
        {"kind": "vm", "length": 50}
    )

    total = len(data.get("entities", []))

    running = sum(
        1 for vm in data.get("entities", [])
        if vm["status"]["resources"]["power_state"] == "ON"
    )

    return {
        "total": total,
        "running": running
    }
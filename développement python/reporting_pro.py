import json
rapport_dict = {
    "serveur": "web-01",
    "statut_general": "OK",
    "details": [
        {"check": "port_80", "statut": "OUVERT"},
        {"check": "service_nginx", "statut": "ACTIF"}
    ]
}

rapport_json = json.dumps(rapport_dict, indent=4)
print(rapport_json)
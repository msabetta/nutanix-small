# Piccolo progetto Nutanix IaC

Gestione base di Nutanix con Terraform (deploy VM) + Ansible (categorie + config guest).

## Prerequisiti
- Terraform ≥ 1.9
- Ansible ≥ 2.14 + collection nutanix.ncp (`ansible-galaxy collection install nutanix.ncp`)
- Accesso a Prism Central (utente con permessi sufficienti)

## Struttura
- terraform/ → crea VM, network, assegna categorie (se già esistenti)
- ansible/   → crea categorie + assegna + configura guest OS

## Come partire (flusso consigliato)

1. Copia terraform.tfvars.example → terraform.tfvars e valorizza
2. cd terraform && terraform init && terraform apply
3. Valorizza ansible/group_vars/all.yml (o usa vault)
4. cd ansible && ansible-playbook -i inventory.yml playbooks/00_create_categories.yml
5. ansible-playbook -i inventory.yml playbooks/10_tag_vms.yml
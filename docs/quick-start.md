# Quick Start – Nutanix piccolo progetto IaC

1. `cp terraform/terraform.tfvars.example terraform/terraform.tfvars` → modifica
2. `cd terraform && terraform init && terraform plan && terraform apply`
3. `ansible-vault edit vault/secrets.yml` (o usa --ask-vault-pass)
4. `cd ../ansible && ansible-playbook -i inventory.yml --ask-vault-pass playbooks/00_create_categories.yml`
5. `ansible-playbook -i inventory.yml --ask-vault-pass playbooks/10_tag_vms.yml`

Ordine consigliato: categorie → VM → tag → guest config
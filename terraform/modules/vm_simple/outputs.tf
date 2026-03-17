output "vm_ext_id" {
  description = "External ID (UUID v4) della VM creata"
  value       = nutanix_virtual_machine.this.id
}

output "vm_name" {
  description = "Nome della VM"
  value       = nutanix_virtual_machine.this.name
}

output "power_state" {
  description = "Stato di alimentazione attuale"
  value       = nutanix_virtual_machine.this.power_state
}

output "categories_applied" {
  description = "Categorie effettivamente applicate"
  value       = nutanix_virtual_machine.this.categories[*].ext_id
}

output "primary_ip" {
  description = "Primo indirizzo IP rilevato (se presente)"
  value       = try(nutanix_virtual_machine.this.nic_list[0].ip_endpoint_list[0].ip.value, null)
}
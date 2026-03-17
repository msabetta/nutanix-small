# output "vm_ext_id" {
#   description = "External ID della VM creata"
#   value       = nutanix_virtual_machine_v2.example_vm.id
# }

# output "vm_ip" {
#   description = "IP assegnato (se DHCP)"
#   value       = nutanix_virtual_machine_v2.example_vm.nic_list[0].ip_endpoint_list[0].ip.value   # approx
# }


# ────────────────────────────────────────────────
# Output utili
# ────────────────────────────────────────────────

output "web_server_vm_ext_id" {
  description = "External ID (UUID) della VM creata"
  value       = module.web_server.vm_ext_id
}

output "web_server_primary_ip" {
  description = "IP principale (se rilevato)"
  value       = module.web_server.primary_ip
}
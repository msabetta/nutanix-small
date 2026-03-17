variable "prism_central_ip" {
  description = "IP o FQDN di Prism Central"
  type        = string
}

variable "prism_username" {
  description = "Utente Prism Central (es. admin@dominio.local)"
  type        = string
  sensitive   = true
}

variable "prism_password" {
  description = "Password Prism Central"
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "Nome del cluster Nutanix target"
  type        = string
  default     = "NTNX-Cluster01"
}

variable "cluster_uuid" {
  description = "External ID del cluster Nutanix dove creare la VM"
  type        = string
  default = "c2f9b6a4-5d3e-4a7b-9c12-8f6e2b4d9a10"
}

variable "image_name" {
  description = "Nome immagine OS da usare (es. Rocky Linux cloud)"
  type        = string
  default     = "Rocky-9-GenericCloud-9.3-20231119.0.x86_64"
}

variable "subnet_name" {
  description = "Nome della subnet per le VM"
  type        = string
  default     = "VLAN-10-Mgmt"
}

variable "vm_name_prefix" {
  description = "Prefisso nome VM"
  type        = string
  default     = "test-iac-"
}


variable "guest_os_id" {
  description = "Guest OS ID for the VM"
  type        = string
  default     = "Ubuntu"
}

variable "num_vcpus_per_socket" {
  description = "Core per socket"
  type        = number
  default     = 2
}


variable "image_ext_id" {
  type        = string
  description = "ID univoco dell'immagine OS in Prism"
}

variable "subnet_ext_id" {
  type        = string
  description = "ID univoco della subnet in Prism"
}

variable "name" {
  description = "Nome della macchina virtuale"
  type        = string
}

variable "description" {
  description = "Descrizione opzionale della VM"
  type        = string
  default     = ""
}

variable "cluster_uuid" {
  description = "External ID del cluster Nutanix dove creare la VM"
  type        = string
}

variable "num_sockets" {
  description = "Numero di socket CPU"
  type        = number
  default     = 1
}

variable "num_vcpus_per_socket" {
  description = "Core per socket"
  type        = number
  default     = 2
}

variable "memory_size_mib" {
  description = "Quantità di RAM in MiB"
  type        = number
  default     = 4096
}

variable "guest_os_type" {
  description = "Tipo di guest OS (es. Linux, Windows)"
  type        = string
  default     = "Linux"
}


variable "guest_os_id" {
  description = "Guest OS ID for the VM"
  type        = string
}

variable "disks" {
  description = "Lista dei dischi da creare"
  type = list(object({
    size_bytes          = number
    source_image_ext_id = optional(string) # se clonare da immagine
    is_cdrom            = optional(bool, false)
  }))
  default = [
    {
      size_bytes = 53687091200 # 50 GiB
    }
  ]
}

variable "network_adapters" {
  description = "Lista delle interfacce di rete"
  type = list(object({
    subnet_ext_id = string
    ip_address    = optional(string) # IP statico opzionale
  }))
  default = []
}

variable "category_ext_ids" {
  description = "Lista di external ID delle categorie da assegnare"
  type        = list(string)
  default     = []
}

variable "cloud_init_user_data" {
  description = "Contenuto cloud-init (user-data) in chiaro"
  type        = string
  default     = ""
}

variable "power_on" {
  description = "Accendere la VM dopo la creazione?"
  type        = bool
  default     = true
}

variable "categories" {
  type    = map(string)
  default = {}
}


variable "nics" {
  description = "List of NICs"
  type = list(object({
    subnet_uuid = string
  }))
  default = []
}
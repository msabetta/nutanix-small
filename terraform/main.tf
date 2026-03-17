# terraform/main.tf
# Recupero dati esistenti
data "nutanix_cluster" "main" {
  name = var.cluster_name
}

data "nutanix_image" "os" {
  image_name = var.image_name
}

# Sottorete necessaria per le NIC (aggiunta - era mancante)
data "nutanix_subnet" "primary" {
  subnet_name = "your-subnet-name-here" # ← SOSTITUISCI con il nome reale della tua subnet
  # Oppure usa filter se preferisci: filter = "name==VLAN-10"
}

#Categoria di esempio (deve esistere già in Prism Central)
# data "nutanix_category_value_v2" "env_prod" {
#   key   = "env"
#   value = "prod"
# }

# ────────────────────────────────────────────────
# Chiamata al modulo vm_simple
# ────────────────────────────────────────────────

module "web_server" {
  source = "./modules/vm_simple"

  name        = "web-test-01"
  description = "Server web di test creato con modulo semplice"

  cluster_uuid = data.nutanix_cluster.main.id
  guest_os_id = var.guest_os_id

  num_sockets          = 1
  num_cores_per_socket = 4
  memory_size_mib      = 8192 # 8 GB

  disks = [
    {
      size_bytes          = 107374182400 # 100 GiB
      source_image_ext_id = data.nutanix_image.os.id
    }
    # Aggiungi altri dischi se necessario
  ]

  network_adapters = [
    {
      subnet_ext_id = data.nutanix_subnet.primary.id
      ip_address    = "172.16.10.45" # opzionale – IP statico
    }
  ]

  # category_ext_ids = [
  #   data.nutanix_category_value_v2.env_prod.id
  #   # Aggiungi altri ext_id se necessario
  # ]

  cloud_init_user_data = <<-EOT
    #cloud-config
    hostname: web-test-01
    fqdn:     web-test-01.lab.internal

    users:
      - name: nutanix
        ssh_authorized_keys:
          - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... la-tua-chiave-pubblica
        sudo: ALL=(ALL) NOPASSWD:ALL

    packages:
      - nginx
      - git
      - curl

    runcmd:
      - systemctl enable --now nginx
  EOT

  power_on = true
}


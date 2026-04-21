terraform {
  required_version = ">= 1.5" # o ">= 1.9" se usi features recenti

  required_providers {
    nutanix = {
      source  = "nutanix/nutanix"
      version = "~> 2.0" # usa la più recente stabile al 2026 (v2.x)
    }
  }
}

provider "nutanix" {
  endpoint = "192.168.119.128"
  username = var.prism_username
  password = var.prism_password
  insecure = true # ← solo per lab / self-signed cert – rimuovi in prod
}

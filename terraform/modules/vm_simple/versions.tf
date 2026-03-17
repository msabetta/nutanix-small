terraform {
  required_providers {
    nutanix = {
      source  = "nutanix/nutanix"
      version = "~> 2.0" # o "~> 2.4" se vuoi pin più preciso
    }
  }
}
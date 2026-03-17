# ------------------------------------------------------------------------------
# Nutanix VM - Simple Module
# ------------------------------------------------------------------------------

resource "nutanix_virtual_machine" "this" {
  name         = var.name
  cluster_uuid = var.cluster_uuid
  num_vcpus      = var.num_vcpus
  num_cores_per_vcpu = var.num_cores_per_socket
  memory_mb      = var.memory_size_mib

  guest_os_id = var.guest_os_id

  dynamic "disk_list" {
    for_each = var.disks
    content {
      data_source_reference = {
        kind = "image"
        uuid = disk_list.value.image_uuid
      }
    }
  }

  dynamic "nic_list" {
    for_each = var.nics
    content {
      subnet_uuid = nic_list.value.subnet_uuid
    }
  }
}
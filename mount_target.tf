resource "oci_file_storage_mount_target" "my_mount_target_1" {
  #Required
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"
  subnet_id           = "${oci_core_subnet.my_subnet.id}"

  #Optional
  display_name = "MountTarget_1"
}

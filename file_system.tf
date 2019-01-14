resource "oci_file_storage_file_system" "my_fs_1" {
  #Required
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"

  #Optional
  display_name = "FileSystem_1"
}

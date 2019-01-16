# Gets a list of Availability Domains
data "oci_identity_availability_domains" "ADs" {
  compartment_id = "${var.tenancy_ocid}"
}

# Gets a list of vNIC attachments on the bastion host
data "oci_core_vnic_attachments" "BastionVnics" {
  compartment_id      = "${var.compartment_ocid}"
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  instance_id         = "${oci_core_instance.BastionHost.id}"
}

# Gets the OCID of the first vNIC on the bastion host
data "oci_core_vnic" "BastionVnic" {
  vnic_id = "${lookup(data.oci_core_vnic_attachments.BastionVnics.vnic_attachments[0],"vnic_id")}"
}

# Get the Private of bastion host
data "oci_core_private_ips" "BastionPrivateIPs" {
    ip_address = "${data.oci_core_vnic.BastionVnic.private_ip_address}"
    subnet_id = "${oci_core_subnet.BastionSubnetAD1.id}"
}

# Gets the list of file systems in the compartment
data "oci_file_storage_file_systems" "file_systems" {
  #Required
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"

  #Optional fields. Used by the service to filter the results when returning data to the client.
  #display_name = "my_fs_1"
  #id = "ocid1.filesystem.oc1.phx.aaaaaaaaaaaaawynobuhqllqojxwiotqnb4c2ylefuyqaaaa"
  #state = "DELETED"
}

# Gets the list of mount targets in the compartment
data "oci_file_storage_mount_targets" "mount_targets" {
  #Required
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"

  #Optional fields. Used by the service to filter the results when returning data to the client.
  #display_name = "${var.mount_target_display_name}"
  #export_set_id = "${var.mount_target_export_set_id}"
  #id = "${var.mount_target_id}"
  #state = "${var.mount_target_state}"
}

# Gets the list of exports in the compartment
data "oci_file_storage_exports" "exports" {
  #Required
  compartment_id = "${var.compartment_ocid}"

  #Optional fields. Used by the service to filter the results when returning data to the client.
  #export_set_id = "${oci_file_storage_mount_target.my_mount_target_1.export_set_id}"
  #file_system_id = "${oci_file_storage_file_system.my_fs.id}"
  #id = "${var.export_id}"
  #state = "${var.export_state}"
}

# Gets a list of snapshots for a particular file system
#data "oci_file_storage_snapshots" "snapshots" {
  #Required
#  file_system_id = "${oci_file_storage_file_system.my_fs_1.id}"

  #Optional fields. Used by the service to filter the results when returning data to the client.
  #id = "${var.snapshot_id}"
  #state = "${var.snapshot_state}"
#}

# Gets a list of export sets in a compartment and availability domain
data "oci_file_storage_export_sets" "export_sets" {
  #Required
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"

  #Optional fields. Used by the service to filter the results when returning data to the client.
  #display_name = "${var.export_set_display_name}"
  #id = "${var.export_set_id}"
  #state = "${var.export_set_state}"
}

data "oci_core_private_ips" ip_mount_target1 {
  subnet_id = "${oci_file_storage_mount_target.my_mount_target_1.subnet_id}"

  filter {
    name   = "id"
    values = ["${oci_file_storage_mount_target.my_mount_target_1.private_ip_ids.0}"]
  }
 }

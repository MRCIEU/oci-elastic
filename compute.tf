resource "oci_core_instance" "ESVM" {
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"
  display_name        = "ESVM"
  shape               = "${var.MasterNodeShape}"

  create_vnic_details {
        subnet_id = "${oci_core_subnet.BastionSubnetAD1.id}"
        skip_source_dest_check = true
  }

  metadata {
    ssh_authorized_keys = "${var.ssh_public_key}"
	ssh_private_key     = "${var.ssh_private_key}"
    user_data           = "${base64encode(file(var.ESBootStrap))}"
  }

  source_details {
    source_id = "${var.InstanceImageOCID[var.region]}"
    source_type = "image"
    }

  timeouts {
   create = "${var.create_timeout}"
   }
}

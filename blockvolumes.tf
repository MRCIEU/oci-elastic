

#### block storage on master nodes

resource "oci_core_volume" "ESDataVol" {
    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
    compartment_id = "${var.compartment_ocid}"
    size_in_gbs = "${var.DataVolSize}"
    display_name = "ESDataVol"
 }

resource "oci_core_volume_attachment" "Attach_ESDataVol" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESVM.id}"
    volume_id = "${oci_core_volume.ESDataVol.id}"
}

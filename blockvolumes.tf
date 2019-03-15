#### NFS
#resource "oci_core_volume" "NFSBlock" {
#    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
#    compartment_id = "${var.compartment_ocid}"
#    size_in_gbs = "${var.NFSVolSize}"
#    display_name = "NFSBlock"
#}

#resource "oci_core_volume_attachment" "Attach_NFSBlock" {
#     attachment_type = "${var.volume_attachment_attachment_type}"
#	 compartment_id = "${var.compartment_ocid}"
#     instance_id = "${oci_core_instance.BastionHost.id}"
#     volume_id = "${oci_core_volume.NFSBlock.id}"
#}

#### block storage on master nodes

resource "oci_core_volume" "ESDataVol" {
	count="${var.count}"
    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
    compartment_id = "${var.compartment_ocid}"
    size_in_gbs = "${var.DataVolSize}"
    display_name = "ESDataVol${count.index}"
 }

resource "oci_core_volume_attachment" "Attach_ESDataVol" {
	count="${var.count}"
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode.*.id[count.index]}"
    volume_id = "${oci_core_volume.ESDataVol.*.id[count.index]}"
}

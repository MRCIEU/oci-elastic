#### NFS
resource "oci_core_volume" "NFSBlock" {
    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
    compartment_id = "${var.compartment_ocid}"
    size_in_gbs = "${var.NFSVolSize}"
    display_name = "NFSBlock"
 }

resource "oci_core_volume_attachment" "Attach_NFSBlock" {
     attachment_type = "${var.volume_attachment_attachment_type}"
	 compartment_id = "${var.compartment_ocid}"
     instance_id = "${oci_core_instance.BastionHost.id}"
     volume_id = "${oci_core_volume.NFSBlock.id}"
 }

#### block storage on master nodes

resource "oci_core_volume" "ESData1Vol1" {
    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
    compartment_id = "${var.compartment_ocid}"
    size_in_gbs = "${var.DataVolSize}"
    display_name = "ESData1Vol1"
 }

resource "oci_core_volume" "ESData2Vol2" {
    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
    compartment_id = "${var.compartment_ocid}"
    size_in_gbs = "${var.DataVolSize}"
    display_name = "ESData2Vol2"
 }

resource "oci_core_volume" "ESData3Vol3" {
    availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
    compartment_id = "${var.compartment_ocid}"
    size_in_gbs = "${var.DataVolSize}"
    display_name = "ESData3Vol3"
 }


resource "oci_core_volume_attachment" "Attach_ESData1Vol1" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode1.id}"
    volume_id = "${oci_core_volume.ESData1Vol1.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData2Vol2" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode2.id}"
    volume_id = "${oci_core_volume.ESData2Vol2.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData3Vol3" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode3.id}"
    volume_id = "${oci_core_volume.ESData3Vol3.id}"
}

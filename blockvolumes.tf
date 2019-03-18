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

resource "oci_core_volume" "ESData4Vol4" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData4Vol4"
}

resource "oci_core_volume" "ESData5Vol5" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData5Vol5"
}

resource "oci_core_volume" "ESData6Vol6" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData6Vol6"
}

resource "oci_core_volume" "ESData7Vol7" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData7Vol7"
}

resource "oci_core_volume" "ESData8Vol8" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData8Vol8"
}

resource "oci_core_volume" "ESData9Vol9" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData9Vol9"
}

resource "oci_core_volume" "ESData10Vol10" {
 availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
 compartment_id = "${var.compartment_ocid}"
 size_in_gbs = "${var.DataVolSize}"
 display_name = "ESData10Vol10"
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

resource "oci_core_volume_attachment" "Attach_ESData4Vol4" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode4.id}"
    volume_id = "${oci_core_volume.ESData4Vol4.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData5Vol5" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode5.id}"
    volume_id = "${oci_core_volume.ESData5Vol5.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData6Vol6" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode6.id}"
    volume_id = "${oci_core_volume.ESData6Vol6.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData7Vol7" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode7.id}"
    volume_id = "${oci_core_volume.ESData7Vol7.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData8Vol8" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode8.id}"
    volume_id = "${oci_core_volume.ESData8Vol8.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData9Vol9" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode9.id}"
    volume_id = "${oci_core_volume.ESData9Vol9.id}"
}

resource "oci_core_volume_attachment" "Attach_ESData10Vol10" {
    attachment_type = "${var.volume_attachment_attachment_type}"
    instance_id = "${oci_core_instance.ESMasterNode10.id}"
    volume_id = "${oci_core_volume.ESData10Vol10.id}"
}

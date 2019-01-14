resource "oci_core_instance" "BastionHost" {
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"
  display_name        = "BastionHost"
  shape               = "${var.BastionShape}"

  create_vnic_details {
        subnet_id = "${oci_core_subnet.BastionSubnetAD1.id}"
        skip_source_dest_check = true
  }

  metadata {
    ssh_authorized_keys = "${var.ssh_public_key}"
    user_data           = "${base64encode(file(var.BastionBootStrap))}"
  }

  source_details {
    source_id = "${var.InstanceImageOCID[var.region]}"
    source_type = "image"
    }

  timeouts {
   create = "${var.create_timeout}"
   }
}

resource "oci_core_instance" "ESMasterNode1" {
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"
  display_name        = "ESMasterNode1"
  shape               = "${var.MasterNodeShape}"
  depends_on          = ["oci_core_instance.BastionHost"]

 create_vnic_details {
       subnet_id = "${oci_core_subnet.PrivSubnetAD1.id}"
       assign_public_ip = false
  }

  metadata {
    ssh_authorized_keys = "${var.ssh_public_key}"
    user_data           = "${base64encode(file(var.ESBootStrap))}"
  }

  source_details {
    source_id = "${var.InstanceImageOCID[var.region]}"
    source_type = "image"
    boot_volume_size_in_gbs = "${var.BootVolSize}"
    }

  timeouts {
   create = "${var.create_timeout}"
   }
}

resource "oci_core_instance" "ESMasterNode2" {
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"
  display_name        = "ESMasterNode2"
  shape               = "${var.MasterNodeShape}"
  depends_on          = ["oci_core_instance.BastionHost"]

 create_vnic_details {
       subnet_id = "${oci_core_subnet.PrivSubnetAD2.id}"
       assign_public_ip = false
  }

 metadata {
    ssh_authorized_keys = "${var.ssh_public_key}"
    user_data           = "${base64encode(file(var.ESBootStrap))}"
  }

  source_details {
    source_id = "${var.InstanceImageOCID[var.region]}"
    source_type = "image"
    boot_volume_size_in_gbs = "${var.BootVolSize}"
    }

  timeouts {
   create = "${var.create_timeout}"
   }
}

resource "oci_core_instance" "ESMasterNode3" {
  availability_domain = "${lookup(data.oci_identity_availability_domains.ADs.availability_domains[1],"name")}"
  compartment_id      = "${var.compartment_ocid}"
  display_name        = "ESMasterNode3"
  shape               = "${var.MasterNodeShape}"
  depends_on          = ["oci_core_instance.BastionHost"]

 create_vnic_details {
       subnet_id = "${oci_core_subnet.PrivSubnetAD3.id}"
       assign_public_ip = false
  }

 metadata {
    ssh_authorized_keys = "${var.ssh_public_key}"
    user_data           = "${base64encode(file(var.ESBootStrap))}"
  }

  source_details {
    source_id = "${var.InstanceImageOCID[var.region]}"
    source_type = "image"
    boot_volume_size_in_gbs = "${var.BootVolSize}"
    }

  timeouts {
   create = "${var.create_timeout}"
   }
}

resource "null_resource" "mount_fss_on_ESMasterNode1" {
  depends_on = ["oci_core_instance.ESMasterNode1",
    "oci_file_storage_export.my_export_fs1_mt1",
  ]

  provisioner "remote-exec" {
    connection {
      agent       = false
      timeout     = "15m"
      host        = "${oci_core_instance.ESMasterNode1.private_ip}"
      user        = "opc"
      private_key = "${var.ssh_private_key}"
    }

    inline = [
      "sudo yum -y install nfs-utils > nfs-utils-install.log",
      "sudo mkdir -p /mnt/myfsspaths/fs1/path1",
      "sudo mount ${local.mount_target_1_ip_address}:${var.export_path_fs1_mt1} /mnt${var.export_path_fs1_mt1}",
    ]
  }
}

resource "null_resource" "mount_fss_on_ESMasterNode2" {
  depends_on = ["oci_core_instance.ESMasterNode2",
    "oci_file_storage_export.my_export_fs1_mt1",
  ]

  provisioner "remote-exec" {
    connection {
      agent       = false
      timeout     = "15m"
      host        = "${oci_core_instance.ESMasterNode2.private_ip}"
      user        = "opc"
      private_key = "${var.ssh_private_key}"
    }

    inline = [
      "sudo yum -y install nfs-utils > nfs-utils-install.log",
      "sudo mkdir -p /mnt/myfsspaths/fs1/path1",
      "sudo mount ${local.mount_target_1_ip_address}:${var.export_path_fs1_mt1} /mnt${var.export_path_fs1_mt1}",
    ]
  }
}

resource "null_resource" "mount_fss_on_ESMasterNode3" {
  depends_on = ["oci_core_instance.ESMasterNode3",
    "oci_file_storage_export.my_export_fs1_mt1",
  ]

  provisioner "remote-exec" {
    connection {
      agent       = false
      timeout     = "15m"
      host        = "${oci_core_instance.ESMasterNode3.prviate_ip}"
      user        = "opc"
      private_key = "${var.ssh_private_key}"
    }

    inline = [
      "sudo yum -y install nfs-utils > nfs-utils-install.log",
      "sudo mkdir -p /mnt/myfsspaths/fs1/path1",
      "sudo mount ${local.mount_target_1_ip_address}:${var.export_path_fs1_mt1} /mnt${var.export_path_fs1_mt1}",
    ]
  }
}

variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "region" {}

variable "compartment_ocid" {}
variable "ssh_public_key" {}
variable "ssh_private_key" {}

variable "BastionShape" {
  //default = "VM.Standard2.1"
  default = "VM.Standard2.24"
}

variable "MasterNodeShape" {
  default = "VM.Standard.E2.8"
  //default = "VM.DenseIO2.24"
}

variable "DataNodeShape" {
  default = "VM.Standard2.2"
}

variable "BootVolSize" {
  default = "100"
}

variable "lb_shape" {
  default = "100Mbps"
}

variable "InstanceImageOCID" {
  type = "map"

  default = {
    // See https://docs.us-phoenix-1.oraclecloud.com/images/
    // Oracle-provided image "Oracle-Linux-7.4-2018.02.21-1"
    us-phoenix-1   = "ocid1.image.oc1.phx.aaaaaaaasez4lk2lucxcm52nslj5nhkvbvjtfies4yopwoy4b3vysg5iwjra"
    us-ashburn-1   = "ocid1.image.oc1.iad.aaaaaaaa2tq67tvbeavcmioghquci6p3pvqwbneq3vfy7fe7m7geiga4cnxa"
    eu-frankfurt-1 = "ocid1.image.oc1.eu-frankfurt-1.aaaaaaaakzrywmh7kwt7ugj5xqi5r4a7xoxsrxtc7nlsdyhmhqyp7ntobjwq"
    //uk-london-1    = "ocid1.image.oc1.uk-london-1.aaaaaaaalsdgd47nl5tgb55sihdpqmqu2sbvvccjs6tmbkr4nx2pq5gkn63a"
	uk-london-1    = "ocid1.image.oc1.uk-london-1.aaaaaaaarruepdlahln5fah4lvm7tsf4was3wdx75vfs6vljdke65imbqnhq"
  }
}

variable "VCN-CIDR" {
  default = "192.168.0.0/25"
}

variable "BastSubnetAD1CIDR" {
  default = "192.168.0.0/28"
}

variable "PrivSubnetAD1CIDR" {
  default = "192.168.0.16/28"
}

variable "PrivSubnetAD2CIDR" {
  default = "192.168.0.32/28"
}

variable "PrivSubnetAD3CIDR" {
  default = "192.168.0.48/28"
}

variable "LBSubnetAD1CIDR" {
  default = "192.168.0.64/28"
}

variable "LBSubnetAD2CIDR" {
  default = "192.168.0.80/28"
}

variable "ESBootStrap" {
  default = "./userdata/ESBootStrap.sh"
}

variable "BastionBootStrap" {
  default = "./userdata/BastionBootStrap.sh"
}

variable "backend_set_health_checker_interval_ms" {
  default = "15000"
}

variable "KibanaPort" {
  default = "5601"
}

variable "ESDataPort" {
  default = "9200"
}

variable "create_timeout" {
  default ="60000m"
}

variable "DataVolSize" {
  default = "3000"
}

variable "NFSVolSize" {
  default = "1024"
}

variable "volume_attachment_attachment_type" {
  default = "iscsi"
}

variable "export_path_fs1_mt1" {
  default = "/myfsspaths/fs1/path1"
}

variable "export_read_write_access_source" {
  #default = "10.0.0.0/8"
  #default = "192.168.0.0/28"
  default = "0.0.0.0/0"
}

variable "export_read_only_access_source" {
  default = "0.0.0.0/0"
}

variable "max_byte" {
  default = 2384320233300
}

variable "export_set_name_1" {
  default = "export set for mount target 1"
}

variable "max_files" {
  default = 223442
}

locals {
  mount_target_1_ip_address = "${lookup(data.oci_core_private_ips.ip_mount_target1.private_ips[0], "ip_address")}"
 }

variable "my_vcn-cidr" {
  #default = "10.0.0.0/16"
  default = "192.168.0.0/16"
}

#variable "my_subnet_cidr" {
#  default = "10.0.1.0/24"
#}

variable "my_subnet_cidr" {
  default = "192.168.0.96/28"
}

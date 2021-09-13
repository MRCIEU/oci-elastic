#! /bin/bash

## NFS - https://github.com/terraform-providers/terraform-provider-oci/blob/master/docs/examples/storage/nfs/userdata/nfs-bootstrap
### Send stdout, stderr to /var/log/messages/
#exec 1> >(logger -s -t $(basename $0)) 2>&1

# ### Storage setup
# wget -O /usr/local/bin/iscsiattach.sh https://raw.githubusercontent.com/oracle/terraform-provider-oci/master/docs/examples/storage/nfs/userdata/iscsiattach.sh
# chmod +x /usr/local/bin/iscsiattach.sh
# /usr/local/bin/iscsiattach.sh
# mkfs.xfs /dev/sdb
# mkdir /mnt/nfs
# mount -t xfs /dev/sdb /mnt/nfs/
# sdb_uuid=`blkid /dev/sdb -s UUID -o value`
# echo "UUID=$sdb_uuid    /mnt/nfs    xfs    defaults,noatime,_netdev,nofail" >> /etc/fstab
#
#
# ### NFS setup
# firewall-offline-cmd --zone=public --add-service=nfs
# yum -y install nfs-utils
# systemctl enable nfs-server.service
# systemctl start nfs-server.service
# chown nfsnobody:nfsnobody /mnt/nfs/
# chmod 777 /mnt/nfs/
# cidr=`ip addr show dev ens3 | grep "inet " | awk -F' ' '{print $2}'`
# echo "/mnt/nfs $cidr(rw,sync,no_subtree_check)" > /etc/exports
# exportfs -a

### YUM update
#yum update -y

## Enables Bastion Host as NAT instance for ES master/data nodes to update/install software from internet.
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
firewall-offline-cmd --direct --add-rule ipv4 nat POSTROUTING 0 -o ens3 -j MASQUERADE
firewall-offline-cmd --direct --add-rule ipv4 filter FORWARD 0 -i ens3 -j ACCEPT
sysctl -p

systemctl restart firewalld
mkdir /home/opc/bin
for i in {0..11}; do echo '#!/bin/bash' > /home/opc/bin/node${i}; echo "ssh esmasternodev3${i}.privad1.ociesvcn.oraclevcn.com" >> /home/opc/bin/node${i}; done
chown opc /home/opc/bin/*
chmod 700 /home/opc/bin/*
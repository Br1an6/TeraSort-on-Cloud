#!/bin/bash

# You may want to put your own key
eval `ssh-agent -s`
ssh-add ~/i3keypair.pem

# sudo fdisk -l
sudo mkdir /mnt

#Added for mount: wrong fs type, bad option, bad superblock error
#sudo mkfs.ext4 /dev/nvme0n1

sudo mount /dev/nvme0n1 /mnt
# lsblk -o "NAME,MAJ:MIN,RM,SIZE,RO,FSTYPE,MOUNTPOINT,UUID"
sudo chmod 777 /mnt/

cd /mnt

mkdir -p hdfs
mkdir -p hdfs/namenode
mkdir -p hdfs/datanode
mkdir -p tmp
mkdir -p tmp/hadoop-ubuntu

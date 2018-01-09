#!/bin/bash

# You may want to put your own key
eval `ssh-agent -s`

ssh-add aws.pem

# lsblk -o "NAME,MAJ:MIN,RM,SIZE,RO,FSTYPE,MOUNTPOINT,UUID"
sudo mdadm

sudo mdadm --create --verbose /dev/md0 --level=0 --name=PA2_RAID --raid-devices=2 /dev/nvme0n1 /dev/nvme1n1

sudo mkfs.ext4 -L PA2_RAID /dev/md0

sudo mkdir -p /mnt/raid

sudo mount LABEL=PA2_RAID /mnt/raid


sudo chmod 777 /mnt/raid/


rm -Rf /mnt/raid/hdfs/*
rm -Rf /mnt/raid/tmp/*

cd /mnt/raid/

mkdir -p hdfs
mkdir -p hdfs/namenode
mkdir -p hdfs/datanode
mkdir -p tmp
mkdir -p tmp/hadoop-ubuntu

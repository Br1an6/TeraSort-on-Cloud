#!/bin/bash

dir=$(pwd)
if [ $dir != '/mnt' ]
then
	echo "Please make sure that current location is under /mnt"
fi


echo "[*] Generating 1 TB"
./gensort -a 10000000000 input
echo "[*] File generated"


# Please make sure that current location is uder /mnt
python shared_memory_sort.py 1 input output -b 10G -k "line[0:10]" -t /mnt

echo "[*] File sorted"
echo "[*] validating file"
./valsort output

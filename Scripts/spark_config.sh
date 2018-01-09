#!/bin/bash

sudo apt-get update
sudo apt-get install default-jre
sudo apt-get install default-jdk
sudo apt install unzip

wget https://downloads.lightbend.com/scala/2.11.11/scala-2.11.11.tgz
tar xvf scala-2.11.11.tgz
rm scala-2.11.11.tgz
sudo mv scala-2.11.11 /mnt/scala

export PATH=$PATH:/mnt/scala/bin

wget http://apache.claz.org/spark/spark-2.1.2/spark-2.1.2-bin-hadoop2.7.tgz
tar xvf spark-2.1.2-bin-hadoop2.7.tgz
sudo mv spark-2.1.2-bin-hadoop2.7 /mnt/spark 

export PATH=$PATH:/mnt/spark/bin

echo "export LD_LIBRARY_PATH=/home/ubuntu/hadoop/lib/native/:$LD_LIBRARY_PATH" >> .bashrc
# source ~/.bashrc
# vi /usr/local/spark/python/pyspark/shell.py remove enableHiveSupport

#if needed
sudo apt-get install python
echo "export your key" >> .bashrc
echo "export your key" >> .bashrc

echo "export SPARK_HOME=/mnt/spark" >> .bashrc
echo "export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH" >> .bashrc

wget https://github.com/amplab/spark-ec2/archive/branch-2.0.zip
sudo unzip branch-2.0.zip -d $SPARK_HOME
mv $SPARK_HOME/spark-ec2-branch-2.0 $SPARK_HOME/ec2

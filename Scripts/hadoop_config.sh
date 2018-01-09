#!/bin/bash

sudo apt-get update
sudo apt-get install default-jre
sudo apt-get install default-jdk

# You may want to put your own key
eval `ssh-agent -s`
chmod 400 i3keypair.pem
ssh-add i3keypair.pem

cd /mnt/

wget http://apache.claz.org/hadoop/common/hadoop-2.8.1/hadoop-2.8.1.tar.gz

tar -xzf hadoop-2.8.1.tar.gz
rm hadoop-2.8.1.tar.gz
mv hadoop-2.8.1 hadoop

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
export HADOOP_PREFIX=/mnt/hadoop
# java
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre" >> .bashrc
echo "export HADOOP_PREFIX=/mnt/hadoop" >> .bashrc

# hadoop
echo "export HADOOP_HOME=$HADOOP_PREFIX" >> .bashrc
# echo "export PATH=$PATH:$HADOOP_HOME/bin" >> .bashrc # Put this inside your basrc if you want
# echo "export PATH=$PATH:$HADOOP_HOME/sbin" >> .bashrc # Put this inside your basrc if you want
echo "export HADOOP_COMMON_HOME=$HADOOP_PREFIX" >> .bashrc
echo "export HADOOP_CONF_DIR=$HADOOP_PREFIX/etc/hadoop" >> .bashrc
echo "export HADOOP_HDFS_HOME=$HADOOP_PREFIX" >> .bashrc
echo "export HADOOP_MAPRED_HOME=$HADOOP_PREFIX" >> .bashrc
echo "export HADOOP_YARN_HOME=$HADOOP_PREFIX" >> .bashrc
echo "export HADOOP_OPTS=-Djava.net.preferIPv4Stack=true" >> .bashrc
echo "export HADOOP_CLASSPATH=/usr/lib/jvm/java-8-openjdk-amd64/lib/tools.jar" >> .bashrc
source .bashrc

# hadoop env property
cd /mnt/hadoop/etc/hadoop
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre" >> hadoop-env.sh
echo "export HADOOP_PREFIX=/mnt/hadoop" >> hadoop-env.sh
echo "export HADOOP_HOME=$HADOOP_PREFIX" >> hadoop-env.sh
echo "export HADOOP_COMMON_HOME=$HADOOP_PREFIX" >> hadoop-env.sh
echo "export HADOOP_CONF_DIR=$HADOOP_PREFIX/etc/hadoop" >> hadoop-env.sh
echo "export HADOOP_HDFS_HOME=$HADOOP_PREFIX" >> hadoop-env.sh
echo "export HADOOP_MAPRED_HOME=$HADOOP_PREFIX" >> hadoop-env.sh
echo "export HADOOP_YARN_HOME=$HADOOP_PREFIX" >> hadoop-env.sh
echo "export HADOOP_OPTS=-Djava.net.preferIPv4Stack=true" >> hadoop-env.sh


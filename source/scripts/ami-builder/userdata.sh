#!/bin/bash

# USER DATA TO INSTALL LATEST CASSANDRA

# add oracle repo to install java later
add-apt-repository -y ppa:webupd8team/java
echo "---------- ORACLE REPO ADDED ------------"


# add apache repo
echo "deb http://www.apache.org/dist/cassandra/debian 310x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl -s https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
echo "---------- Apache Repo and Keys added ----------"

# update apt
apt-get update
echo "---------- APT UPDATED ----------"


# oracle license needs to be agreed to before installing java8
echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
# install java 8
apt-get install -y oracle-java8-installer
echo "---------- JAVA 8 INSTALLED ----------"

# install apache cassandra
apt-get install -y cassandra
echo "---------- CASSANDRA INSTALLED ----------"

# stop cassandra
service cassandra stop

# Installing Python, AWS CLI, and jq

# if python and curl if not installed
hash python 2>/dev/null || { apt-get install -y python; echo "---------- PYTHON INSTALLED ----------"; }
hash curl 2>/dev/null || { apt-get install -y curl; echo "---------- CURL INSTALLED ----------"; }

# once python & curl are installed, install PIP
curl -s https://bootstrap.pypa.io/get-pip.py | python
echo "---------- PIP INSTALLED ----------"

# use PIP to install awscli
pip install awscli

# check aws version
aws --version
echo "---------- AWS CLI INSTALLED ----------"

# install systems manager agent
cd /tmp
wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb
dpkg -i amazon-ssm-agent.deb
systemctl enable amazon-ssm-agent
echo "---------- SYSTEMS MANAGER INSTALLED ----------"

################################################################################

# Tag the current instance as having completed this bootstrapping script

INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

# get the current region
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
REGION=${AZ::-1} # remove the last letter to get the current region

# use aws cli to add a Tag
aws --region ${REGION} ec2 create-tags --resources ${INSTANCE_ID} --tags Key=Bootstrapping,Value=complete

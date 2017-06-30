#!/bin/bash

# Installing the AWS CLI and Python SDK
# These commands are intended to be run on nix-based EC2 instances
# Run these individually by hand or execute this script
#
apt-get update
# if python and curl if not installed
hash python 2>/dev/null || { apt-get install -y python; }
hash curl 2>/dev/null || { apt-get install -y curl; }
hash jq 2>/dev/null || { apt-get install -y jq; } # jq is a JSON parse and query tool, very helpful for manipulating JSON returned from AWS CLI

# once python & curl are installed, install PIP
curl -s https://bootstrap.pypa.io/get-pip.py | python

# use PIP to install awscli
pip install awscli

# check aws version
aws --version
# should return (or greater versions)
# aws-cli/1.11.93 Python/2.7.12 Linux/4.9.27-moby botocore/1.5.56

# install Boto3, the AWS Python SDK
pip install boto3

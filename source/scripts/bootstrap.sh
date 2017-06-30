#!/bin/bash

# install cloudwatch logs
curl https://s3.amazonaws.com//aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -O
chmod +x ./awslogs-agent-setup.py

# config file is in S3
./awslogs-agent-setup.py -n -r us-east-1 -c s3://path/to/cloudwatch-logs/config

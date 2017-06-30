import boto3
import json
import time
import sys

def handle_cleanup(event, context):
    client = boto3.client('ec2')

    # find instances by tag
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Environment',
                'Values': [
                    'dev',
                    'sandbox'
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running'
                ]
            }
        ]
    )

    # gather instances IDs in lists according to tag
    instances = {
        'dev': [],
        'sandbox': []
    }

    # iterate through Reservations
    for reservation in response['Reservations']:
        # iterate through instances in each reservation
        for instance in reservation['Instances']:
            # use "generator expression" to find Tag by value of Key
             tag = (x for x in instance['Tags'] if x["Key"] == "Environment").next()

             # Value of tag should be one of 'dev' or 'sandbox'
             if tag['Value'] in instances:
                 # add the instance id to end of list
                 instances[tag['Value']].append(instance['InstanceId'])

    # STOP 'dev' instances
    if len(instances['dev']) > 0 :
        print "stopping " + json.dumps(instances['dev'])
        response = client.stop_instances(InstanceIds=instances['dev'])

    # TERMINATE 'sondbox' instances
    if len(instances['sandbox']) > 0 :
        print "terminating " + json.dumps(instances['sandbox'])
        response = client.terminate_instances(InstanceIds=instances['sandbox'])

    return {
        'status' : 'clean'
    }

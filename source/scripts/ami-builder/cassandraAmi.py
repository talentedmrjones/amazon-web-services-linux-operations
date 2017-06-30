import boto3
import json
import time
import os
import sys

session = boto3.session.Session(profile_name='admin') # we will NOT use profile_name when running in EC2 or Lambda
client = session.client('ec2')

# find latest Ubuntu
print 'Finding latest Ubuntu 16.04 image...'
response = client.describe_images(
    Owners=['099720109477'],
    Filters=[
        {
            'Name': 'architecture',
            'Values': ['x86_64']
        },
        {
            'Name': 'virtualization-type',
            'Values': ['hvm']
        },
        {
            'Name': 'root-device-type',
            'Values': ['ebs']
        },
        {
            'Name': 'name',
            'Values': ['ubuntu/images/hvm-ssd/ubuntu-xenial-16.04*']
        }
    ]
)

# sort Images by creation date so we can pull the latest from the top
response['Images'].sort(key=lambda x: x['CreationDate'], reverse=True)

imageId = response['Images'][0]['ImageId']
print imageId

# capture our userdata script
with open(os.path.dirname(sys.argv[0]) + '/userdata.sh', 'r') as myfile:
    userdata=myfile.read()

# launch an ec2 instance with User Data
print 'Launching ec2 instance...'
response = client.run_instances(
    ImageId=imageId,
    MinCount=1,
    MaxCount=1,
    IamInstanceProfile={'Name':'EC2AmiBuilder'},
    InstanceType='t2.medium', # while bursting we get the same performance as c4.large for half the price
    UserData=userdata,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Bootstrapping',
                    'Value': 'pending'
                },
            ]
        },
    ]
)

# capture the instance id
instanceId = response['Instances'][0]['InstanceId']


# wait for the instance to be running
waiter = client.get_waiter('instance_running')
waiter.wait(InstanceIds=[instanceId])
print instanceId + ' is running.'
print 'Instance is bootstrapping...'


# monitor the tags to see when the instance tags itself as complete
ec2 = session.resource('ec2')
instance = ec2.Instance(instanceId)

while (instance.tags[0]['Value'] != 'complete'):
    time.sleep(10)
    instance.reload()
    print instance.tags[0]['Value']

# user data has now finished installing, so create AMI

print 'Creating Image...'

image = instance.create_image(Name='cassandra' + time.strftime('%Y%m%d'))

while (image.state == 'pending'):
    time.sleep(10)
    image.reload()
    print image.state

# image is complete, terminate the instance
print 'Terminating instance'

instance.terminate()

print 'Image Created: ' + image.name + ' (' + image.id + ')'

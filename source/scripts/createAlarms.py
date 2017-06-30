import boto3

# we will NOT use profile_name when running in EC2 or Lambda
session = boto3.session.Session(profile_name='dev')

ec2 = session.client('ec2')
cloudwatch = session.client('cloudwatch')

# first find instances that are not terminating or terminated
response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending',
                'running',
                'stopping',
                'stopped'
            ]
        }
    ]
)

# iterate over instances
for reservation in response['Reservations']:
    for instance in reservation['Instances']:

        # CHALLENGE: You can't create the same alarm twice
        # implement a way to check if the alarm already exists
        # doesn't necessarily require a call to cloudwatch
        # hint: key/value pairs

        # create alarm for this instance
        cloudwatch.put_metric_alarm(
            AlarmName='CPU_Utilization_'+instance['InstanceId'],
            ComparisonOperator='GreaterThanThreshold',
            Period=300,
            EvaluationPeriods=1,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistic='Average',
            Threshold=70.0,
            ActionsEnabled=True,
            AlarmActions=[
              '<topic arn>'
            ],
            AlarmDescription='Alarm when server CPU exceeds 70%',
            Dimensions=[
                {
                  'Name': 'InstanceId',
                  'Value': instance['InstanceId']
                },
            ],
            Unit='Seconds'
        )

        print 'Created alarm: CPU_Utilization_'+instance['InstanceId']

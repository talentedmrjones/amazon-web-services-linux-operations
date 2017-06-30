import sys
import boto3

session = boto3.session.Session(profile_name='dev') # we will NOT use profile_name when running in EC2
client = session.client('route53')

zone = sys.argv[1]
name = sys.argv[2]
ip = sys.argv[3]

# get the hosted zone ID
response  = client.list_hosted_zones_by_name(
    DNSName=zone,
    MaxItems='1'
)

hostedZoneId = response['HostedZones'][0]['Id']

response = client.change_resource_record_sets(
    HostedZoneId=hostedZoneId,
    ChangeBatch={
        "Comment": "Update record for " + name,
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": name + ".",
                    "Type": "A",
                    "TTL": 30,
                    "ResourceRecords": [
                        {
                            "Value": ip
                        }
                    ]
                }
            }
        ]
    }
)

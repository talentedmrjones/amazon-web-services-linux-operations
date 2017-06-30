import sys
import boto3

session = boto3.session.Session(profile_name='dev') # we will NOT use profile_name when running in EC2
client = session.client('ec2')

# find all volumes that are not currently attached
print 'Finding volumes...'
response = client.describe_volumes(
    Filters=[
        {
            'Name': 'status',
            'Values': [
                'available'
            ]
        }
    ]
)

if len(response['Volumes']) == 0:
    print 'found none.'
    sys.exit()

print 'Found ' + str(len(response['Volumes']))

# make a list to hold snapshot ids
snapshotIds = []

# iterate through volumes and snapshot them all concurrently
for volume in response['Volumes']:

    # initiate a snapshot
    snapshot = client.create_snapshot(
        VolumeId=volume['VolumeId']
    )

    # add snapshot id to list
    snapshotIds.append(snapshot['SnapshotId'])

    # CHALLENGE
    # here within the for loop, mark the snapshot in way
    # that indicates what volume it came from
    # hint: key/value pairs

print 'Waiting for snapshots...'
# wait for all snapshots to complete
waiter = client.get_waiter('snapshot_completed')
waiter.wait(
    SnapshotIds=snapshotIds
)

print 'Deleting volumes...'
# now delete the volumes
for volume in response['Volumes']:
    client.delete_volume(VolumeId=volume['VolumeId'])

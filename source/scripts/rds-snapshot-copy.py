import boto3
import json
import datetime
import sys

# we will NOT use profile_name when running in Lambda
# profile_name is for running locally
session = boto3.session.Session(profile_name='dev')
client = session.client('rds')

# second client in Oregon to perform copy_db_snapshot
clientWest = session.client('rds', region_name='us-west-2')

# find RDS db instances
print 'Finding DB Instances...'
response = client.describe_db_instances()

dbInstances = response['DBInstances']

# for each instance create snapshots
for dbInstance in dbInstances:

    print 'Creating snapshot for ' + dbInstance['DBName']

    response = client.create_db_snapshot(
        DBSnapshotIdentifier=dbInstance['DBName'] + '-' + datetime.datetime.today().strftime('%Y-%m-%d'),
        DBInstanceIdentifier=dbInstance['DBInstanceIdentifier']
    )

    dbSnapshot = response['DBSnapshot']

    # wait for snapshot to complete
    print 'Waiting for completion of snapshot ' + dbSnapshot['DBSnapshotIdentifier']
    waiter = client.get_waiter('db_snapshot_completed')
    waiter.wait(DBSnapshotIdentifier=dbSnapshot['DBSnapshotIdentifier'])

    # to copy to another region, we must make the copy call FROM that region
    print 'Copying snapshot...'
    response = clientWest.copy_db_snapshot(
        SourceDBSnapshotIdentifier='arn:aws:rds:us-east-2:<dev account number>:snapshot:'+dbSnapshot['DBSnapshotIdentifier'],
        TargetDBSnapshotIdentifier=dbSnapshot['DBSnapshotIdentifier'],
        CopyTags=True,
        SourceRegion='us-east-2'
    )

print 'Done!'

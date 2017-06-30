#!/bin/bash
# capture old key to delete later
OLD_KEY=$(aws configure get aws_access_key_id)

# create new credentials
printf "Creating new keys...\n"
CREDS=$(aws iam create-access-key --user-name $1)

# set those credentials
printf "Set access key...\n"
aws configure set aws_access_key_id $(echo $CREDS | jq -r '.AccessKey.AccessKeyId')
printf "Set secret key...\n"
aws configure set aws_secret_access_key $(echo $CREDS | jq -r '.AccessKey.SecretAccessKey')

# delete the old ones
printf "Deleting old key $OLD_KEY ..."
sleep 10
aws iam delete-access-key --user-name $1 --access-key-id "$OLD_KEY"

printf "Done\n"

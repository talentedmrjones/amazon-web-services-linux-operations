#!/bin/bash

# REBUILD DOCKER IMAGE

# first get the repo URI
REPO_URI=$(aws --profile admin ecr describe-repositories --repository-names microservices/billing --query 'repositories[0].repositoryUri' --output text) && echo ${REPO_URI}

# get the version from our package.json
VERSION=$(cat source/services/billing/package.json | jq -r '.version') && echo ${VERSION}

# first build the NEW docker image
docker build -t ${REPO_URI}:${VERSION} source/services/billing/

# ensure docker is logged in to the private registry
aws --profile admin ecr get-login --registry-ids <admin account number> --no-include-email | bash

# push the image to the repo
docker push ${REPO_URI}:${VERSION}

# get role arn
ROLE_ARN=$(aws --profile dev iam get-role --role-name EcsTaskRoleForServiceBilling --query 'Role.Arn' --output text) && echo ${ROLE_ARN}

# update the task-definition.json file using some bash magic ("in-place editing")
# http://backreference.org/2011/01/29/in-place-editing-of-files/
{ rm source/configs/services/billing/task-definition.json; jq -r ".containerDefinitions[0].image = \"${REPO_URI}:${VERSION}\"" > source/configs/services/billing/task-definition.json; } < source/configs/services/billing/task-definition.json


# create the task definition and capture task Arn
TASK_ARN=$(aws --profile dev ecs register-task-definition --task-role-arn ${ROLE_ARN} --cli-input-json file://source/configs/services/billing/task-definition.json --query 'taskDefinition.taskDefinitionArn' --output text) && echo ${TASK_ARN}

# update the service
aws --profile dev ecs update-service --cluster microservices-dev-ohio --service billing --task-definition ${TASK_ARN}

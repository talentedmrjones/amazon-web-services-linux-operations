#!/bin/bash
read -s -p "Enter Old Password: " OLD_PASS
printf "\n"
read -s -p "Enter New Password (blank for auto): " NEW_PASS
printf "\n"
if [ "$NEW_PASS"=="" ]; then
	# capture a new strong password (upper, lower, numbers, special chars, 32 length)
	NEW_PASS=$(< /dev/urandom tr -dc 'a-zA-Z0-9~!@#$%^&*_-' | head -c${1:-32}; echo;)
fi

aws --profile admin iam change-password --old-password $OLD_PASS --new-password $NEW_PASS

if [ $? -eq 0 ]; then
	echo "Your new password is: $NEW_PASS"
fi

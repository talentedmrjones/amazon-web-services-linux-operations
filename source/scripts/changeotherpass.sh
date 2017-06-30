# to change someone elses password, best to enforce update on next login
# to run:
# ./changeotherpass.sh <user name>

aws iam update-login-profile --user-name $1 --password "cH4n63M3N0w!" --password-reset-required

# sts_persist
Agent &amp; Reporter for persisting STS credentials

AWS Instances may be assigned IAM roles, which have temporary credentials, expiring after between 15mins and 36 hours.
If you aren't able to use the role to create a different user for long-term access, you can use this to keep your AWS profile up to date with the current session key and token.


PREREQUISITES:

1 - Install awscli (pip install awscli)

2 - Install flask (pip install flask)

3 - Set up an awscli initial profile (aws configure)

	You may use bogus info for the initial profile, it just needs to create the config/credentials file structure
	
4 - Run run.py

	It's a foreground process, so you'll probably want to do this in screen
	
5 - Update sts_persist.py Line 9 with reporter IP/Hostname:

	This will let the agent know where to send the credentials
	
5 - Deploy and run the sts_persist.py script on the victim.

	Set it in cron, run it every 5 mins or so
	TODO: Loop it

Every time sts_persist.py triggers it will send a message to your host.
The flask app will update your awscli credentials file with the new or updated profile.
You can check the credentials file for newly added profiles.
Profile names are in the format of <account_id>:<role_name>

From there you can use the AWS CLI as normal, making sure that you specify the profile:

Ex:
aws --profile 1234567890:s3access s3 ls


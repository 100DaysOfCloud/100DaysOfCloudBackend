100daysofcloud profile backend:
- dynamodb table "profiles" for registering profiles with GitHub OAUTH


### Database
#### Access pattern
- Input form for each days' entries from participants
- Leaderboard up-to-date entries (LEADERB#1...)
- 

### Users Table
- 
  AttributeName: "twitter_username"
  AttributeType: "S"
- 
  AttributeName: "linkedin_profile"
  AttributeType: "S"
- 
  AttributeName: "full_name"
  AttributeType: "S"
- 
  AttributeName: "bio"
  AttributeType: "S"
- 
  AttributeName: "status"
  AttributeType: "S"
- 
  AttributeName: "last_entry_at"
  AttributeType: "S"
- 
  AttributeName: "days_completed"
  AttributeType: "N"
- 
  AttributeName: "twitter_score"
  AttributeType: "N"
- 
  AttributeName: "github_score"
  AttributeType: "N"
- 
  AttributeName: "twitter_streak"
  AttributeType: "N"
- 
  AttributeName: "github_streak"
  AttributeType: "N"

- input form on the frontend goes into the dynamodb profiles table
	- github username (maybe this as primary key)
	- twitter username
	- linkedin
	- entry number (10/100)

	- full_name - The name we will display on the website
	- github_name - Their github handle so we can see if they have the 100DaysOfCloud repo
	- twitter_name - Their twitter handle so we can check if they have been tweeting progress
	- github_entry_count - the number github enteries completed (increment updates)
	- twitter_entry_count - the number of twitter enterprise completed
	- status - active, inactive, completed
	- last_entry_at - when the last entry occured

- second table for commit submissions from the form
	- github_name - how we can indentify who this record belongs to
	- entry_type - Either Github or Twitter
	- url - Link to Twitter post or Link to Github post
	- day - What day out of 100 this entry counts for
	- verified - true or false (default to false, can use 0 or 1) If our system has checked the entry
	- confidence - this is score from 0 to 100 of the quality of the entry
	- created_at - The first time this record was created
	- updated_at - If the user has updated this entry

#### IAM Permissions request from Boyko 21.07.2020
Serverless
- Everything will be deployed via SAM. This means that some of the resources should be name "100DaysOfCloud-*" automatically.
- I will have SAM assume a role for deployment - that can have much more than my access. I just need to be able to deploy and update it.

Serverless stack permissions and used services
- I believe SAM needs CodePipeline or CodeDeploy permissions as it transforms the CF template
- CloudFormation (stack named 100DaysOfCloud-*)
- S3 (same name) - create bucket, handle objects in the bucket, CORS+bucket policy
- CloudFront (same name likely) - create distribution, create OAI, modify distribution etc
- Lambda (same name likely)
- IAM - SAM creates a role for itself, Lambda roles etc
- DynamoDB (same name) - create table and put/read from table for myself + the Lambda roles which I'll create


## Authenticate CLI with MFA
aws sts get-session-token --serial-number arn:aws:iam::525128325639:mfa/Chris --profile chris@100daysofcloud --token-code code

[mfa]
aws_access_key_id = example-access-key-as-in-returned-output
aws_secret_access_key = example-secret-access-key-as-in-returned-output
aws_session_token = example-session-Token-as-in-returned-output


## GitHub
…or create a new repository on the command line
---
echo "# dfdadaf" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/what-name/dfdadaf.git
git push -u origin master
                

…or push an existing repository from the command line
---
git remote add origin https://github.com/what-name/dfdadaf.git
git push -u origin master
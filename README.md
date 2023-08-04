# Automating-backup-Boto3
AWS lambda function in python using AWS SDK Boto3 for deleting the AMI of multiple EC2 instances created over multiple region running everyday for taking back. the condition is, we have identify the AMIs created uptill 15th and 30th day of each month, and delete all but the latest 7 AMIs for each instance.

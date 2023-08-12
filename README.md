# Automating-backup-Boto3

- Python script using AWS Boto3 SDK for automating creation and deletion of AMI and snapshots, deleting all the backups except the latest 7.
      -- the script will run on a daily basis and take a Backup of that day for the mentioned Instance.
      -- it will traverse through all the AMI created from the mentioned Instances in all the mention regions and look for the "DeleteOn" tag, if the date mentioned in the value of the tag matches with the date on which this script is running, it will delete that AMI.

---------------------------------------------------------------------------------------------------------------------

#### Instance created with DeleteOn Tag :
![Instance Created with DeleteOn Tag](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/instance-created-with-DeleteOn-tag.png)

---------------------------------------------------------------------------------------------------------------------

#### Role Attached with the Lambda Function :
![Role Attached with the Lambda Function](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/role-attached.png)

----------------------------------------------------------------------------------------------------------------------

#### Environment Variable :
![Environment Variable](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/env_variables.png)

-----------------------------------------------------------------------------------------------------------------------

#### EventBridge Rule :
![EventBridge Rule](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/eventbridge-rule.png)

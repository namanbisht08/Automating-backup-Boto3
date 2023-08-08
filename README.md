# Automating-backup-Boto3
- Python script using AWS Boto3 SDK for automating creation and deletion of AMI and snapshots, deleting all the backups except latest 7.<br> 
      -- the script will run on daily basis and take Backup of that day for the mentioned Instance.<br>
      -- it will traverse through all the AMI created from the mentioned Instances in all the mention region and look for the "DeleteOn" tag, if the date mention in the value of the tag matches with date on which this script is running, it will delete that AMI.<br>

---------------------------------------------------------------------------------------------------------------------
#### Instance created with DeleteOn Tag :
![Alt text](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/instance-created-with-DeleteOn-tag.png "Optional title")

---------------------------------------------------------------------------------------------------------------------
#### Role Attached with the Lambda Function :
![Alt text](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/role-attached.png "Optional title")

----------------------------------------------------------------------------------------------------------------------
#### Environment Varibale :
![Alt text](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/env_variables.png "Optional title")

-----------------------------------------------------------------------------------------------------------------------

#### EventBridge Rule :
![Alt text](https://github.com/namanbisht08/Automating-backup-Boto3/blob/main/screenshort/eventbridge-rule.png "Optional title")

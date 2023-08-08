# Automating-backup-Boto3
- Python script using AWS Boto3 SDK for automating creation and deletion of AMI and snapshots, deleting all the backups except latest 7.<br> 
      -- the script will run on daily basis and take Backup of that day for the mentioned Instance.<br>
      -- it will traverse through all the AMI created from the mentioned Instances in all the mention region and look for the "DeleteOn" tag, if the date mention in the value of the tag matches with date on which this script is running, it will delete that AMI.<br>

---------------------------------------------------------------------------------------------------------------------
![Alt text](/screenshort/instance-created-with-DeleteOn-tag.png?raw=true "Optional Title")


import boto3
import datetime
import os

def delete_ami(ec2_client, name, date, delToday):
    try:
        describeImages = ec2_client.describe_images(Filters=[{'Name': 'tag:Name', 'Values': ['AMIBackup-' + name + "-" + delToday]}])['Images']

        for image in describeImages:
            imageId = image['ImageId']

            if 'BlockDeviceMappings' not in image:
                print(f"BlockDeviceMappings not found for AMI {imageId}")
                continue

            snapList = []
            for mapping in image['BlockDeviceMappings']:
                if 'Ebs' in mapping and 'SnapshotId' in mapping['Ebs']:
                    snapList.append(mapping['Ebs']['SnapshotId'])


            tagDelDate = None  # Default value for tagDelDate
            for tag in image['Tags']:
                try:
                    if tag['Key'] == 'DeleteOn':
                        tagDelDate = tag['Value']
                        
                except Exception as e:
                    print('Tag Errors: ', e)

            if tagDelDate == date :
                dereg_img = ec2_client.deregister_image(ImageId=imageId)

                for snapId in snapList:
                    del_snap = ec2_client.delete_snapshot(SnapshotId=snapId)
            else:
                print('Image cannot be deleted: ', imageId)

    except Exception as e:
        print('Image Deletion Errors: ', e)


def lambda_handler(event, context):
    try:
        server_dictionary = {
                                os.environ['REGION1'] : [os.environ['test1'], os.environ['test2'], os.environ['test3'], os.environ['test4'], os.environ['test5'], os.environ['test6'], os.environ['test7'], os.environ['test8'], os.environ['test9'], os.environ['test10']], 
                                os.environ['REGION2'] : [os.environ['INSTANCE3'], os.environ['INSTANCE4']]
                            }
        
        currentDT = datetime.datetime.now()
        date = currentDT.strftime("%d-%m-%Y")   #date toay
        delDate = currentDT + datetime.timedelta(days=7)
        delDate = delDate.strftime("%d-%m-%Y")  #deletion date, for mentioning on the tag (toady's date + 7)
        delToday = (currentDT - datetime.timedelta(days=7)).strftime("%d-%m-%Y") #instance deleting today, used in describe_images in delete_ami function (today's date -7)
        
        

        for region in list(server_dictionary.keys()):
            ec2_client = boto3.client('ec2', region_name=region)

            response = ec2_client.describe_instances(InstanceIds= server_dictionary[region])  
            for instance in response['Reservations']:
                for i in instance['Instances']:
                    try:
                        tagList = i.get('Tags', '')
                        
                        for tag in tagList:
                            if tag.get('Key', '') == 'Name':
                                name = tag.get('Value', '')
                                delete_ami(ec2_client, name, date, delToday)
                                break

                        createImage = ec2_client.create_image(InstanceId=i.get('InstanceId', ''),
                                                              Name="Lambda - " + i.get('InstanceId', '') + " from " + date + "(7 Days Backup)",
                                                              Description="Lambda created AMI of instance " + i.get('InstanceId', '') + " from " + date,
                                                              NoReboot=True, DryRun=False)

                        createTags = ec2_client.create_tags(Resources=[createImage.get('ImageId', '')],
                                                            Tags=[{'Key': 'Name', 'Value': 'AMIBackup-' + name +"-"+date},
                                                                  {'Key': 'DeleteOn', 'Value': delDate}])


                    except Exception as e:
                        print('Image Creation Errors: ', e)

        print('All regions and instances processed.')

    except Exception as e:
        print('Errors: ', e)


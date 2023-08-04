import boto3
import datetime
import os

def delete_ami(ec2_client, name, date):
    try:
        describeImages = ec2_client.describe_images(Filters=[{'Name': 'tag:Name', 'Values': ['AMIBackup-' + name]}])['Images']
        print(describeImages)

        for image in describeImages:
            imageId = image['ImageId']
            print("imageId --->" + imageId)

            if 'BlockDeviceMappings' not in image:
                print(f"BlockDeviceMappings not found for AMI {imageId}")
                continue

            snapList = []
            for mapping in image['BlockDeviceMappings']:
                if 'Ebs' in mapping and 'SnapshotId' in mapping['Ebs']:
                    snapList.append(mapping['Ebs']['SnapshotId'])

            print(snapList)

            tagDelDate = None  # Default value for tagDelDate
            for tag in image['Tags']:
                try:
                    if tag['Key'] == 'DeleteOn':
                        tagDelDate = tag['Value']
                        print("tagDelDate --->" + tagDelDate)
                except Exception as e:
                    print('Tag Errors: ', e)

            if tagDelDate == date:
                print('Deregistering image ---> ', imageId)
                dereg_img = ec2_client.deregister_image(ImageId=imageId)

                for snapId in snapList:
                    print('Deleting Snapshot: ', snapId)
                    del_snap = ec2_client.delete_snapshot(SnapshotId=snapId)
            else:
                print('Image cannot be deleted: ', imageId)

    except Exception as e:
        print('Image Deletion Errors: ', e)


def lambda_handler(event, context):
    try:
        # instanceList = [os.environ['INSTANCE1'], os.environ['INSTANCE2'], os.environ['INSTANCE3'], os.environ['INSTANCE4']] 
        # regions = [os.environ['REGION1'], os.environ['REGION2']]

        server_dictionary = {
                                os.environ['REGION1'] : [os.environ['INSTANCE1'], os.environ['INSTANCE2']], 
                                os.environ['REGION2'] : [os.environ['INSTANCE3'], os.environ['INSTANCE4']]
                            }
        
        
        currentDT = datetime.datetime.now()
        date = currentDT.strftime("%d-%m-%Y")
        delDate = currentDT + datetime.timedelta(days=2)
        delDate = delDate.strftime("%d-%m-%Y")

        for region in list(server_dictionary.keys()):
            print(f"Processing region: {region}")
            ec2_client = boto3.client('ec2', region_name=region)

            response = ec2_client.describe_instances(InstanceIds= server_dictionary[region])  
            print(response)
            for instance in response['Reservations']:
                for i in instance['Instances']:
                    try:
                        tagList = i.get('Tags', '')

                        for tag in tagList:
                            if tag.get('Key', '') == 'Name':
                                name = tag.get('Value', '')
                                delete_ami(ec2_client, name, date)
                                break

                        createImage = ec2_client.create_image(InstanceId=i.get('InstanceId', ''),
                                                              Name="Lambda - " + i.get('InstanceId', '') + " from " + date + "(2 Days Backup)",
                                                              Description="Lambda created AMI of instance " + i.get('InstanceId', '') + " from " + date,
                                                              NoReboot=True, DryRun=False)

                        createTags = ec2_client.create_tags(Resources=[createImage.get('ImageId', '')],
                                                            Tags=[{'Key': 'Name', 'Value': 'AMIBackup-' + name},
                                                                  {'Key': 'DeleteOn', 'Value': delDate}])

                        print('Image Created: ', createImage)

                    except Exception as e:
                        print('Image Creation Errors: ', e)

        print('All regions and instances processed.')

    except Exception as e:
        print('Errors: ', e)

lambda_handler(None, None)  # Invoke the lambda function (This is only for local testing)

##
# @author Graham Schmidt
# Title: Infor Sample Challenge: Junior
# Purpose: iterate through all Regions and list Stopped ec2 instances
##

# Retrieve all regions
# Iterate through all regions, list every instance in each region

import json, boto3

def lambda_handler(event, context):
    # Retrieve keys from event
    ACCESSKEY = event.get('access_key')
    SECRETKEY = event.get('secret_key')

    ec2 = boto3.client('ec2', aws_access_key_id=ACCESSKEY, aws_secret_access_key=SECRETKEY)
    regions = ec2.describe_regions()

    # Isolate list of regions
    regionDictList = regions['Regions']
    print("## Regions accessed")
    regionList = []
    for dict in regionDictList:
        regionList.append(dict['RegionName'])
    print("## Region list built")

    # Loop through regions, print associated Instances (Running and Stopped)
    for r in regionList:
        resource = boto3.resource('ec2', aws_access_key_id=ACCESSKEY, aws_secret_access_key=SECRETKEY)
        instances = resource.instances.filter()
        print("## " + r + " instances loaded")
        print("## Looping through instances in region: " + r)
        for instance in instances:
            # Option 'running' line, can be removed
            if instance.state["Name"] == "running" and r in instance.placement['AvailabilityZone']:
                print("Running: ", instance.id, instance.instance_type)
            elif instance.state["Name"] == "stopped" and r in instance.placement['AvailabilityZone']:
                print("Stopped: ", instance.id, instance.instance_type)
            else:
                print("No instances associated with " + r)

    return {
            'statusCode': 200,
            'message':'Success!'}

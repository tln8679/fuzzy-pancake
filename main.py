#!/usr/bin/env python3
import boto3
from botocore.exceptions import ClientError, BotoCoreError 


def main():
    # init values
    ec2 = boto3.resource('ec2')
    client = client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    
    print ("Choose the running instance you want to restore (copy and paste the instance ID): ")
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    # Counter's purpose is for print formatting only
    running_counter = 1
    for instance in instances:
        # Grab the name of the instance
        for tags in instance.tags:
            if tags["Key"] == 'Name':
                instance_name = tags["Value"]
        print(str(running_counter)+")")
        print("Instance ID: " + instance.id + "\nInstance name: " + instance_name + "\nroot_device_name: " + instance.root_device_name+"\n")
        running_counter+=1
    
    # Get selected instance from the user
    instance_id = input("Paste your instance ID: ")
    instance = ec2.Instance(instance_id.strip())
    try:
        # This line will call DescribeInstance and raise an error if the user put in an incorrect instance ID
        for tags in instance.tags:
            if tags["Key"] == 'Name':
                instance_name = tags["Value"]
        print("You have chosen your instance named: " + instance_name)
    except ClientError as e:
        print("You entered an invalid instance ID. Try again.")
        print(e)
        return None
    
    # Display volumes on that instance
    volumes = instance.volumes.all()
    print ("\nVolumes attached to " +  instance.id + ": ")
    for v in volumes: 
        print(v.id)

    # Ask user to confirm they want to proceed
    decision = input("Do you want to detach these volumes (YES/NO)?\n").strip()
    while decision != "YES" and decision != "NO":
        decision = input("Invalid input. Enter \"YES\" or \"NO\"\n").strip()
    if decision == "NO": 
        print("Exiting script....")
        exit()
    elif decision == "YES": 
        print("Now stopping instance...")
    
    # Stop the instance and print the JSON response
    response = instance.stop(
        Force=False
    )
    print (response)
    
    # We cannot proceed until the instance has fully stopped
    print("Waiting for instance to stop (this may take a few minutes)...")
    instance.wait_until_stopped()
    # TODO: Detach volume(s)
    print("Now detaching volumes...")
    snaps_needed = 0
    for v in volumes: 
        snaps_needed += 1
        response = instance.detach_volume(
            Force=False,
            VolumeId=v.id,
        )
        print(response)
    # TODO: Create volume from snapshot(s)
    print("You need to select: " + str(snaps_needed) +" snapshots")
    # All snapshots created from the associated volume(s) we just detached
    # TODO: Replace each detached volume with only volumes created from viable snapshots,
    #       where a viable snapshot is a snpashot that was taken from the exact volume that was detached.
    #       OpenEMR 5.01 has two devices attached so we want to make sure only the correct snapshots are used for each volume 
    s_iterator = ec2.snapshots.filter(
        OwnerIds=[
            account_id,
        ],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [
                    # This hardcode will be replaced by a volume id in a for loop
                    'vol-0c3ea35f83b72a0dc',
                ]
            },
        ],
    ) 
    for s in s_iterator: print(s.id)

    # TODO: Attach volume(s)
    # If > 1 volumes ask user to confirm which one is the root device (sda1)

    # TODO: Start instance

if __name__ == "__main__": main()
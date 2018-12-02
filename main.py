#!/usr/bin/env python3
import boto3   

def main():
    ec2 = boto3.resource('ec2')

    print ("Choose the running instance you want to restore (copy and paste the instance ID): ")
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print("Instance ID: " + instance.id, "Instance name: " + instance.key_name, "root_device_name" + instance.root_device_name)
    
    # Get selected instance from the user
    instance_id = input("\nPaste your instance ID: ")
    instance = ec2.Instance(instance_id.strip())
    
    # Display volumes on that instance
    volumes = instance.volumes.all()
    print ("\nVolumes attached to " +  instance.id + ": ")
    for v in volumes: print(v)

    decision = input("Do you want to detach these volumes (YES/NO)?").strip
    while decision is not "YES" or decision is not "NO":
        decision = input("Invalid input. Enter \"YES\" or \"NO\"").strip()
    if decision is "NO": 
        print("Exiting script....")
        exit()
    elif decision is "YES": 
        print("Displaying snapshots of your instance: ")

    # TODO: Stop instance
    # TODO: Detach volume(s)
    # TODO: Create volume from snapshot(s)
    # TODO: Attach volume(s)
    # TODO: Start instance

if __name__ == "__main__": main()

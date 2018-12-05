# fuzzy-pancake
EC2 instance volume swap using Boto3 (AWS python SDK).

#### If you create snapshots of your EC2 instance (and you should be), you can use this tool to easily recover from a disaster
- There are a few different ways to set your AWS credentials for boto. (https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html). I chose to install the aws cli (https://docs.aws.amazon.com/cli/latest/userguide/installing.html) and run the 'aws configure' command.
- Check out https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html for snapshot lifecycle management
- With this command line tool, you can select the instance you want to restore, select the snapshot you wan to restore from, and let the program take care of the rest.


import boto3

ec2 = boto3.client("ec2")

# try...except will catch any errors that occur during creation process
try:
    # creates new ec2 instance
    result = ec2.run_instances(
        ImageId= "ami-0f403e3180720dd7e",# AMI for a basic linux machine
        InstanceType= "t2.micro",
        MaxCount=1,# creates 1 instance
        MinCount=1,
        KeyName = "vockey"
        # security group not specified, default used
    )
    print(result)# outputs response of creation process
except:
    # outputs error message
    print("Failed to create ec2 Instance.")
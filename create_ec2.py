import boto3

ec2 = boto3.client("ec2")
print(ec2.run_instances(
    ImageId= "ami-0f403e3180720dd7e",
    InstanceType= "t2.micro",
    MaxCount=1,
    MinCount=1,
    KeyName = "vockey"
))
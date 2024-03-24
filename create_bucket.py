import boto3

s3 = boto3.client("s3")
print(s3.create_bucket(Bucket="mybuckets2225362"))
import boto3

s3 = boto3.client("s3")

# try...except will catch any errors that occur during creation process
try:
    # creates new bucket and outputs response
    print(s3.create_bucket(Bucket="mybuckets2225362"))
except:
    # outputs error message
    print("Something went wrong, bucket creation failed.")
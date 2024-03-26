# Author: Logan Mclachlan, s2225362
# Last Updated: 26/3/2024

# This script will fetch an image from a SQS event,
# use rekognition to analyse the image, then create
# a new record of the resutl on a dynamoDB table.

import json
import boto3

# set up boto clients to access aws components
rekognition = boto3.client('rekognition')
s3 = boto3.client("s3")
db = boto3.client("dynamodb")

def lambda_handler(event, context):
    image = get_image(event)
    result = analyse_image(image,"mybuckets2225362")

    return {
        'statusCode': 200,
        'body': json.dumps('Image analysis complete.')
    }

# gets image title from sqs event
def get_image(event):
    try:
        # gets most recent image
        file_obj = json.loads(event["Records"][0]["body"])# converts str body to json object
        # gets image title
        image = file_obj["Records"][0]["s3"]["object"]["key"]
        return image
    except:
        print("Failed to get image.")

# sends image to be analysed, returns results
def analyse_image(image,bucket):
    try:
        # gives recognition service image name and specified attributes to be returned
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},
            Attributes=["EMOTIONS"])
        return format_result(response)
    except:
        print("Failed to analyse image.")

# extracts important info into readable object
def format_result(result):
    formatted = result
    print(formatted)
    return formatted

# records record of result to dynamoDB
def record_result(result):
    print("Result recorded.")
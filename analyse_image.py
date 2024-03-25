import json
import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client("s3")

def lambda_handler(event, context):
    image = get_image(event)
    result = analyse_image(image,"mybuckets2225362")

    return {
        'statusCode': 200,
        'body': json.dumps('Checking image...')
    }

# gets image title from sqs event
def get_image(event):
    try:
        # gets most recent image
        file_obj = json.loads(event["Records"][0]["body"])# converts str body to json onject
        # gets image title
        image = file_obj["Records"][0]["s3"]["object"]["key"]
        return image
    except:
        print("Failed to get image.")

# sends image to be analysed, returns results
def analyse_image(image,bucket):
    try:
        # gives recognition service image name and specified attributes to be returned
        response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': image}})
        print(response)
        return response
    except:
        print("Failed to analyse image.")

# records record of result to dynamoDB
def record_result(result):
    print("Result recorded.")
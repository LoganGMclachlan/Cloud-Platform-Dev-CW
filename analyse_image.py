# Author: Logan Mclachlan, s2225362
# Last Updated: 26/3/2024

# This script will fetch an image from a SQS event,
# use rekognition to analyse the image, then create
# a new record of the result on a dynamoDB table.

import json
import boto3

# set up boto clients to access aws components
rekognition = boto3.client('rekognition')
s3 = boto3.client("s3")
db = boto3.client("dynamodb")

# handles the event trigger
def lambda_handler(event, context):
    result = analyse_image(get_image(event))
    record_result(result)
    print(result)

    return {
        'statusCode': 200,
        'body': json.dumps('Image analysis complete.')
    }

# gets image title from sqs event
def get_image(event):
    try:
        # gets most recent image
        image = json.loads(event["Records"][0]["body"])# converts str body to json object
        # returns image title/key
        return image["Records"][0]["s3"]["object"]["key"]
    except:
        print("Failed to get image.")

# sends image to be analysed, returns results
def analyse_image(image):
    try:
        # gives recognition service image name and specified attributes to be returned
        result = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': "mybuckets2225362", 'Name': image}},
            Attributes=["EMOTIONS"])
        return format_result(result,image)
    except:
        print("Failed to analyse image.")

# extracts important info into readable object
def format_result(result,image):
    formatted = {"Image":image,"Faces":[]}
    # loops through every face detected
    for face in result["FaceDetails"]:
        # sets most confidant emotion to first option
        most_confident = face["Emotions"][0]
        # loops through emotion options
        for emotion in face["Emotions"]:
            # checks for most confidant emotion
            if (emotion["Confidence"] > most_confident["Confidence"]):
                most_confident = emotion
        # adds most confidant emotion for a face to formatted list
        formatted["Faces"].append(most_confident)
    # final data structure example:
    # {"Image":"image1","Faces":[{"Type":"HAPPY","Confidance":98.04},{"Type":"SAD","Confidance":94.23}]}
    return formatted

# records record of result to dynamoDB
def record_result(result):
    print("Result recorded.")
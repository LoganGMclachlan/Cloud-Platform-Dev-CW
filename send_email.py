# Author: Logan Mclachlan, s2225362
# Last Updated: 27/3/2024

# When a new table entry is made, check if 
# any angry or frustrated faces are detected
# and send email if so.

import json
import boto3

sns = boto3.client("sns")

# handles the event trigger
def lambda_handler(event, context):
    for record in event["Records"]:
        # only checks insert type events
        if(record["eventName"] == "INSERT"):
            # gets image data from record
            image = record["dynamodb"]["NewImage"]
            key = record["dynamodb"]["Keys"]["PrimaryKey"]["S"]
            print("Checking " + key + "...")
            
            # checks for angry or frustrated emotion data
            check_emotion("Angry",image,key)
            check_emotion("Frustrated",image,key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('New item checked.')
    }

def check_emotion(emotion,image,key):
    # checks for face data
    confidences = image[emotion]["S"].split(", ")
    for value in confidences:
        # sends email if confidence reaches 10%
        if(value != "" and float(value) >= 10):
            send_email(emotion,value,key)

# sends and email to SNS topic
def send_email(emotion,value,image):
    message = "ALERT! " + emotion + " face detected in image " + image
    print(message)
    try:
        sns.publish(TopicArn="arn:aws:sns:us-east-1:891377312372:MyTopics2225362",
            Message=message,
            Subject=message)
        print("Email sent.")
    except:
        print("Failed to send email.")
# Author: Logan Mclachlan, s2225362
# Last Updated: 27/3/2024

# When a new table entry is made, check if 
# any angry or frustrated faces are detected
# and send email if so.

import json

# handles the event trigger
def lambda_handler(event, context):
    for record in event["Records"]:
        # only checks insert type events
        if(record["eventName"] == "INSERT"):
            # checks for angry face data
            anger_confidences = record["dynamodb"]["NewImage"]["Angry"]["S"].split(", ")
            for value in anger_confidences:
                if(value != "" and float(value) >= 10):
                    send_email(anger_confidences)
                    
            # checks for frustrated face data
            frustrated_confidences = record["dynamodb"]["NewImage"]["Frustrated"]["S"].split(", ")
            for value in frustrated_confidences:
                if(value != "" and float(value) >= 10):
                    send_email(frustrated_confidences)
    
    return {
        'statusCode': 200,
        'body': json.dumps('New item checked.')
    }

def send_email(image):
    print("Angry face detected in image")
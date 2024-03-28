# Author: Logan Mclachlan, s2225362
# Last Updated: 27/3/2024

# This script will fetch an image from a SQS event,
# use rekognition to analyse the image, then create
# a new record of the result on a dynamoDB table.

import json
import boto3

# set up boto clients to access aws components
rekognition = boto3.client('rekognition')
s3 = boto3.client("s3")
db = boto3.resource("dynamodb")

# handles the event trigger
def lambda_handler(event, context):
    result = analyse_image(get_image(event))
    print(result)
    record_result(result)

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
    formatted = {"Image":image,"Emotions":[]}
    # loops through every face detected
    for face in result["FaceDetails"]:
        # extracts first 5 emotions for each face
        formatted["Emotions"].append(face["Emotions"][:5])
    return formatted

# records record of result to dynamoDB
def record_result(result):
    records = db.Table('MyDynamoDBTemplateS2225362-myDynamoDBTable-IHDW0QM0JDRR')
    records.put_item(Item={
        # key saved as image name
        "PrimaryKey":result["Image"],
        "No. of Faces":len(result["Emotions"]),
        # gets confidence levels for all emotions
        "Happy": check_emotion("HAPPY",result),
        "Sad": check_emotion("SAD",result),
        "Angry": check_emotion("ANGRY",result),
        "Surpirsed": check_emotion("SURPRISED",result),
        "Frustrated": check_emotion("FRUSTRATED",result),
        "Disgusted": check_emotion("DISGUSTED",result),
        "Calm": check_emotion("CALM",result),
        "Confused": check_emotion("CONFUSED",result)}
    )
    print("Result recorded.")

# returns all confidance levels of a target emotion within a set of results
def check_emotion(target,result):
    values = ""
    for face in result["Emotions"]:# loops for each face detected
        for emotion in face:# loops for all emotion responses
            if(emotion["Type"] == target):
                values += str(round(emotion["Confidence"],4)) + ", "
                break# exits 2nd loop if emotion is found
    return values
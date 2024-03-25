import json
import boto3

client = boto3.client('rekognition')

def lambda_handler(event, context):
    result = analyse_image("mybuckets2225362")

    return {
        'statusCode': 200,
        'body': json.dumps('Checking image...')
    }

# send image to be analysed, returns results
def analyse_image(bucket):
    images = ["image5","image4","image3","Image2","image1"]
    # loops through images in reverse order of upload
    for image in images:
        # if image referance before it is uploaded, try will catch error
        try:
            # tries until most recently uploaded is found
            response = client.detect_faces(
                Image={'S3Object': {'Bucket': bucket, 'Name': image}},
                Attributes=["EMOTIONS","GENDER"])
            print(response)
            return response
        except:
            pass

# records record of result to dynamoDB
def record_result(result):
    print("Result recorded.")
    return null
import json

def lambda_handler(event, context):
    print("context: " + context)
    print("event: " + event)
    return {
        'statusCode': 200,
        'body': json.dumps('Checking image...')
    }

# gets the most recent image uploaded to s3 b ucket, returns image
def get_image():
    print("Getting recent image...")
    return null
    
# send image to be analysed, returns results
def analyse_image(image):
    print("Analysing image: " + image)
    return null
    
# records record of result to dynamoDB
def record_result(result):
    print("Result recorded.")
    return null
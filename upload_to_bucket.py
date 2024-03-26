# Author: Logan Mclachlan, s2225362
# Last Updated: 20/3/2024

# This script will upload 5 images from an ec2
# instance to an s3 bucket. Each image is uploaded
# 10 seconds appart.

import boto3
import time

bucket = boto3.client("s3")
# defines image file names
images = ["image1","Image2","image3","image4","image5"]

# try...except will catch any errors that occur during upload process
try:
    print("Uploading images...")
    for image in images:
        path = "./cloud_images/"+image+".jpg"# concats file path to image name
        bucket.upload_file(path, "mybuckets2225362", image)
        print(image + " uploaded to bucket.")
        if(image != "image5"):
            time.sleep(10)# 10 second delay
    print("Image upload complete!")
except:
    # outputs error message
    print("Something went wrong, process stopped.")
import boto3
import time

bucket = boto3.client("s3")
# defines image file names
images = ["image1","Image2","image3","image4","image5"]

# try...except will catch any errors that occur during upload process
try:
    for image in images:
        path = "./cloud_images/"+image+".jpg"# concats file path to image name
        bucket.upload_file(path, "mybuckets2225362", image)
        print(image + " uploaded to bucket")
        time.sleep(10)# 10 second delay
    print("Image upload complete!")
except:
    print("Something went wrong, process stopped.")
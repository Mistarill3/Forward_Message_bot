import json
import urllib.parse
import urllib.request
import urllib.error
import boto3
import botocore


s3 = boto3.resource("xxx")
bucket = s3.Bucket("yyy")


def downloadAndReadFile(fileName):
    print("==startS3FileOperation.DownloadAndReadFile")
    downloadedFileName = "downloadedFile.txt"
    
    try:
        bucket.download_file(fileName, "/tmp/"+downloadedFileName)
        print("==toBeDownloadedFile")
        print(fileName)
        
    except botocore.exceptions.ClientError as e:
        print("==except")        
        print(e.response["Error"])
        if e.response["Error"]["Code"] == "404":
            print("fileNotFound")
            return
        elif e.response["Error"]["Code"] == "400":
            print("Bad Request")
            return
        else:
            raise e

    with open("/tmp/" + downloadedFileName, mode="r") as f:
        fileContents = f.read()
        print("==openFileContentsInReadMode")
        print("==endS3FileOperation.DownloadAndReadFile")
        return fileContents



def writeAndUploadFile(newFileContents, fileName):
    print("==startS3FileOperation.WriteAndUploadFile")

    with open("/tmp/test.txt", mode="w") as f:
        f.write(str(newFileContents))
    bucket.upload_file("/tmp/test.txt", fileName)
    print("==newFileContentsWritten")

    print("==endS3FileOperation.WriteAndUploadFile")

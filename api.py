import boto3
from botocore.errorfactory import ClientError
from typing import Union
from fastapi import FastAPI
import urllib.parse
import os

endpoint_url = "https://s3.wasabisys.com" #change if needed
s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=os.environ["S3_ACCESS"], aws_secret_access_key=os.environ["S3_SECRET"])
BucketName = "repov2"
cdn_endpoint = "https://repo.cdn.trolling.solutions/" #change if needed
app = FastAPI()




@app.get("/files/getFolders")
def getFolders():
    query = listFolders()
    return {"Folders": query}
    #['Key'], "Size": query['Contents']['Size']}

@app.get("/files/getFolderContent")
def getFolderContent(q: str, continuationToken=None):
    content = folderContentQuery(q, continuationToken)
    if content == 0:
        return {"Error": "Invalid folder name"}

    return {"content": content}
        


# returns the first 250 files and subdirectories within a given subdirectory.
def folderContentQuery(folderName: str, continuationToken=None):
    queryList = []
    coord = (len(folderName) - 1)
    if (folderName[coord:] != "/"):
        return 0
    if (continuationToken == None):
        results = s3.list_objects_v2(Bucket=BucketName, MaxKeys=250, Prefix=folderName)
    else:
        results = s3.list_objects_v2(Bucket=BucketName, MaxKeys=250, Prefix=folderName, ContinuationToken=continuationToken)
    del results["ResponseMetadata"]
    del results["Name"]
    del results["Prefix"]
    del results["MaxKeys"]
    del results["KeyCount"]
    del results["EncodingType"]
    for i in range(len(results["Contents"])):
        del results["Contents"][i]["ETag"]
        del results["Contents"][i]["StorageClass"]
        results["Contents"][i]["URL"] = urllib.parse.quote(cdn_endpoint + results["Contents"][i]["Key"])

    return results
        
    
    

def listFolders(numQuery=1000):
    queryList = []
    results = s3.list_objects_v2(Bucket=BucketName, MaxKeys=numQuery)
    for i in range(len(results['Contents'])):
        coord = (len(results['Contents'][i - 1]['Key']) - 1)
        checkLetter = results['Contents'][i- 1]['Key'][coord:]
        if (checkLetter == "/"):
            queryList.append(results['Contents'][i - 1])  
        else:
            pass
    for i in range(len(queryList)):
        del queryList[i]["ETag"]
        del queryList[i]["StorageClass"]
        del queryList[i]["Size"]
        queryList[i]["URL"] = urllib.parse.quote(cdn_endpoint + queryList[i]["Key"])
    return queryList
    


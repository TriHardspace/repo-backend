import boto3
from botocore.errorfactory import ClientError
from typing import Union
import urllib.parse
import os


class s3_queries:
    def __init__(self, endpointURL="https://s3.wasabisys.com", cdnEndpoint="https://repo.cdn.trolling.solutions/", bucketName="repov2"):
        self.s3 = boto3.client('s3', endpoint_url=endpointURL, aws_access_key_id=os.environ["S3_ACCESS"], aws_secret_access_key=os.environ["S3_SECRET"])
        self.endpointURL = endpointURL
        self.bucketName = bucketName
        self.cdnEndpoint = cdnEndpoint
        

    #def listFolders(self):
    #    queryList = []
    #    results = self.s3.list_objects_v2(Bucket=self.bucketName, MaxKeys=1000, Prefix="Combat")
    #    for i in range(len(results['Contents'])):
    #        coord = (len(results['Contents'][i - 1]['Key']) - 1)
    #        checkLetter = results['Contents'][i- 1]['Key'][coord:]
    #        print(results['Contents'][i- 1]['Key'])
    #    if (checkLetter == "/"):
    #        queryList.append(results['Contents'][i - 1])  
    #        print(results['Contents'][i - 1])

    #    else:
    #        pass
    #    for i in range(len(queryList)):
    #        del queryList[i]["ETag"]
    #        del queryList[i]["StorageClass"]
    #        del queryList[i]["Size"]
    #        queryList[i]["URL"] = urllib.parse.quote(self.cdnEndpoint + queryList[i]["Key"])
    #    return queryList
    

    def listFolders(self):
        queryList = []
        returnList = []
        is_Truncated = True
        continuationToken = ""
        while (is_Truncated):
            results = self.s3.list_objects_v2(Bucket=self.bucketName, MaxKeys=1000, ContinuationToken=continuationToken)
            queryList.append(results)
            isTruncated = results["IsTruncated"]
            if (isTruncated == True):
                continuationToken = results["NextContinuationToken"]
                print("e")
            else: 
                break
        for i in range(len(queryList['Contents'])):
            coord = (len(queryList['Contents'][i - 1]['Key']) - 1)
            checkLetter = queryList['Contents'][i- 1]['Key'][coord:]
            print(queryList['Contents'][i- 1]['Key'])
            if (checkLetter == "/"):
                returnList.append(results['Contents'][i - 1]) 
            else:
                pass
            for i in range(len(returnList)):
                del queryList[i]["ETag"]
                del queryList[i]["StorageClass"]
                del queryList[i]["Size"]
                queryList[i]["URL"] = urllib.parse.quote(self.cdnEndpoint + queryList[i]["Key"])
        return queryList    

        print(returnList)



    # returns the first 250 files and subdirectories within a given subdirectory.
    def folderContentQuery(self, folderName: str, continuationToken=None):
        queryList = []
        coord = (len(folderName) - 1)
        if (folderName[coord:] != "/"):
            return 0
        if (continuationToken == None):
            results = self.s3.list_objects_v2(Bucket=self.bucketName, MaxKeys=250, Prefix=folderName)
        else:
            results = self.s3.list_objects_v2(Bucket=self.bucketName, MaxKeys=250, Prefix=folderName, ContinuationToken=continuationToken)
        del results["ResponseMetadata"]
        del results["Prefix"]
        del results["MaxKeys"]
        del results["KeyCount"]
        del results["EncodingType"]
        for i in range(len(results["Contents"])):
            del results["Contents"][i]["ETag"]
            del results["Contents"][i]["StorageClass"]
            results["Contents"][i]["URL"] = urllib.parse.quote(self.cdnEndpoint + results["Contents"][i]["Key"])
        
        return results

        
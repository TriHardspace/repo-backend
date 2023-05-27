from fastapi import FastAPI
from s3_queries import s3_queries

app = FastAPI()
s3 = s3_queries()



@app.get("/files/getFolders")
def getFolders():
    query = s3.listFolders()
    return {"Folders": query}
    #['Key'], "Size": query['Contents']['Size']}

@app.get("/files/getFolderContent")
def getFolderContent(q: str, continuationToken=None):
    content = s3.folderContentQuery(q, continuationToken)
    if content == 0:
        return {"Error": "Invalid folder name"}

    return {"content": content}
        

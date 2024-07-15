from fastapi import FastAPI, status, Query, Body, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel
from datetime import  timedelta
from datetime import datetime
from typing import Optional
from routes.resumeDB import conn
import uvicorn
# from routes.resumeDB import conn

from parser.chatbot import ResumeBot
import random
from fastapi.middleware.cors import CORSMiddleware
from routes.resumeRoute import conn
from Session_Mangement.session import generateSessionToken, generateValidationTime, generateSessionName
# import secrets
import json
from models.filters import ResumeFilters , Education
import base64
from minio import Minio
from fastapi.responses import JSONResponse
from minioClient import client
# from boto3Client import s3_client
import requests
from parser.main_func import main
import traceback
from enum import Enum
 
class NotificationType(Enum):
    FileUpload = 1

class NotificationStatus(Enum):
    InProcess = 1
    Completed = 2
    Duplicate = 3
    CorruptError = 4

class MainNotificationStatus(Enum):
    InProcess = 1
    Resolved = 2


# url = config("SUPERBASE_URL")
# key = config("SUPERBASE_KEY")
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# supabase: Client = create_client(url, key)
class InputData(BaseModel):
    input: str

def downloadFile(filename):
    url = client.get_presigned_url(
        "GET",
        "armss-dev",
        filename,
        expires=timedelta(days=1),
    )
    # r = requests.get(url, allow_redirects=True)

    # path = f'miniodown/{filename}';

    # open(path, 'wb').write(r.content)
    
    return url


# def downloadFile(object_name):
#     """Generate a presigned URL to share an S3 object
    
#     :param bucket_name: string
#     :param object_name: string
#     :param expiration: Time in seconds for the presigned URL to remain valid (maximum 7 days)
#     :return: Presigned URL as string. If error, returns None.
#     """
#     try:
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': 'armss-dev',
#                                                             'Key': object_name},
#                                                     ExpiresIn=604800)
#     except Exception as e:
#         print(e)
#         return None

#     # The response contains the presigned URL
#     return response




def handleUpload(filename):
    url = downloadFile(filename)
    print(f'main was called, link is {url}')
    main(url, filename)

    

async def getFileNameFromFileID(file_id):
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT "FileName" FROM "Resume" where "Resume"."ResumeId"={file_id};')
        record = cursor.fetchall()
        cursor.close()
        print("records got:", record)

        return record[0][0]
        #  records
    except Exception as fetch_err:

        traceback.print_exc()
        conn.rollback() 
        print("Error fetching file id:", fetch_err)    
        return None
    



@app.get('/view-resume/')
async def resumeViewer(fileID:str):
    print(fileID)
    filename = await getFileNameFromFileID(fileID);
    print(filename)
    fileLink = downloadFile(filename)
    print(fileLink)
    return fileLink

@app.get('/view-resume_by_name/')
async def resumeViewer_byname(filename:str):
 
    print(filename)
    fileLink = downloadFile(filename)
    print(fileLink)
    return fileLink


# @app.post("/webhook")
# def fileUploaded(msg:dict):
#     print('webhook caught****************************')
#     filename = msg["Key"].split("/")[-1]
#     print(f'filename is ***********: {filename}')
#     handleUpload(filename)

@app.get("/")
async def read_root():
    return {"message": "Server is up"}

import re

def getSessionTime(notifID):
    try:
        query = 'SELECT "CreatedAt" FROM "Notification" WHERE "Id"=%s'
        cursor = conn.cursor()
        
        cursor.execute(query, (notifID,))
        createdAtTime = cursor.fetchall()[0]
        print(createdAtTime[0])  # Directly print createdAtTime
        return createdAtTime[0]
    except Exception as err:
        print(f"Error occurred: {str(err)}")
        traceback.print_exc()  # Print the full traceback for debugging purposes
    finally:
        cursor.close()  # Ensure the cursor is closed

class FileNames(BaseModel):
    file1: str
    file2: str

@app.post("/getLinkAndDateFromFileName")
async def getLinkAndDateFromFileName(files:FileNames):
    try:

        filename1 = files.file1;
        filename2 = files.file2;
        notif1 = re.search(r'\[(\d+)\]', filename1)
        notif2 = re.search(r'\[(\d+)\]', filename2)
        
        obj = {
            'filelink1':downloadFile(filename1),
            'filelink2':downloadFile(filename2),
            'filetime1': getSessionTime(notif1.group(1)),
            'filetime2': getSessionTime(notif2.group(1))
        }
        return obj;
    
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


@app.post("/presignedUrl")
async def get_presigned_url(key:InputData):
    try:
        # Generate presigned URL
        url = client.get_presigned_url(
            "PUT",
            "armss-dev",
            key.input,
            expires=timedelta(days=1),

        )
        print(url)
        return JSONResponse(content={"presignedUrl": url})
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

class NotificationRequest(BaseModel):
    fileCount: int

# @app.post("/presignedUrl")
# def get_presigned_url(key:InputData):
#     """Generate a presigned URL to upload an S3 object
    
#     :param bucket_name: string
#     :param object_name: string
#     :param expiration: Time in seconds for the presigned URL to remain valid (maximum 7 days)
#     :return: Presigned URL as string. If error, returns None.
#     """
#     try:
#         response = s3_client.generate_presigned_url('put_object',
#                                                     Params={'Bucket': 'armss-dev',
#                                                             'Key': key.input},
#                                                     ExpiresIn=604800)
#     except Exception as err:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

#     # The response contains the presigned URL
#     return response
from botocore.exceptions import NoCredentialsError
class ObjectNameRequest(BaseModel):
    object_name: str
    file_type: str



# @app.post("/presignedUrl")
# async def get_presigned_url(request: ObjectNameRequest):

#     if request.file_type is None:
#         request.file_type = 'application/octet-stream'

#     print(request.object_name)
#     # Create an S3 client
    
#     try:
#         response = s3_client.generate_presigned_post(
#             Bucket='armss-dev',
#             Key= request.object_name,
#             Fields={
#                 "Content-Type" : request.file_type
#             },
#             Conditions=[{
#                 "Content-Type" : request.file_type
#             }],
#             ExpiresIn=3600
#         )
#     except NoCredentialsError:
#         print("Credentials not available")
#         return None
    
#     return response

class uploadAbortReq(BaseModel):
    NotificationId: int
    CountOfFiles: int

@app.post('/abort-upload')
async def abort_upload(request: uploadAbortReq):
    try:
        notificationId = request.NotificationId
        fileCount = request.CountOfFiles

        json_data_str = json.dumps({
            'notification_message':'file upload notification',
            'fileCount':fileCount,
        })
        
        cursor = conn.cursor()
        query = 'UPDATE "Notification" SET "NotificationDetails"=%s WHERE "Id"=%s'
        cursor.execute(query, (json_data_str, notificationId))
        conn.commit()  # Commit the transaction
        cursor.close()
        return {"message": "Successfully Aborted Upload"}
    except Exception as e:
        traceback.print_exc()



@app.post("/create-notification")
async def create_notification(notification_request: NotificationRequest):
    fileCount = notification_request.fileCount
    try:
        cursor = conn.cursor()
        json_data_str = json.dumps({
            'notification_message':'file upload notification',
            'fileCount':fileCount,
        })
        
        # Use prepared statements to avoid SQL injection
        insert_query = '''
            INSERT INTO "Notification" ("Type", "NotificationDetails", "CreatedBy", "Status")
            VALUES (%s, %s, %s, %s) RETURNING "Id";
        '''
        cursor.execute(insert_query, (NotificationType['FileUpload'].value, json_data_str, 70, NotificatonMainStatus.UnResolved.value))
        notification_id = cursor.fetchone()[0]
        print(notification_id)
        

        
        conn.commit()  # Commit the transaction
        cursor.close()

        return {"message": "Successfully Added Notification", "notification_id": notification_id}

    except Exception as e:
        traceback.print_exc()

        if conn:
            conn.rollback()  # Rollback the transaction if an error occurs

        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
    
class NotificatonMainStatus(Enum):
    Resolved = 2
    UnResolved = 1


@app.post('/refresh-modal')
async def refreshModal(request: Request):
    data = await request.json()

    # json = json.loads(data)
    # print(data)
    print(data['statusId'],data['filecount'])
    notifD = checkAndMarkNotificationsAsCompleted(data['statusId'],data['filecount'])
    
    return notifD
    # val = checkAndMarkNotificationsAsCompleted(notificationId,fileCount)
    # return val
    

def checkAndMarkNotificationsAsCompleted(notificationId, fileCount):
    fileCount = int(fileCount)
    try:
        cursor = conn.cursor()

        # Step 1: Check if logs for that notification ID have count = fileCount
        query1 = 'SELECT COUNT(*) FROM "Log" WHERE "NotificationId" = %s;'
        cursor.execute(query1, (notificationId,))
        total_count = cursor.fetchone()[0]

        print('total count', total_count)

        if total_count == fileCount:
            print('coming here')
            # Step 2: Check if with status as completed count = fileCount
            query2 = 'SELECT COUNT(*) FROM "Log" WHERE "NotificationId" = %s AND "Status" = %s;'
            cursor.execute(query2, (notificationId, NotificationStatus.Completed.value))
            completed_count = cursor.fetchone()[0]
 
            if completed_count == fileCount:
                cursor.close()
                
                return {"status":"success"}
            else:
                query9 = 'SELECT COUNT(*) FROM "Log" WHERE "NotificationId" = %s AND "Status"=%s;'
                cursor.execute(query9, (notificationId,NotificationStatus.InProcess.value))
                inprocess_count = cursor.fetchone()[0]

                if inprocess_count>0:
                    return {"status":"inProgress"}

                # ******* need to check whether any file in progress, if so wait, and show errors after
                query3 = 'SELECT "Details" FROM "Log" WHERE "NotificationId" = %s AND "Status" IN (%s,%s);'
                cursor.execute(query3, (notificationId, NotificationStatus.Duplicate.value, NotificationStatus.CorruptError.value))
                errors = cursor.fetchall()
                error_details = [record[0] for record in errors]
                cursor.close()
                
                return {"status": "error", "errors": error_details}
        else:
            cursor.close()
            return {"status":"inProgress"}

    except Exception as e:
        print("Error checking notifications:", e)
        return {"status": "fetching-error", "message": str(e)}


# async def checkAndMarkNotificationsAsCompleted(NotificationId:int, fileCount):
#     try:
#         cursor = conn.cursor()
#         logQuery = """select count(*) from "Log" where "Log"."NotificationId" = '{}';""".format(NotificationId)
#         cursor.execute(logQuery)
#         logFileCount = cursor.fetchall()
#         if(fileCount == logFileCount):
#             cursor.execute('UPDATE "Notification" SET "Status" = %s WHERE "Id" = %s;', (NotificationStatus['Completed'].value, NotificationId))
#             conn.commit()  

        
#     except Exception as fetch_err:
#         print("Error fetching records:", fetch_err)
#         # conn.rollback()
#         raise HTTPException(status_code=500, detail=f"Error occurred: {str(fetch_err)}")
#     return ;

# checkAndMarkNotificationsAsCompleted: takes notificationId and FileCount, if fileCount is equal to number of logs, or if the time to last upload has been 30mins, then we will update the status based on if we got any errors, if errors are there we need to give option to replace or discard, in corrupt error no need for option

@app.post('/clear-all-notifications')
async def clearAllNotifications():
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM "Notification";')
        conn.commit()
        cursor.close()
        return "success, notifications cleared"
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(fetch_err)}")


@app.post('/get-notification-date')
def getNotificationDate():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT "CreatedAt" FROM "Notification" ORDER BY "CreatedAt" DESC LIMIT 1;')
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result[0]
        else:
            return None  # No notifications found
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(fetch_err)}")

class NotificationLimit(BaseModel):
    Limit: int


@app.post('/get-notifications')
async def getNotifications(notificationLimit:NotificationLimit):
    limit = notificationLimit.Limit
    print('limit is ', limit)

    try:

        # cursor = conn.cursor()
        # cursor.execute('SELECT * FROM "Notification" ORDER BY "CreatedAt" DESC;')
        # records = cursor.fetchall()

        cursor = conn.cursor()
        query = 'SELECT * FROM "Notification" ORDER BY "CreatedAt" DESC LIMIT %s;'
        cursor.execute(query, (limit,))
        records = cursor.fetchall()

        updated_records = []

        for noti in records:
            
            val = json.loads(noti[2])
            print('notif: ', val['fileCount'])
            if(noti[5]==MainNotificationStatus.Resolved.value):
                notification_status = {"status":"success"}
            else:
                notification_status = checkAndMarkNotificationsAsCompleted(noti[0],val['fileCount'])
            
            print('moon')
            noti_list = list(noti)
            noti_list.append(notification_status)
            
            # Convert back to tuple if necessary or add to updated_records directly
            updated_records.append(noti_list)

        print(records)
        
        cursor.close()
        
        
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
    return updated_records

@app.get("/login/",status_code=status.HTTP_201_CREATED)
async def get_users(Email: str, Password: str):
    cursor = conn.cursor()
    query = """SELECT "Email", "Password" FROM "User" WHERE "User"."Email" = '{}';""".format(Email)
    cursor.execute(query)
    data = cursor.fetchall()
    # # todos = supabase.table("User").select("*").execute()
    # todos = supabase.table("User").select("Email","Password")
    # todos = todos.eq("Email",Email).execute()
    # data = todos.data
    if len(data) == 0:
        return {"error": "Invalid Login Credentials", "statusCode":False}
    else:
        if data[0][1] == Password:
            return {"error": "Password is correct" ,"statusCode" : True,"session_name":generateSessionName(),"session_token":generateSessionToken(),"validation_time":generateValidationTime()}
        else:
            return {"error": "Invalid Login Credentials","statusCode" : False}



# =======================================================================================================================
# ===================================TABLE SELECT QUERIES ===========================================================
# =======================================================================================================================


@app.get("/get_education/")
def get_education():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Education";')
        records = cursor.fetchall()
        cursor.close()
        print("records got:", records)
        #  records
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
    # todos = fetch_records()
    return records

# Experience
@app.get("/workexperience/")
def get_workExperience():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "WorkExperience";')
        records = cursor.fetchall()
        cursor.close()
        print("records got:", records)
        #  records
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
    # todos = fetch_records()
    return records



# Skills
@app.get("/Skills/")
def get_Skills():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Skill";')
        records = cursor.fetchall()
        cursor.close()
        print("records got:", records)
        #  records
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
    # todos = fetch_records()
    return records

# Details
@app.get("/candidatedetails/")
def get_details():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Candidate";')
        records = cursor.fetchall()
        cursor.close()
        print("records got:", records)
        #  records
    except Exception as fetch_err:
        
        print("Error fetching records:", fetch_err)
    # todos = fetch_records()
    return records

# Contact
@app.get("/contact/")
def get_contact():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Contact";')
        records = cursor.fetchall()
        cursor.close()
        print("records got:", records)
        #  records
    except Exception as fetch_err:
        print("Error fetching records:", fetch_err)
    # todos = fetch_records()
    return records

# check User
def get_checkuser(FirstName,LastName,Email,MobileNumber):
    lst=[]
    ConatctVAlues = [*Email,*MobileNumber]
    for i in ConatctVAlues:
        lst.append("'{}'".format(i))
    values = ",".join(lst)
    print(values)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM "Resume" INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId" INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" WHERE "Candidate"."FirstName" = '{}' AND "Candidate"."LastName" ='{}' 
                    AND "Contact"."Contact_value" IN ({});'''.format(FirstName,LastName,values))
    resumes = cursor.fetchall()
    if len(resumes)>0:
        return "Already Exist"
    else:
        return "Please Enter"
    
# =======================================================================================================================
# ===================================TABLE SELECT QUERIES END ===========================================================
# =======================================================================================================================


import json

import os

def file_exists(filename):
    return os.path.exists(filename)

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_json_file(filename, data):
    # filename = f"{user_id}_output.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.post("/chatbot/", status_code=status.HTTP_201_CREATED)
def chatbot(data:dict):
    print("chatbot recieved:: ",data)

    # file = "D:/Ex2_Projects/TalenTrack/api/" + str(data["user"])+"_output.json"
    file = str(data["user"])+"_output.json"
    if file_exists(file):

        print("file_exists")
        
        log_data = read_json_file(file)
        print("log",log_data["resume_filters"])
        p = ResumeBot(str(data["query"]), log_data["resume_filters"],log_data["count"],False)
    
    else:
        p = ResumeBot(str(data["query"]), data["resume_filters"],data["count"],False)
    print("archit check reply")
    print("reply", p.reply[2])
    user_id = "userid1"
    data = {
    "query": "",
    "resume_filters": {
        "Candidate": {
            "check": []
        },
        "Education": {
            "check": []
        },
        "WorkExperience": {
            "check": []
        },
        "Contact": {
            "check": []
        },
        "Skill": {
            "check": []
        },
        "Address":{
            "check":[]
        },
        "ResumeIdList": {
            "check": [],
            "ResumeIdValue": []
        }
    },
    "count": 0
}
    data["resume_filters"] = p.reply[1]
    # print(p.reply[1])
    print("summary....................",p.summary)
    # data["count"] = p.reply[2]
    data["count"] = p.count
    updatedfile = f"{user_id}_output.json"
    write_json_file(updatedfile, data)

    print("reply.....................",p.reply)

    final_reults=p.reply+[p.summary]
    print("finalllll", final_reults)
    return final_reults

# class Education(BaseModel)
#     # Id:int
#     ResumeId :int
#     Degree :str
#     Branch:str
#     Institution:str
#     Score:float
#     YearOfPassing:str


    

    
class Data(BaseModel):
    data:list

@app.post("/Resumeslist/",status_code=status.HTTP_201_CREATED)
async def get_resumeslist(data:Data):
    print(type(data))
    value = base64.b64decode(data)
    decoded_string = value.decode('utf-8')
    print(data)
    cursor = conn.cursor()
    query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
    INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
    INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
    INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
    INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
    WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
    '''


    placeholders = ', '.join(['%s' for _ in data])
    cursor.execute(query % placeholders, data)

    resumes = cursor.fetchall()

    return (resumes)


# For Display Filters

Send_Data = {
  "ResumeId": "",
  "FirstName": "",
  "Role":  "",
  "SkillName":  set(),
  "Experience":"",
  "Contact_Email":  "",
  "Contact_Phone": "",
  "Location":set(),
  "UploadDate":"",
  "IsViewed":""
}
def to_DateTime(item):
    dateitem = datetime.strptime(str(item),'%Y-%m-%d %H:%M:%S.%f')
    ConvertedDate = dateitem.strftime('%d-%m-%Y')
    return ConvertedDate


from collections import OrderedDict
def tocreate_json(data):
    mainlst={}
    item = Send_Data.copy()
    for i in data:
        item = Send_Data.copy()
        item["SkillName"]=set()
        item["Location"]=set()
        # print(i)
        if i[0] in mainlst:
                mainlst[i[0]]['SkillName'].add(i[5])
                mainlst[i[0]]['Location'].add(i[7].title() if i[7] else i[7])
                if i[4]=="Email":
                    mainlst[i[0]]["Contact_Email"]=i[3]
                if i[4]=="Phone_no":
                    mainlst[i[0]]["Contact_Phone"]=i[3]
        else:
            item["ResumeId"] = i[0]
            item["FirstName"] = i[1].title()+" "+i[-1].title()
            item["Role"] = i[2].capitalize()
            if i[4]=="Email":
                item["Contact_Email"]=i[3]
            if i[4]=="Phone_no":
                item["Contact_Phone"]=i[3]
            item["Experience"]=i[6]
            item["Location"].add(i[7].title() if i[7] else i[7])

            item["UploadDate"]=to_DateTime(i[8])
            item["IsViewed"] = i[-2]
            item["SkillName"].add(i[5])
            mainlst[i[0]]=item
    # mainlst = dict(reversed(mainlst.items()))

    # sorted_mainlst = OrderedDict(sorted(mainlst.items(), key=lambda item: item[1]['ResumeId'], reverse=True))
    # print(sorted_mainlst)
    return mainlst  


@app.post("/displayfilter/",status_code=status.HTTP_201_CREATED)
async def display_filter_resume_data(filters:ResumeFilters):
    # filters = dict(filters)
    
    r = get_filter_resume(filters)
    if r:
        return full_resume_data(r)
    else:
        
        return []
    


@app.post("/chatbotfilter/",status_code=status.HTTP_201_CREATED)
async def get_chatbot_resumes(filters:ResumeFilters):
    r = get_filter_resume(filters)
    if r:
        return r
    else:
        
        return []

    


def get_filter_resume(filters):
    filters = dict(filters)

    print("get_filter_resume", filters)
    ResumesIds=[]
    
    query = 'select "Resume"."ResumeId" from "Resume"'
    tables = []
    where_filters = []
    for key in filters:
        print(filters[key])
        if dict(filters[key])["check"]!=[] and key == "ResumeIdList":
            ResumesIds = dict(filters[key])["ResumeIdValue"][0]
            continue
        if dict(filters[key])["check"]!=[]:
            tables.append('"'+key+'"')
            for col in list(dict(filters[key])["check"]):
                print(dict(filters[key]))
                values = dict(filters[key])[col]
                lst=[]
                for i in values:
                    lst.append("'{}'".format(i))
                lst = ",".join(lst)
                print(dict(filters[key])[col])

                if col=="Experience":
                     where_filters.append(f'"{key}"."{col}" >= {dict(filters[key])[col][0]}')
                else:
                    where_filters.append(f'"{key}"."{col}" IN ({lst})')
                # return tuple(dict(filters[key])[col])
    # table_query =' INNER JOIN '.join(tables)
    where_query = ' AND '.join(where_filters)
    # on_query = " ON "
    # on_query = " ON "
    for table in tables:
        table_join = ' INNER JOIN '+ f"{table}"
        on_query = " ON " + ' "Resume".'+'"ResumeId"'+"="+f"{table}."+'"ResumeId" '
        query += table_join + on_query
    if where_query:
        query= query + " WHERE "+ where_query + ' AND "Resume"."IsActive" = true'
    else:
        query+= " WHERE "+ '"Resume"."IsActive" = true'
    # if "SkillName" in query:
    #     query = query+" GROUP BY 'Resume'.'ResumeId' HAVING COUNT( DISTINCT 'Skill'.'SkillName' ) = {};".format(len(dict(filters['Skill'])['SkillName']))
    # else:
    query = query+";"
    print("queryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy---------------------------: ",query)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        resumesId = cursor.fetchall()
        print("length..................................................",len(resumesId))
        print(resumesId)
        lst=[]
        if len(resumesId)>0:
            print("cccccccccccccccccccccccccccccccc ",len(ResumesIds))
            for i in resumesId:
                lst.append(str(i[0]))
            if (len(ResumesIds)>0):
                lst = list(set(lst).intersection(set(ResumesIds)))
            # if len(lst)==0:
            #     return []

            print("get_filter_resume", lst)
            return list(set(lst))
            # return full_resume_data(lst)
        else:
            return []
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return []
    


@app.post("/full_resume_data/",status_code=status.HTTP_201_CREATED)
async def get_chatbot_resumes(resumeids:list[str]):
    print("entering full_resume_data")
    data = full_resume_data(list(resumeids))
    return data
    

def full_resume_data(lst):
    print("lst................len///////////////",len(lst))
    try:

        if len(lst)==0:
            print("no resumes")
            return [0,None]
        cursor = conn.cursor()
        query = '''SELECT "Resume"."ResumeId","FirstName","Category","Contact_value","Contact_type","SkillName","Experience","City","UpdatedDate","IsViewed","LastName" FROM "Resume"
        LEFT JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
        LEFT JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
        LEFT JOIN "Address" ON "Address"."ResumeId" = "Resume"."ResumeId"
        LEFT JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
        WHERE ("Contact"."Contact_type"='Email' OR "Contact"."Contact_type"='Phone_no') AND "Resume"."IsActive" = true AND "Resume"."ResumeId" IN (%s) ORDER BY "UpdatedDate" DESC;
        '''
        placeholders = ', '.join(['%s' for _ in lst])
        # Executing the query with the placeholders and values


        cursor.execute(query % placeholders, lst)
        resumes = cursor.fetchall()
        print("len_----------------",len(resumes))
        resumes = tocreate_json(resumes)
        print("len_----------------",len(resumes))
        return [len(resumes),resumes]
    except Exception as e:
        traceback.print_exc()
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return [0, None]




import json

# Open the JSON file and load its contents into a Python dictionary
with open('data/SkillsData/skillsMapping.json', 'r') as file:
    skills = json.load(file)


with open('data/SkillsData/Category.json', 'r') as file:
    skill_category = json.load(file)

@app.post("/CreateMapper/",status_code=status.HTTP_201_CREATED)
async def get_skills(Category:str,Skills:str):
    skills[Category] = Skills.split(',')


@app.get("/SkillMappers/",status_code=status.HTTP_201_CREATED)
async def get_skills():
    # print(list(skill_category.keys()))
    with open('data/SkillsData/Category.json', 'r') as file:
        skill_category = json.load(file)
    print(skill_category)
    return list(skill_category.keys())

def to_map_flag_value(folder,categorys):
    new_categories ={}
    for i in categorys.keys():
        value=0
        print(categorys[i])
        for j in categorys[i]:
            if j in folder:
                value = value +folder[j]
                print(value)
        new_categories[i] = value
    return new_categories
def to_map_subcategory_flag_value(folder,category):

    print("cats",category)
    new_categories ={}
    for i in category:
        value = folder[i]
        new_categories[i] = value
    return new_categories


@app.get("/CategoryFlag/",status_code=status.HTTP_201_CREATED)
async def Category_flag():
    # print(list(skill_category.keys()))

    print("entering category flag")
    with open('data/SkillsData/Category.json', 'r') as file:
        skill_category = json.load(file)
    print(skill_category)
    folders = read_json_file("data/folders/newData.json")
    new_category_list = to_map_flag_value(folders,skill_category)
    print(new_category_list)
    return new_category_list


@app.get("/subCategoryflag/",status_code=status.HTTP_201_CREATED)
def subcategory_newDataFlag(category:str):
    print("entering skillmapcategory")
    # print(skill_category[category])
    with open('data/SkillsData/Category.json', 'r') as file:
        skill_category = json.load(file)
    print(skill_category)
    folders = read_json_file("data/folders/newData.json")
    print(folders)
    new_category_list = to_map_subcategory_flag_value(folders,skill_category[category])
    print(new_category_list)
    return new_category_list

# def to_map_flag_value(folder,categorys):
#     new_categories ={}
#     for i in categorys.keys():
#         value=0
#         for j in categorys[i]:
#             if i in folder:
#                 value = value +folder[i]
#         new_categories[i] = value
#     return new_categories
# @app.get("/SkillMappers2/",status_code=status.HTTP_201_CREATED)
# async def get_skills():
#     # print(list(skill_category.keys()))
#     with open('data/SkillsData/Category.json', 'r') as file:
#         skill_category = json.load(file)
#     print(skill_category)
#     folders = read_json_file("data/folders/newData.json")
#     new_category_list = to_map_flag_value(folders,skill_category)
#     print(new_category_list)
#     # return list(skill_category.keys())
#     return new_category_list




# @app.get("/skillmapCategory/",status_code=status.HTTP_201_CREATED)
# def skills_mapping_Category(category:str):
#     print("entering skillmapcategory")
#     # print(skill_category[category])
#     with open('data/SkillsData/Category.json', 'r') as file:
#         skill_category = json.load(file)
#     print(skill_category)
#     return skill_category[category]

@app.get("/fetch_folder_skills/",status_code=status.HTTP_201_CREATED)
def fetch_folder_skills():   
    data = read_json_file("data/SkillsData/skillsMapping.json")

    for key in data:
        for i in range(len(data[key])):
            data[key][i] = data[key][i].title()
            # print(v)
            
    # print(data)
    return data


# @app.get("/displayskillmap/",status_code=status.HTTP_201_CREATED)
# def skills_mapping(category_data:str):
#     print(category_data, category_data)
#     # print(skills["Web Developers"])
#     category = [i.capitalize() for i in skills[category_data]]
#     cursor = conn.cursor()
#     cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in {tuple(category)} group by "Skill"."ResumeId";""")
#     # cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in ('Java','Python') group by "Skill"."ResumeId";""")
#     resumes =[]
#     for item in cursor.fetchall():
#         resumes.append(item[0])
#     print(resumes)
#     cursor.close()
#     cursor = conn.cursor()
#     query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
#     INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
#     INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
#     INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
#     INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
#     WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
#     '''
#     placeholders = ', '.join(['%s' for _ in resumes])
#     cursor.execute(query % placeholders, resumes)
#     resumes = cursor.fetchall()
#     return [len(resumes),resumes]

@app.get("/displayskillmap/",status_code=status.HTTP_201_CREATED)
def skills_mapping_display(category_data:str):
    print("category_data",category_data)
    try:
    # print(skills["Web Developers"])
        # cursor = conn.cursor()
        category_data = category_data.split(" & ")
        categories =[]
        for i in category_data:
            print(i.capitalize())
            categories.append("'{}'".format(i.lower()))
        categories = ",".join(categories)
        cursor = conn.cursor()
        cursor.execute(f"""SELECT "Resume"."ResumeId" FROM "Resume" WHERE "Resume"."Category" IN ({categories});""")
        resumes =[]
        for item in cursor.fetchall():
            resumes.append(item[0])
        # print("llllllllllllllllllllllllllllllllllll------------------------------",resumes)
        cursor.close()
        if len(resumes)>0:
            cursor = conn.cursor()
            query = '''SELECT "Resume"."ResumeId","FirstName","Category","Contact_value","Contact_type","SkillName","Experience","City","UpdatedDate","IsViewed","LastName" FROM "Resume"
        LEFT JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
        LEFT JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
        LEFT JOIN "Address" ON "Address"."ResumeId" = "Resume"."ResumeId"
        LEFT JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
        WHERE ("Contact"."Contact_type"='Email' OR "Contact"."Contact_type"='Phone_no') AND "Resume"."IsActive" = true AND "Resume"."ResumeId" IN (%s) ORDER BY "UpdatedDate" DESC;
            '''
            placeholders = ', '.join(['%s' for _ in resumes])
            cursor.execute(query % placeholders, resumes)
            resumes = cursor.fetchall()
            resumes = tocreate_json(resumes)
            print( [len(resumes),resumes])
            return [len(resumes),resumes]
        else:
            return [0, None]
    except Exception as e:
        traceback.print_exc()
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return [0, None]



# ResumesIds=[]
# Accessing the dictionary
# print(skills["Web Developer"])
@app.post("/skillmap/",status_code=status.HTTP_201_CREATED)
def skills_mapping(category_data:dict):
    # print(category_data, category_data["cat_name"]) 
    # print(skills["Web Developers"])  

    try:

        category = [i.capitalize() for i in skills[category_data["cat_name"]]]
        cursor = conn.cursor()    
        cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in {tuple(category)} group by "Skill"."ResumeId";""")   
        # cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in ('Java','Python') group by "Skill"."ResumeId";""")   
        resumes =[]

        for item in cursor.fetchall():
            resumes.append(item[0])

        # print(resumes)
        cursor.close()
        
        cursor = conn.cursor()
        query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
        INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
        INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
        INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
        INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
        WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
        '''


        placeholders = ', '.join(['%s' for _ in resumes])
        cursor.execute(query % placeholders, resumes)

        resumes = cursor.fetchall()
        return [len(resumes),resumes]
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return [0, "None"]

# =======================================================================================================================
# ===================================TABLE INSERTION QUERIES===========================================================
# =======================================================================================================================
def add_skills(skill, resume_id): 

    try:       
        cursor = conn.cursor()    
        cursor.execute(f'INSERT INTO "Skill" ("ResumeId", "SkillName") VALUES (\'{resume_id}\', \'{skill}\');')    
        cursor.close()
        return "Sucessfully Added skills"

    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        return f"Error occurred: {str(e)}"





def add_contacts(contact_details):   
    try:     
        cursor = conn.cursor()  
        cursor.execute(f'INSERT INTO "Contact" ("CandidateId", "ResumeId", "Contact_type","Contact_value") VALUES (\'{contact_details["CandidateId"]}\',\'{contact_details["ResumeId"]}\', \'{contact_details["Contact_type"]}\', \'{contact_details["Contact_value"]}\');')   
        cursor.close()  
        return "Sucessfully Added skills"
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return "Skills Insertion Unsuccessfull"


def add_candidate(details):
    try:
        cursor = conn.cursor()  
        cursor.execute(f'INSERT INTO "Candidate" ("ResumeId","Title", "FirstName","LastName","DOB", "Status", "Experience","RoleCategory") VALUES (\'{details["ResumeId"]}\', \'{details["Title"]}\',\'{details["FirstName"]}\',\'{details["LastName"]}\',\'{details["DOB"]}\', \'{details["Status"]}\',\'{details["Experience"]}\',\'{details["RoleCategory"]}\')RETURNING   "Candidate"."Id";')   
        candidate_id = cursor.fetchone()[0]
        print(candidate_id)
        cursor.close()  
        return candidate_id
    
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return None


# @app.post("/addEducation/", status_code=status.HTTP_201_CREATED)
def add_education(Details):    

    try:
        cursor = conn.cursor()        
        cursor.execute(f'INSERT INTO "Education" ("ResumeId", "Degree", "Branch", "Institution", "Score", "YearOfPassing") VALUES (\'{Details["ResumeId"]}\', \'{Details["Degree"]}\', \'{Details["Branch"]}\', \'{Details["Institution"]}\', \'{Details["Score"]}\', \'{Details["YearOfPassing"]}\');')
        conn.commit()        
        cursor.close()
        return "Sucessfully Added"
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  
        print(f"Error occurred: {str(e)}")
        return "Error in insertion of data in Education table"+" following details : "+ Details



# @app.post("/addExperience/", status_code=status.HTTP_201_CREATED)
def add_experience(exp_data):

    try:
        cursor = conn.cursor()
        ResumeId = exp_data['ResumeId']
        CompanyName = exp_data['CompanyName']
        DepName = exp_data['DepName']
        Role = exp_data['Role']
        StartDate = exp_data['StartDate']
        EndDate = exp_data['EndDate']
        Location = exp_data['Location']
        IsCurrentJob = exp_data['IsCurrentJob']
        Details = exp_data['Details']

        cursor.execute(f'INSERT INTO "WorkExperience" ("ResumeId","CompanyName","DepName","Role","StartDate","EndDate","Location","IsCurrentJob","Details") VALUES ( \'{ResumeId}\',\'{CompanyName}\',\'{DepName}\',\'{Role}\',\'{StartDate}\',\'{EndDate}\',\'{Location}\',\'{IsCurrentJob}\',\'{Details}\');')
      
        cursor.close()
        return "Work ex Successsfuly added"


    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return"Error in insertion of data in work ex table"+" following details : "+ str(exp_data)



def add_resume(filename, category, isViewed, isActive):
    resume_data = {
        # "ResumeId":100,
        "FileName" :filename,
        "FileType": "pdf",
        "Path" :"somewhere",
        "CreatedBy":70,
        # "CreatedDate" ,
        "UpdatedBy" :70,
        # "UpdatedDate" timestamp,
        "Status": True,
        "Category": category.lower() if category else category,
        "IsViewed":isViewed,
        "IsActive":isActive
    }
  

    try:
        insert_query = ("""
        INSERT INTO "Resume" ("FileHash", "FileName", "FileType", "Path", "CreatedBy", "UpdatedBy", "Status", "Category","IsViewed","IsActive")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s) RETURNING   "Resume"."ResumeId";
    """)
        cursor = conn.cursor()
        cursor.execute(insert_query, (
            # resume_data["ResumeId"],
            "dummyhash",
            resume_data["FileName"],
            resume_data["FileType"],
            resume_data["Path"],
            resume_data["CreatedBy"],
            resume_data["UpdatedBy"],
            resume_data["Status"],
            resume_data["Category"],
            resume_data["IsViewed"],
            resume_data["IsActive"],
        ))
        resume_id = cursor.fetchone()[0]
        print(resume_id)
        cursor.close()
        conn.commit() 
        return resume_id
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return None


@app.post("/savefilter/",status_code=status.HTTP_201_CREATED)
def save_filter(filter_data):
    try:
        cursor = conn.cursor()  
        cursor.execute(f'INSERT INTO "SavedFilter" ("title", "content","createdby") VALUES (\'{filter_data["Title"]}\', \'{filter_data["Content"]}\',\'{filter_data["CreatedBy"]}\';')   
        # candidate_id = cursor.fetchone()[0]
        # print(candidate_id)
        cursor.close()  
        pass
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return 
    

from parser.skills_Extractor import add_newskills



@app.post("/add_folder/",status_code=status.HTTP_201_CREATED)
def add_folder(folder_data:dict):
    print(folder_data)



    if "ParentFolder" in folder_data:
        parentFolder = folder_data["ParentFolder"]
    else:
        parentFolder = None


    folders = read_json_file("data/SkillsData/Category.json")

    newDatamap = read_json_file("data/folders/newData.json")


    all_folders = []

    # print(folders)

    for key, values in folders.items():
        all_folders.append(key.lower())
        for v in values:
            all_folders.append(v.lower())

    if folder_data["Name"].strip().lower() in all_folders:
        print("Folder already exists")
        # return "Folder already exists"
        return {"status":409,"error":"Folder already exists"}

   

    try:
        cursor = conn.cursor()
        # query = """
        # INSERT INTO "ResumeFolder" ("Name", "Role", "Skills", "IsActive","CreatedBy", "SharedWith","ParentFolder")
        # VALUES (%s, %s,%s,%s, %s, %s,%s);
        # """
        query = f'INSERT INTO "ResumeFolder" ("Name","Skills","IsActive","ParentFolder") VALUES (\'{folder_data["Name"]}\',\'{folder_data["Skills"]}\',\'{True}\',\'{parentFolder}\');'
        

        print(query)
        # params = (folder_data["Name"], folder_data["Skills"], True,folder_data["UserId"],'UserId',None)

        # cursor.execute(query, (folder_data["Name"], folder_data["Role"], 
        # folder_data["Skills"], True,folder_data["UserId"],"",7))
        cursor.execute(query)

        cursor.close()
        conn.commit() 


        if parentFolder:          
            folders[parentFolder].append(folder_data["Name"])
            newDatamap[folder_data["Name"]] = 0
            write_json_file("data/folders/newData.json",newDatamap)
            
        else:        
            # folders[folder_data["Name"]] = [folder_data["Skills"]]
            folders[folder_data["Name"]] = []

        
        write_json_file("data/SkillsData/Category.json", folders)

        folder_skills = read_json_file("data/SkillsData/skillsMapping.json")
        folder_skills[folder_data["Name"]] = [a.strip().lower() for a in folder_data["Skills"].lower().split(',')]
        write_json_file("data/SkillsData/skillsMapping.json", folder_skills)


        add_newskills(folder_data["Skills"].split(','))
        

        return {"status":200, "action": "Folder Created"}
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return "add folder failed"
    


from fuzzywuzzy import fuzz


@app.post("/editFolderName/",status_code=status.HTTP_201_CREATED)
def edit_folder_name(data:dict):

    try:

        data = dict(data)
        old_name = data["PrevFolderName"]
        new_name = data["NewFolderName"]
        parent_folder = data["ParentFolder"]


        if fuzz.partial_ratio(old_name.lower(), new_name.lower())<60:
            return {"status":401, "action": "Changes are more that 60%. Please create a new folder"}


        categoryFolders = read_json_file("data/SkillsData/Category.json")
        newDatamap = read_json_file("data/folders/newData.json")


        if parent_folder:
            # print(categoryFolders[parent_folder], old_name)
            
            categoryFolders[parent_folder].remove(old_name)
            categoryFolders[parent_folder].append(new_name)
            newDatamap[new_name] = newDatamap.pop(old_name)

        else:
            categoryFolders[new_name] = categoryFolders.pop(old_name)

        write_json_file("data/folders/newData.json",newDatamap)       
        write_json_file("data/SkillsData/Category.json", categoryFolders)

        return {"status":200, "action": "Folder name edited"}
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return {"status":400, "action": "Error occured in folder name editing"}

    
    
def add_address(resumeId, city, state, country):

    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO public."Address" ("ResumeId", "City", "State", "Country")
        VALUES (%s, %s,%s, %s) RETURNING "Id";
        """
        cursor.execute(insert_query, (
        resumeId,city,state,country
        ))
        
        conn.commit()
        cursor.close()
        return "address added"
    except Exception as e:
        traceback.print_exc()
        conn.rollback()       
        print(f"Error occurred: {str(e)}")
        # raise HTTPException(status_code=500, detail=str(e))
        return "address added error occured"



# =======================================================================================================================
# ===================================TABLE INSERTION QUERIES END===========================================================
# =======================================================================================================================


class UpdateView(BaseModel):
    id:int
    isviewed:bool
@app.put("/Isviewed",status_code=status.HTTP_201_CREATED)
def isviewedResume(data:UpdateView):
    try:
        print(data)
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE "Resume" SET "IsViewed"={data.isviewed} WHERE "Resume"."ResumeId"={data.id};""")
        conn.commit()
        cursor.close()
        return "Successfully Updated"

    except Exception as e:
            traceback.print_exc()
            conn.rollback()       
            print(f"Error occurred: {str(e)}")
            # raise HTTPException(status_code=500, detail=str(e))
            return "error occured in resume view status updation"

def create_newDataFlag(resumeCategory):

    try:

        folders = read_json_file("data/folders/newData.json")
        category = resumeCategory.title()

        for k in folders:
            if k.lower()==category.lower():
                folders[k]+=1
        write_json_file("data/folders/newData.json", folders)
        return "Created Flag successfully"

    except Exception as e:
            traceback.print_exc()
            conn.rollback()       
            print(f"Error occurred: {str(e)}")


@app.post("/updateNewDataFlag/",status_code=status.HTTP_201_CREATED)
def update_newDataFlag(data:dict):

    category = data["folder"]
    folders = read_json_file("data/folders/newData.json")

    for k in folders:
        if category.lower()==k.lower():
            folders[k] = 0
    write_json_file("data/folders/newData.json", folders)
    
    return "Flag data updated"

@app.get("/fetchNewDataFlag/", status_code=status.HTTP_200_OK)
def fetch_newDataFlag():
    try:
        folders = read_json_file("data/folders/newData.json")
        return folders
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error reading newData.json"})
    
@app.get("/fetch_folder_subfolders/", status_code=status.HTTP_200_OK)
def fetch_newDataFlag():
    try:
        folders = read_json_file("data/SkillsData/Category.json")
        return folders
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error reading newData.json"})


    






def DuplicateDetection(FirstName,LastName,Email,MobileNumber):

    try:
        lst=[]
        ConatctVAlues = [*Email,*MobileNumber]
        for i in ConatctVAlues:
            lst.append("'{}'".format(i))
        values = ",".join(lst)
        print(values)
        cursor = conn.cursor()
        cursor.execute('''SELECT "FileName" FROM "Resume" INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId" INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" WHERE "Candidate"."FirstName" = '{}' AND "Candidate"."LastName" ='{}'
                        OR "Contact"."Contact_value" IN ({});'''.format(FirstName,LastName,values))
        resumes = cursor.fetchall()

        # print(resumes[0][0])
        if len(resumes)>0:
            return resumes[0][0]
        else:
            return False   
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return  False
 
    

from parser.boolean_search import filter_finder

@app.post("/search_query/",status_code=status.HTTP_201_CREATED)
def bool_query(query:dict):

    try:
        print(type(query), query)

        showFlag = False
        search_words = ["find","need","search","retrieve","show", "get","give","provide"]

        for i in query["query"].split():
            if i.lower().strip() in search_words:
                showFlag = True


        filters, bools = filter_finder(query["query"], showFlag)
        print("second",filters,bools)
        resumes= []
        for filter in filters:

            if filter:
                resumes.append(get_filter_resume(filter))
            else:
                resumes.append([])

        print(resumes)
        
        for i in range(len(bools)):
            if bools[i]=="and":
                intersection = set(resumes[i]).intersection(set(resumes[i+1]))
                # resumes[i] = intersection
                resumes[i+1] = intersection
                
            else:
                union = set(resumes[i]).union(set(resumes[i+1]))
                resumes[i+1]=union

        
                
        return full_resume_data(list(resumes[-1]))
    except Exception as e:
        traceback.print_exc()
        print(f"Error occurred: {str(e)}")
        return full_resume_data([])


class NotificationId(BaseModel):
    NotifID:int

@app.post("/markNotificationAsResolved/")
def markNotificationAsResolved(notificationID:NotificationId):
    notificationID = notificationID.NotifID;
    try:
        update_query = ("""
        UPDATE "Notification"
        SET "Status" = %s
        WHERE "Id" = %s;
        """)
        cursor = conn.cursor()
        cursor.execute(update_query, (
            MainNotificationStatus.Resolved.value,
            notificationID
        ))
        conn.commit()
        cursor.close()       
        return {'success':'Success'} 

    except Exception as e:
        traceback.print_exc()
        conn.rollback() 
        print(f"Error occurred: {str(e)}")
        return {'failed':'Failed'} 




from typing import List


@app.post("/replace_resume/",status_code=status.HTTP_201_CREATED)
def replace_resume(data:List[str]):

    print(data)

    for d in data:

        d=d.split(",")



        filename1 = d[0]
        filename2 = d[1]
        logId = d[2]
        
        
        try:

            
            update_query = ("""DELETE FROM "Resume" WHERE "FileName" = %s;""")
            cursor = conn.cursor()        
            cursor.execute(update_query, (filename1,))

            update_query = ("""UPDATE "Log" SET "Status"=%s WHERE "Id"=%s;""")
            # cursor = conn.cursor()        
            cursor.execute(update_query, (2,logId,))

            update_query = ("""UPDATE "Resume" SET "IsActive"=%s WHERE "FileName"=%s;""")
            # cursor = conn.cursor()        
            cursor.execute(update_query, (True,filename2,))

            conn.commit()
            cursor.close()
            # print(f"Log entry with Id: {updated_log["Id"]} updated successfully")   

            print("File got replaced succesfully")
            return "File got replaced succesfully"
            

        except Exception as e:
            traceback.print_exc()
            conn.rollback()  # Rollback the transaction if an error occurs
            print(f"Error occurred: {str(e)}")
            return "Error occured in file replacement"
    

    return "File replaced successfully"


def update_log(updated_log):
    try:
        update_query = ("""
        UPDATE "Log"
        SET "Status" = %s, "Details" = %s
        WHERE "Id" = %s;
        """)
        cursor = conn.cursor()
        cursor.execute(update_query, (
            updated_log["Status"],
            updated_log["Details"],
            updated_log["Id"],
            
            
        ))
        conn.commit()
        cursor.close()
        # print(f"Log entry with Id: {updated_log["Id"]} updated successfully")

        

    except Exception as e:
        traceback.print_exc()
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        






class WorkExperienceItem(BaseModel):
    Company: str
    Position: str
    Start_Date: str
    End_Date: str
    Location: str
    Description: str
    Is_Current: bool
    Reference: str

class DataItem(BaseModel):
    LogId:int
    Resume_name:str
    Summary:list
    Name: str
    Phn_no: list
    Email: list
    Urls: dict
    Education: OrderedDict
    Skills: list
    Degree: dict
    Work_Experience: dict
    Projects: list
    Locations:dict
    Curr_role:str
    TotalExp:float


from mapping_func import find_best_match, category_finder, skill_based_category

@app.post("/alldata/",status_code=status.HTTP_201_CREATED)
async def post_all_data(all_data:DataItem):


    try:
        print('All data function was successfully called!')

        print(all_data)


        # print("lOg idddddddddddddddddddddddd, ", all_data.LogId)


        updated_log = {
            "Id":all_data.LogId,
            "Status":NotificationStatus.Completed.value,
            "Details": str(all_data.Resume_name)
        }


        if not all_data.Email and not all_data.Phn_no:
            updated_log = {
            "Id":all_data.LogId,
            "Status":NotificationStatus.Completed.value,
            "Details": str(all_data.Resume_name)
            }

            updated_log["Status"] = NotificationStatus.CorruptError.value
            updated_log["Details"] = "no emails or phone number found"
            update_log(updated_log)
            resume_id = add_resume(all_data.Resume_name, resume_category, False,False)




        



        
        new_curr_role = str(all_data.Curr_role)
        current_job_role = ""
        reserve_job = []
        total_exp = 0

        for k in all_data.Work_Experience:
            reserve_job.append(k)

            print(k)


            total_exp+=all_data.Work_Experience[k][8]

            print(total_exp,"exppppppppppppppppppp")
            if all_data.Work_Experience[k][6]:
                
                current_job_role = k

        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        print("cureent_job========================", current_job_role)

        if all_data.Summary[0]!="None":
            # resume_category = find_best_match(all_data.Summary[0])
            resume_category = category_finder(all_data.Summary[0])


        

        elif current_job_role.strip()!="":        

            resume_category = category_finder(current_job_role)
            # resume_category = find_best_match(current_job_role)
            print(current_job_role, resume_category)
            if not resume_category:
                for j in reserve_job:
                    print("reserve_job", j)
                    resume_category = category_finder(j)
                    if resume_category:
                        break

        elif new_curr_role!="":
            resume_category = category_finder(new_curr_role)
            # resume_category = find_best_match(current_job_role)
            print(new_curr_role, resume_category)
            if not resume_category:
                for j in reserve_job:
                    print("reserve_job", j)
                    resume_category = category_finder(j)
                    if resume_category:
                        break

                
        elif reserve_job:

            for j in reserve_job:
                print("reserve_job", j)
                resume_category = category_finder(j)
                if resume_category:
                    break

            # resume_category = find_best_match(current_job_role)
            print(current_job_role, resume_category)

        else:
            resume_category="None"



        if resume_category=="None" or not resume_category:
            print("skill based category")
            resume_category = skill_based_category(all_data.Skills)
        

        print("resume category......................", resume_category)

        if DuplicateDetection(" ".join(all_data.Name.split()[:-1]),all_data.Name.split()[-1] if len(all_data.Name.split())>1 else "NA",list(all_data.Phn_no),list(all_data.Email)):

            dup_file = DuplicateDetection(" ".join(all_data.Name.split()[:-1]),all_data.Name.split()[-1] if len(all_data.Name.split())>1 else "NA",list(all_data.Phn_no),list(all_data.Email))
            print("detected")

            updated_log["Status"] = NotificationStatus.Duplicate.value
            updated_log["Details"] = str(all_data.Resume_name)+","+ str(dup_file)+","+str(all_data.LogId)



            update_log(updated_log)
            resume_id = add_resume(all_data.Resume_name, resume_category, False,False)
            # return "Resume Already Exists"
        else:

            update_log(updated_log)
            resume_id = add_resume(all_data.Resume_name, resume_category, False,True)

            if resume_category:
                create_newDataFlag(resume_category)

        
        
            

        

        
        

        if resume_id:
            # experience = random.choice([0.0,1.0, 2.0, 3.0, 4.0])



            candidate_details = {

                "ResumeId":resume_id,
                "Title":"Unknown",
                "FirstName":" ".join(all_data.Name.split()[:-1]).title() if len(all_data.Name.split())>1 else all_data.Name.title() ,
                "LastName":all_data.Name.split()[-1].title() if len(all_data.Name.split())>1 else " ",
                "DOB":"",
                "Status":"Null",
                "Experience":float(all_data.TotalExp) ,
                # "Experience":round(total_exp,2) ,
                "RoleCategory": resume_category.lower().strip()
            }

            candidate_id = add_candidate(candidate_details)

            print(f"Resume ID: {resume_id}, Candidate ID: {candidate_id}")

            

            for key , value in all_data.Urls.items():

                contact_details = {
                    "CandidateId":candidate_id,
                    "ResumeId":resume_id,
                    "Contact_type":key,
                    "Contact_value":value

                }
                add_contacts(contact_details)

            if all_data.Phn_no:
                for phone in all_data.Phn_no:
                    contact_details = {
                        "CandidateId":candidate_id,
                        "ResumeId":resume_id,
                        "Contact_type":"Phone_no",
                        "Contact_value":phone

                    }
                    add_contacts(contact_details)

            else:
                contact_details = {
                        "CandidateId":candidate_id,
                        "ResumeId":resume_id,
                        "Contact_type":"Phone_no",
                        "Contact_value":"91XXXXXXXX"

                    }
                add_contacts(contact_details)


            for email in all_data.Email:
                contact_details = {
                    "CandidateId":candidate_id,
                    "ResumeId":resume_id,
                    "Contact_type":"Email",
                    "Contact_value":email.split(":")[-1]

                }
                add_contacts(contact_details)



            # all_data.Skills+=resume_category.lower().split()

            for skill in all_data.Skills:
                add_skills(skill, resume_id)

            
            if all_data.Locations:
                locs = dict(all_data.Locations)
                states = []
                for city, state in locs.items():
                    if state not in locs:
                        states.append(state)

                for s in states:
                    locs[s] = s            
                for city,state in locs.items():
                    add_address(resume_id, city.lower(),state.lower(), "India")


            for key, value in all_data.Work_Experience.items():
                    
                    
                    
                    
                    exp_data = {
                            "ResumeId":resume_id,
                            "CompanyName": all_data.Work_Experience[key][0] if all_data.Work_Experience[key] else "" ,
                            "DepName":all_data.Work_Experience[key][1],
                            "Role":all_data.Work_Experience[key][2], 
                            "StartDate": all_data.Work_Experience[key][3],
                            "EndDate": all_data.Work_Experience[key][4], 
                            # "Location": all_data.Work_Experience[key][5], 
                            # "Location": all_data.Work_Experience[key][5], 
                            "Location": "India", 
                            "IsCurrentJob": all_data.Work_Experience[key][6], 
                            "Details": all_data.Work_Experience[key][7]
                            }
                    
                    add_experience(exp_data)


            for key , value in all_data.Education.items():
                # print(key)

                if all_data.Education[key]:
                    if all_data.Education[key][0]=="":
                        score = 0
                    elif float(all_data.Education[key][0].strip("%")) > 10:
                        score = float(all_data.Education[key][0].strip("%"))/10
                    else:
                        score = float(all_data.Education[key][0].strip("%"))
                    degree = random.choice(["bachelors", "masters", "phd", "diploma"])
                    education = {
                                "ResumeId":resume_id,
                                "Degree" :degree,
                                "Branch":'none',
                                "Institution":key,
                                "Score":score ,
                                "YearOfPassing":all_data.Education[key][1][1] if len(all_data.Education[key][1]) >1 else "Unknown year of passing"
                                # "YearOfPassing":all_data.Education[key][1].split("-")[1],
                            }
                    add_education(education)
            
            conn.commit()   
                
            return all_data
        else:
            return "Resume Id not generated"
        
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=404, detail=f"all_data insertion error occur.")
        
        

def hello():
    print("hello2")


# class RawString(BaseModel):
#     raw_string: str

# @app.post("/decode/")
# def decode_raw_string(raw_string: RawString):
#     try:
#         normal_string = raw_string.raw_string.encode().decode('unicode_escape')
#         return {"normal_string": normal_string}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# def upload_to_s3(file_path, bucket_name, object_name):
#     # Initialize boto3 client

#     try:
#         # Upload file to specified bucket
#         s3_client.upload_file(file_path, bucket_name, object_name)
#         print(f"File uploaded successfully to {bucket_name}/{object_name}")
#     except Exception as e:
#         print(f"Error uploading file: {e}")


if __name__ == "__main__":
    # consumer_thread = threading.Thread(target=consumer_function)
    # consumer_thread.start()
    # upload_to_s3('C:/Users/yaggarwal/Documents/archit.pdf','armss-dev','archit.pdf')
 
    # print(checkAndMarkNotificationsAsCompleted(16, 2))
    
    print('****************This function was reached, and launched uvicorn fastapi**********')
    uvicorn.run("main:app", host="0.0.0.0",port=8000, reload=True)

#database restart
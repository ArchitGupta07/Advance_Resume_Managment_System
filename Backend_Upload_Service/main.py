from fastapi import FastAPI, status, Query, Body, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config
# from supabase import create_client, Client
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
import requests
from parser.main_func import main
import traceback
import uuid
from uploadLogging2 import upload_logging

# from boto3Client import s3_client 

url = config("SUPERBASE_URL")
key = config("SUPERBASE_KEY")
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# supabase: Client = create_client(url, key)
from enum import Enum


class NotificationType(Enum):
    FileUpload = 1

class NotificationStatus(Enum):
    InProcess = 1
    Completed = 2
    Duplicate = 3
    CorruptError = 4


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


# from botocore.exceptions import NoCredentialsError

# def downloadFile(filename):
#     try:
#         # Generate the presigned URL for the S3 object
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': 'armss-dev',
#                                                             'Key': filename},
#                                                     ExpiresIn=3600)
#     except NoCredentialsError:
#         print("Credentials not available")
#         return None

#     # The response contains the presigned URL
#     return response


def handleUpload(filename):
    log_id=1
    try:
        url = downloadFile(filename)
        print(f'main was called, link is {url}')
        

        notif_match = re.search(r'\[(\d+)\]', filename)
        if notif_match:
            log_data = {
                "NotificationId": notif_match.group(1) ,
                "Status": NotificationStatus.InProcess.value,
                "Details": "file data extraction in process",
                "CreatedAt": datetime.now()
            }

            log_id = post_log(log_data)
        
        
        main(url,filename, log_id)
    except Exception as fetch_err:

        updated_log = {
        "Id":log_id,
        "Status":NotificationStatus.CorruptError.value,
        "Details": str(filename)
        }
        update_log(updated_log)
        
        print("Error  running upload function:", fetch_err)
        
    # todos = fetch_records()
        return None

# @app.post('/view-resume')
# def resumeViewer(filename):
#     return downloadFile(filename)



@app.post("/upload/webhook")
async def fileUploaded(msg:dict):
    print('webhook caught****************************')
    filename = msg["Key"].split("/")[-1]
    print(f'filename is ***********: {filename}')
    handleUpload(filename)

import urllib.parse
from fastapi import Response

# @app.post("/upload/webhook")
# async def fileUploaded(request: Request):
#     # Log the request payload
#     payload = await request.json()
#     message = json.loads(payload['Message'])
#     print(message)
#     filename = message["Records"][0]["s3"]["object"]["key"]

#     fileAlreadyExist = checkIfFileExistsInDB(filename)
#     if fileAlreadyExist:
#         return Response(status_code=200)
    
#     print('webhook caught****************************')
#     print('Payload received:', message)
    
#     decoded_filename = urllib.parse.unquote(filename)
#     print('filename is this: ', str(filename))
#     print('decoded file name: ',decoded_filename)

#     handleUpload(decoded_filename)
#     return Response(status_code=200)

# @app.post("/upload/webhook")
# async def fileUploaded(request: Request):
#     # Log the request payload
#     payload = await request.json()
#     message = json.loads(payload['Message'])
#     print(message)
#     filename = message["Records"][0]["s3"]["object"]["key"]

#     file_already_exists = checkIfFileExistsInDB(filename)
#     if file_already_exists:
#         return Response(status_code=200)
    
#     print('Webhook caught****************************')
#     print('Payload received:', message)
    
#     decoded_filename = urllib.parse.unquote(filename)
#     print('Filename is this: ', str(filename))
#     print('Decoded file name:', decoded_filename)

#     handleUpload(decoded_filename)
#     return Response(status_code=200)



def checkIfFileExistsInDB(filename):
    try:
        cursor = conn.cursor()

        # Step 1: Check if logs for that notification ID have count = fileCount
        query = 'SELECT COUNT(*) FROM "Resume" WHERE "Resume"."FileName" = %s;'
        cursor.execute(query, (filename,))
        total_count = cursor.fetchone()[0]

        if total_count>0:
            return True
    
    except Exception as e:
        traceback.print_exc()
        conn.rollback() 
        print(f"Error occurred: {str(e)}")
        return  False
    


@app.get("/upload/")
async def read_root():
    return {"message": "Upload Service is up"}

@app.get("/upload/create-session")
async def createSession():
    uuid_item = uuid.uuid4()
    uuid_str = str(uuid_item)
    sessionId = uuid_str;
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    sessionTime = current_time;
    return JSONResponse(content={'sessionId':sessionId, 'sessionTime':sessionTime})



# @app.post("/upload/presignedUrl")
# async def get_presigned_url(key:InputData):
#     try:
#         # Generate presigned URL
#         url = client.get_presigned_url(
#             "PUT",
#             "armss-dev",
#             key.input,
#             expires=timedelta(days=1),

#         )
#         print(url)
#         return JSONResponse(content={"presignedUrl": url})
#     except Exception as err:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))




# @app.get("/login/",status_code=status.HTTP_201_CREATED)
# async def get_users(Email: str, Password: str):
#     cursor = conn.cursor()
#     query = """SELECT "Email", "Password" FROM "User" WHERE "User"."Email" = '{}';""".format(Email)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     # # todos = supabase.table("User").select("*").execute()
#     # todos = supabase.table("User").select("Email","Password")
#     # todos = todos.eq("Email",Email).execute()
#     # data = todos.data
#     if len(data) == 0:
#         return {"error": "Account does Not Exists", "statusCode":False}
#     else:
#         if data[0][1] == Password:
#             return {"error": "Password is correct" ,"statusCode" : True,"session_name":generateSessionName(),"session_token":generateSessionToken(),"validation_time":generateValidationTime()}
#         else:
#             return {"error": "Password is incorrect","statusCode" : False}



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

from fastapi.responses import PlainTextResponse

@app.get("/upload/see-logs/")
async def get_log_contents():
    file_path = "out.log"
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/upload/clear-logs/")
async def clear_log():
    log_file = "out.log"
    try:
        # Open the log file in write mode to clear its contents
        open(log_file, 'w').close()
        return {"message": "Log file cleared successfully."}
    except Exception as e:
        return {"error": str(e)}

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

def write_json_file(user_id, data):
    filename = f"{user_id}_output.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# @app.post("/chatbot/", status_code=status.HTTP_201_CREATED)
# def chatbot(data:dict):
#     print("chatbot recieved:: ",data)

#     # file = "D:/Ex2_Projects/TalenTrack/api/" + str(data["user"])+"_output.json"
#     file = str(data["user"])+"_output.json"
#     if file_exists(file):

#         print("file_exists")
        
#         log_data = read_json_file(file)
#         print("log",log_data["resume_filters"])
#         p = ResumeBot(str(data["query"]), log_data["resume_filters"],log_data["count"])
    
#     else:
#         p = ResumeBot(str(data["query"]), data["resume_filters"],data["count"])
#     print("archit check reply")
#     print("reply", p.reply[2])
#     user_id = "userid1"
#     data = {
#     "query": "",
#     "resume_filters": {
#         "Candidate": {
#             "check": []
#         },
#         "Education": {
#             "check": []
#         },
#         "WorkExperience": {
#             "check": []
#         },
#         "Contact": {
#             "check": []
#         },
#         "Skill": {
#             "check": []
#         },
#         "ResumeIdList": {
#             "check": [],
#             "ResumeIdValue": []
#         }
#     },
#     "count": 0
# }
#     data["resume_filters"] = p.reply[1]
#     data["count"] = p.reply[2]

#     write_json_file(user_id, data)

#     return p.reply

# class Education(BaseModel):
#     # Id:int
#     ResumeId :int
#     Degree :str
#     Branch:str
#     Institution:str
#     Score:float
#     YearOfPassing:str


    

    
class Data(BaseModel):
    data:list

# @app.post("/Resumeslist/",status_code=status.HTTP_201_CREATED)
# async def get_resumeslist(data:Data):
#     print(type(data))
#     value = base64.b64decode(data)
#     decoded_string = value.decode('utf-8')
#     print(data)
#     cursor = conn.cursor()
#     query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
#     INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
#     INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
#     INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
#     INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
#     WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
#     '''


#     placeholders = ', '.join(['%s' for _ in data])
#     cursor.execute(query % placeholders, data)

#     resumes = cursor.fetchall()

#     return (resumes)


# For Display Filters

# Send_Data = {
#   "ResumeId": "",
#   "FirstName": "",
#   "Role":  "",
#   "SkillName":  set(),
#   "Experience":"",
#   "Contact_Email":  "",
#   "Contact_Phone": "",
#   "Location":set(),
#   "UploadDate":"",
# }
# def to_DateTime(item):
#     dateitem = datetime.strptime(str(item),'%Y-%m-%d %H:%M:%S.%f')
#     ConvertedDate = dateitem.strftime('%d-%m-%Y')
#     return ConvertedDate


# def tocreate_json(data):
#     mainlst={}
#     lst=[]
#     item = Send_Data.copy()
#     for i in data:
#         if i[0] in lst:
#                 mainlst[i[0]]['SkillName'].add(i[5])
#                 mainlst[i[0]]['Location'].add(i[7])

#                 if i[4]=="Email":
#                     item["Contact_Email"]=i[3]
#                 if i[4]=="Phone_no":
#                     item["Contact_Phone"]=i[3]
#         else:
#             lst.append(i[0])
#             item["ResumeId"] = i[0]
#             item["FirstName"] = i[1]
#             item["Role"] = i[2]
#             if i[4]=="Email":
#                 item["Contact_Email"]=i[3]
#             if i[4]=="Phone_no":
#                 item["Contact_Phone"]=i[3]
#             item["Experience"]=i[6]
#             # item["Location"]=i[7]
#             item["Location"].add(i[7])
#             item["UploadDate"]=to_DateTime(i[8])
#             item["SkillName"].add(i[5])
#             mainlst[i[0]]=item
#             item = Send_Data.copy()
#             item["SkillName"]=set()
#             item["Location"]=set()


#     return mainlst



# @app.post("/displayfilter/",status_code=status.HTTP_201_CREATED)
# async def display_filter_resume_data(filters:ResumeFilters):
#     # filters = dict(filters)
    
#     r = get_filter_resume(filters)
#     if r:
#         return full_resume_data(r)
#     else:
        
#         return []
    


# @app.post("/chatbotfilter/",status_code=status.HTTP_201_CREATED)
# async def get_chatbot_resumes(filters:ResumeFilters):
#     r = get_filter_resume(filters)
#     if r:
#         return r
#     else:
        
#         return []

    


# def get_filter_resume(filters):
#     filters = dict(filters)
#     ResumesIds=[]
    
#     query = 'select "Resume"."ResumeId" from "Resume"'
#     tables = []
#     where_filters = []
#     for key in filters:
#         print(filters[key])
#         if dict(filters[key])["check"]!=[] and key == "ResumeIdList":
#             ResumesIds = dict(filters[key])["ResumeIdValue"][0]
#             continue
#         if dict(filters[key])["check"]!=[]:
#             tables.append('"'+key+'"')
#             for col in list(dict(filters[key])["check"]):
#                 print(dict(filters[key]))
#                 values = dict(filters[key])[col]
#                 lst=[]
#                 for i in values:
#                     lst.append("'{}'".format(i))
#                 lst = ",".join(lst)
#                 print(dict(filters[key])[col])
#                 where_filters.append(f'"{key}"."{col}" IN ({lst})')
#                 # return tuple(dict(filters[key])[col])
#     # table_query =' INNER JOIN '.join(tables)
#     where_query = ' AND '.join(where_filters)
#     # on_query = " ON "
#     # on_query = " ON "
#     for table in tables:
#         table_join = ' INNER JOIN '+ f"{table}"
#         on_query = " ON " + ' "Resume".'+'"ResumeId"'+"="+f"{table}."+'"ResumeId" '
#         query += table_join + on_query
#     if where_query:
#         query= query + " WHERE "+ where_query
#     # if "SkillName" in query:
#     #     query = query+" GROUP BY 'Resume'.'ResumeId' HAVING COUNT( DISTINCT 'Skill'.'SkillName' ) = {};".format(len(dict(filters['Skill'])['SkillName']))
#     # else:
#     query = query+";"
#     print(query,ResumesIds)
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         resumesId = cursor.fetchall()
#         print(resumesId)
#         lst=[]
#         if len(resumesId)>0:
            
#             for i in resumesId:
#                 lst.append(str(i[0]))
#             if (len(ResumesIds)>0):
#                 lst = list(set(lst).intersection(set(ResumesIds)))
#             # if len(lst)==0:
#             #     return []
#             return lst
#             # return full_resume_data(lst)
#         else:
#             return []
#     except Exception as e:
#         traceback.print_exc()

#         conn.rollback()  # Rollback the transaction if an error occurs
#         print(f"Error occurred: {str(e)}")
#         return []
    


# @app.post("/full_resume_data/",status_code=status.HTTP_201_CREATED)
# async def get_chatbot_resumes(resumeids:list[str]):

#     data = full_resume_data(list(resumeids))
#     return data
    

# def full_resume_data(lst):

#     try:
#         cursor = conn.cursor()
      
#         query = '''SELECT "Resume"."ResumeId","FirstName","Category","Contact_value","Contact_type","SkillName","experience","Location","UpdatedDate" FROM "Resume"
#         INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
#         INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
#         INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
#         INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
#         WHERE ("Contact"."Contact_type"='Email' OR "Contact"."Contact_type"='Phone_no') AND "Resume"."ResumeId" IN (%s);
#         '''
#         placeholders = ', '.join(['%s' for _ in lst])
#         # Executing the query with the placeholders and values
#         cursor.execute(query % placeholders, lst)
#         resumes = cursor.fetchall()
#         resumes = tocreate_json(resumes)
#         return [len(resumes),resumes]
#     except Exception as e:
#         traceback.print_exc()

#         conn.rollback()  # Rollback the transaction if an error occurs
#         print(f"Error occurred: {str(e)}")
#         return [0, None]




# import json

# # Open the JSON file and load its contents into a Python dictionary
# with open('data/SkillsData/skillsMapping.json', 'r') as file:
#     skills = json.load(file)


# with open('data/SkillsData/Category.json', 'r') as file:
#     skill_category = json.load(file)

# @app.post("/CreateMapper/",status_code=status.HTTP_201_CREATED)
# async def get_skills(Category:str,Skills:str):
#     skills[Category] = Skills.split(',')


# @app.get("/SkillMappers/",status_code=status.HTTP_201_CREATED)
# async def get_skills():
#     return list(skill_category.keys())


# @app.get("/skillmapCategory/",status_code=status.HTTP_201_CREATED)
# def skills_mapping_Category(category:str):
#     return skill_category[category]



# # @app.get("/displayskillmap/",status_code=status.HTTP_201_CREATED)
# # def skills_mapping(category_data:str):
# #     print(category_data, category_data)
# #     # print(skills["Web Developers"])
# #     category = [i.capitalize() for i in skills[category_data]]
# #     cursor = conn.cursor()
# #     cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in {tuple(category)} group by "Skill"."ResumeId";""")
# #     # cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in ('Java','Python') group by "Skill"."ResumeId";""")
# #     resumes =[]
# #     for item in cursor.fetchall():
# #         resumes.append(item[0])
# #     print(resumes)
# #     cursor.close()
# #     cursor = conn.cursor()
# #     query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
# #     INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
# #     INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
# #     INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
# #     INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
# #     WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
# #     '''
# #     placeholders = ', '.join(['%s' for _ in resumes])
# #     cursor.execute(query % placeholders, resumes)
# #     resumes = cursor.fetchall()
# #     return [len(resumes),resumes]

# @app.get("/displayskillmap/",status_code=status.HTTP_201_CREATED)
# def skills_mapping_display(category_data:str):


#     try:
#     # print(skills["Web Developers"])
#         # cursor = conn.cursor()
#         category_data = category_data.split(" & ")
#         categories =[]
#         for i in category_data:
#             categories.append("'{}'".format(i))
#         categories = ",".join(categories)
#         cursor = conn.cursor()
#         cursor.execute(f"""SELECT "Resume"."ResumeId" FROM "Resume" WHERE "Resume"."Category" IN ({categories});""")
#         resumes =[]
#         for item in cursor.fetchall():
#             resumes.append(item[0])
#         cursor.close()
#         if len(resumes)>0:
#             cursor = conn.cursor()
#             query = '''SELECT "Resume"."ResumeId","FirstName","Category","Contact_value","Contact_type","SkillName","experience","Location","UpdatedDate" FROM "Resume"
#             INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
#             INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
#             INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
#             INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
#             WHERE ("Contact"."Contact_type"='Email' OR "Contact"."Contact_type"='Phone_no') AND "Resume"."ResumeId" IN (%s);
#             '''
#             placeholders = ', '.join(['%s' for _ in resumes])
#             cursor.execute(query % placeholders, resumes)
#             resumes = cursor.fetchall()
#             resumes = tocreate_json(resumes)
#             return [len(resumes),resumes]
#         else:
#             return [0, None]
#     except Exception as e:
#         traceback.print_exc()

#         conn.rollback()  # Rollback the transaction if an error occurs
#         print(f"Error occurred: {str(e)}")
#         return [0, None]



# # ResumesIds=[]
# # Accessing the dictionary
# # print(skills["Web Developer"])
# @app.post("/skillmap/",status_code=status.HTTP_201_CREATED)
# def skills_mapping(category_data:dict):
#     # print(category_data, category_data["cat_name"]) 
#     # print(skills["Web Developers"])  

#     try:

#         category = [i.capitalize() for i in skills[category_data["cat_name"]]]
#         cursor = conn.cursor()    
#         cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in {tuple(category)} group by "Skill"."ResumeId";""")   
#         # cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in ('Java','Python') group by "Skill"."ResumeId";""")   
#         resumes =[]

#         for item in cursor.fetchall():
#             resumes.append(item[0])

#         # print(resumes)
#         cursor.close()
        
#         cursor = conn.cursor()
#         query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
#         INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
#         INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
#         INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
#         INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
#         WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
#         '''


#         placeholders = ', '.join(['%s' for _ in resumes])
#         cursor.execute(query % placeholders, resumes)

#         resumes = cursor.fetchall()
#         return [len(resumes),resumes]
    
#     except Exception as e:
#         traceback.print_exc()

#         conn.rollback()  # Rollback the transaction if an error occurs
#         print(f"Error occurred: {str(e)}")
#         return [0, "None"]

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
        cursor.execute(f'INSERT INTO "Candidate" ("ResumeId","Title", "FirstName","LastName","DOB", "Status", "Experience") VALUES (\'{details["ResumeId"]}\', \'{details["Title"]}\',\'{details["FirstName"]}\',\'{details["LastName"]}\',\'{details["DOB"]}\', \'{details["Status"]}\',\'{details["Experience"]}\')RETURNING   "Candidate"."Id";')   
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
        return"Error in insertion of data in work ex table"+" following details : "+ exp_data



def add_resume(filename, category):
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
        "Category": category
    }
  

    try:
        insert_query = ("""
        INSERT INTO "Resume" ("FileHash", "FileName", "FileType", "Path", "CreatedBy", "UpdatedBy", "Status", "Category")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING   "Resume"."ResumeId";
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
        ))
        resume_id = cursor.fetchone()[0]
        print(resume_id)
        cursor.close()
        return resume_id
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return None
    

def add_address(resumeId, city, country):
    
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO public."Address" ("ResumeId", "City", "Country")
        VALUES (%s, %s, %s) RETURNING "Id";
        """
        cursor.execute(insert_query, (
           resumeId,city,country
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
    


# @app.post("/savefilter/",status_code=status.HTTP_201_CREATED)
# def save_filter(filter_data):
#     try:
#         cursor = conn.cursor()  
#         cursor.execute(f'INSERT INTO "SavedFilter" ("title", "content","createdby") VALUES (\'{filter_data["Title"]}\', \'{filter_data["Content"]}\',\'{filter_data["CreatedBy"]}\';')   
#         # candidate_id = cursor.fetchone()[0]
#         # print(candidate_id)
#         cursor.close()  
#         pass
#     except Exception as e:
#         traceback.print_exc()

#         conn.rollback()  # Rollback the transaction if an error occurs
#         print(f"Error occurred: {str(e)}")
#         return 


# =======================================================================================================================
# ===================================TABLE INSERTION QUERIES END===========================================================
# =======================================================================================================================


def DuplicateDetection(FirstName,LastName,Email,MobileNumber):

    try:
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
        print(resumes)
        if len(resumes)>0:
            return resumes[0][2]
        else:
            return False   
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return  False
 
    

# from parser.boolean_search import filter_finder

# @app.post("/search_query/",status_code=status.HTTP_201_CREATED)
# def bool_query(query:dict):
#     print(type(query), query)

#     filters, bools = filter_finder(query["query"])
#     print("second",filters,bools)
#     resumes= []
#     for filter in filters:
#         resumes.append(get_filter_resume(filter))
#     print(resumes)
    
#     for i in range(len(bools)):
#         if bools[i]=="and":
#             intersection = set(resumes[i]).intersection(set(resumes[i+1]))
#             # resumes[i] = intersection
#             resumes[i+1] = intersection
            
#         else:
#             union = set(resumes[i]).union(set(resumes[i+1]))
#             resumes[i+1]=union
            
#     return full_resume_data(list(resumes[-1]))
def post_log(log_data):

    try:
        insert_query = ("""
        INSERT INTO "Log" ("NotificationId", "Status", "Details", "CreatedAt")
        VALUES (%s, %s, %s, %s) RETURNING "Id";
        """)
        cursor = conn.cursor()
        cursor.execute(insert_query, (
            log_data["NotificationId"],
            log_data["Status"],
            log_data["Details"],
            log_data["CreatedAt"]
        ))
        log_id = cursor.fetchone()[0]
        print(log_id)
        cursor.close()
        conn.commit()
        return log_id

    except Exception as e:
        traceback.print_exc()
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return None
    pass

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
        


from collections import OrderedDict




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
    Locations:list
    Curr_role:str
    TotalExp:float


from mapping_func import find_best_match, category_finder, skill_based_category
import re




@app.post("/alldata/",status_code=status.HTTP_201_CREATED)
async def post_all_data(all_data:DataItem):

    print('all data was called here')


    # print("lOg idddddddddddddddddddddddd, ", all_data.LogId)


    updated_log = {
        "Id":all_data.LogId,
        "Status":NotificationStatus.Completed.value,
        "Details": str(all_data.Resume_name)
    }



    



    if DuplicateDetection(" ".join(all_data.Name.split()[:-1]),all_data.Name.split()[-1] if len(all_data.Name.split())>1 else "NA",list(all_data.Phn_no),list(all_data.Email)):

        dup_file = DuplicateDetection(" ".join(all_data.Name.split()[:-1]),all_data.Name.split()[-1] if len(all_data.Name.split())>1 else "NA",list(all_data.Phn_no),list(all_data.Email))
        print("detected")

        updated_log["Status"] = NotificationStatus.Duplicate.value
        updated_log["Details"] = str(all_data.Resume_name)+","+ str(dup_file)



        update_log(updated_log)
        return "Resume Already Exists"
    else:
        
        update_log(updated_log)
    

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

    elif current_job_role!="":        

        resume_category = category_finder(current_job_role)
        # resume_category = find_best_match(current_job_role)
        print(current_job_role, resume_category)
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

    
    resume_id = add_resume(all_data.Resume_name, resume_category)

    

    if resume_id:
        experience = random.choice([0.0,1.0, 2.0, 3.0, 4.0])



        candidate_details = {

            "ResumeId":resume_id,
            "Title":"Unknown",
            "FirstName":" ".join(all_data.Name.split()[:-1]),
            "LastName":all_data.Name.split()[-1] if len(all_data.Name.split())>1 else "NA",
            "DOB":"",
            "Status":"Null",
            "Experience":round(total_exp,2) 
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
                "Contact_value":email

            }
            add_contacts(contact_details)



        # all_data.Skills+=resume_category.lower().title().split()

        # final_skills = 

        for skill in all_data.Skills:
            add_skills(skill, resume_id)

        
        if all_data.Locations:
            for city in all_data.Locations:
                add_address(resume_id, city, "India")


        for key, value in all_data.Work_Experience.items():
                
                loc = random.choice(["noida", "bangalore", "hyderabad", "mumbai","delhi","new delhi", "lucknow","faridabad","gurugram","gurgaon","pune","jaipur","chandigarh","patiala","jaipur","meerut"])
                
                
                exp_data = {
                        "ResumeId":resume_id,
                        "CompanyName": all_data.Work_Experience[key][0] if all_data.Work_Experience[key] else "" ,
                        "DepName":all_data.Work_Experience[key][1],
                        "Role":all_data.Work_Experience[key][2], 
                        "StartDate": all_data.Work_Experience[key][3],
                        "EndDate": all_data.Work_Experience[key][4], 
                        # "Location": all_data.Work_Experience[key][5], 
                        # "Location": all_data.Work_Experience[key][5], 
                        "Location": loc, 
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

def hello():
    print("hello2")


# from fastapi.responses import FileResponse

# @app.get("/download-logs")
# def download_logs():
#     file_path = "out.log"
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type='application/octet-stream', filename='out.log')
#     else:
#         return {"error": "File not found"}





import threading

if __name__ == "__main__":
    
    # print( downloadFile('1. Vikram iOS.pdf')) 
    # consumer_thread = threading.Thread(target=consumer_function)
    logging_thread = threading.Thread(target=upload_logging)
    logging_thread.start()
    # consumer_thread.start()
    print('****************Upload Service on ::: This function was reached, and launched uvicorn fastapi for Upload**********')
    # upload_logging()
    uvicorn.run("main:app", host="0.0.0.0",port=8001, reload=True)

#database restart
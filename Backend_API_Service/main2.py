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
# import requests
from parser.main_func import main
import traceback

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


def handleUpload(filename):
    url = downloadFile(filename)
    print(f'main was called, link is {url}')
    main(url)


@app.post("/webhook")
def fileUploaded(msg:dict):
    print('webhook caught****************************')
    filename = msg["Key"].split("/")[-1]
    print(f'filename is ***********: {filename}')
    handleUpload(filename)


@app.get("/")
async def read_root():
    return {"message": "Server is up"}


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


# def fetch_records():
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM Education;")
#         records = cursor.fetchall()
#         cursor.close()
#         return records
#     except Exception as fetch_err:
#         print("Error fetching records:", fetch_err)
# @app.get("/usersdetails/",status_code=status.HTTP_201_CREATED)
# async def get_users():
#     todos = supabase.table("User").select("*").execute()
#     return todos



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
            return {"error": "Password is incorrect","statusCode" : False}


# class User(BaseModel):
#     UserName: str
#     Email: str
#     Password: str  

# @app.post("/signup/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: User):
#     user_data = {
       
#         "UserId": random.randint(1000, 10000),
#         "UserName": user.UserName,
#         "Email": user.Email,
#         "Password": user.Password,
#         "Status": True
       
#     }

#     todos = supabase.table("User").select("*")
#     todos = todos.eq("Email",user_data['Email']).execute()
#     data = todos.data

#     if (len(data) == 0):
#         new_user = supabase.table("User").insert(user_data).execute()
#         return {"error":"Sign Up Completed", "statusCode":True}
#     else:
#         return {"error": "Account already Exists , Please Login", "statusCode" : False}


@app.get("/check/")
def get_check():
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

# print(get_checkuser("ADITYA",'RAJ',[+91620187590],['adityaraj.131103@gmail.com']))
# @app.get("/users/")
# async def get_users():
#     # todos = supabase.table("User").select("*").execute()
#     return todos



# @app.get("/login/",status_code=status.HTTP_201_CREATED)
# async def get_users(Email: str, Password: str):
#     # todos = supabase.table("User").select("*").execute()
#     todos = supabase.table("User").select("Email","Password")
#     todos = todos.eq("Email",Email).execute()
#     data = todos.data
#     if len(data) == 0:
#         return {"error": "Account does Not Exists", "statusCode":False}
#     else:
#         if data[0]['Password'] == Password:
#             return {"error": "Password is correct" ,"statusCode" : True,"session_name":generateSessionName(),"session_token":generateSessionToken(),"validation_time":generateValidationTime()}
#         else:
#             return {"error": "Password is incorrect","statusCode" : False}



# class User(BaseModel):
#     UserName: str
#     Email: str
#     Password: str  

# @app.post("/signup/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: User):
#     user_data = {
       
#         "UserId": random.randint(1000, 10000),
#         "UserName": user.UserName,
#         "Email": user.Email,
#         "Password": user.Password,
#         "Status": True
       
#     }
#     # new_user = supabase.table("User").insert(user_data).execute()

#     return new_user


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

@app.post("/chatbot/", status_code=status.HTTP_201_CREATED)
def chatbot(data:dict):
    print(data)

    # file = "D:/Ex2_Projects/TalenTrack/api/" + str(data["user"])+"_output.json"
    file = "api/" + str(data["user"])+"_output.json"
    if file_exists(file):

        print("file_exists")
        
        log_data = read_json_file(file)
        print("log",log_data["resume_filters"])
        p = ResumeBot(str(data["query"]), log_data["resume_filters"],log_data["count"])
    
    else:
        p = ResumeBot(str(data["query"]), data["resume_filters"],data["count"])
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
        "ResumeIdList": {
            "check": [],
            "ResumeIdValue": []
        }
    },
    "count": 0
}
    data["resume_filters"] = p.reply[1]
    data["count"] = p.reply[2]

    write_json_file(user_id, data)

    return p.reply

# class Education(BaseModel):
#     # Id:int
#     ResumeId :int
#     Degree :str
#     Branch:str
#     Institution:str
#     Score:float
#     YearOfPassing:str

# @app.post("/addEducation/", status_code=status.HTTP_201_CREATED)
def add_education(Details):    

    print(Details["Score"])
 
#     new_user = supabase.table("Education").insert(edu_data).execute()
    cursor = conn.cursor()
    # print(f'INSERT INTO "Education" ("ResumeId", "Degree", "Branch", "Institution", "Score", "YearOfPassing") VALUES ({52}, \'{Details["Degree"]}\', \'{Details["Branch"]}\', \'{Details["Institution"]}\', {8.6}, \'{Details["YearOfPassing"]}\');')
    cursor.execute(f'INSERT INTO "Education" ("ResumeId", "Degree", "Branch", "Institution", "Score", "YearOfPassing") VALUES (\'{Details["ResumeId"]}\', \'{Details["Degree"]}\', \'{Details["Branch"]}\', \'{Details["Institution"]}\', \'{Details["Score"]}\', \'{Details["YearOfPassing"]}\');')

    conn.commit()
    
    cursor.close()
    return "Sucessfully Added"



# @app.post("/addExperience/", status_code=status.HTTP_201_CREATED)
def add_experience(exp_data):

    
    # new_user = supabase.table("WorkExperience").insert(exp_data).execute()
    # return new_user
    # print(f'INSERT INTO "WorkExperience" ("CompanyName","DepName","Role","StartDate","EndDate","Location","IsCurrentJob","Details") VALUES ( \'{exp_data['CompanyName']}\',\'{ exp_data['DepName']}\', \'{exp_data['Role']}\',\'{ exp_data['StartDate']}\', \'{exp_data['EndDate']}\', \'{exp_data['Location']}\',\'{ exp_data['IsCurrentJob']}\',\'{ exp_data['Details']}\');')
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
    # cursor.execute(f'INSERT INTO "WorkExperience" ("ResumeId","CompanyName","DepName","Role","StartDate","EndDate","Location","IsCurrentJob","Details") VALUES ( \'{exp_data['ResumeId']}\',\'{exp_data['CompanyName']}\',\'{ exp_data['DepName']}\', \'{exp_data['Role']}\',\'{ exp_data['StartDate']}\', \'{exp_data['EndDate']}\', \'{exp_data['Location']}\',\'{ exp_data['IsCurrentJob']}\',\'{ exp_data['Details']}\');')
    # conn.commit()
    cursor.close()
    
    # cursor = conn.cursor()
    # query = '''SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","experience" FROM "Resume"
    # INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
    # INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
    # INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
    # INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
    # WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
    # '''


    # placeholders = ', '.join(['%s' for _ in resumes])
    # cursor.execute(query % placeholders, resumes)

    # resumes = cursor.fetchall()
    
  
 
    # return [len(resumes),resumes]


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
    # # id = random.randint(0, 100000000)
    # # print(user)
    # new_user = supabase.table("Resume").insert(resume_data).execute()
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
  "Location":"",
  "UploadDate":"",
}
def to_DateTime(item):
    dateitem = datetime.strptime(str(item),'%Y-%m-%d %H:%M:%S.%f')
    ConvertedDate = dateitem.strftime('%d-%m-%Y')
    return ConvertedDate
def tocreate_json(data):
    mainlst={}
    lst=[]
    item = Send_Data.copy()
    for i in data:
        if i[0] in lst:
                mainlst[i[0]]['SkillName'].add(i[5])
                if i[4]=="Email":
                    item["Contact_Email"]=i[3]
                if i[4]=="Phone_no":
                    item["Contact_Phone"]=i[3]
        else:
            lst.append(i[0])
            item["ResumeId"] = i[0]
            item["FirstName"] = i[1]
            item["Role"] = i[2]
            if i[4]=="Email":
                item["Contact_Email"]=i[3]
            if i[4]=="Phone_no":
                item["Contact_Phone"]=i[3]
            item["Experience"]=i[6]
            item["Location"]=i[7]
            item["UploadDate"]=to_DateTime(i[8])
            item["SkillName"].add(i[5])
            mainlst[i[0]]=item
            item = Send_Data.copy()
    return mainlst



@app.post("/displayfilter/",status_code=status.HTTP_201_CREATED)
async def display_filter_resume_data(filters:ResumeFilters):
    filters = dict(filters)
    ResumesIds=[]
    query = 'select "Resume"."ResumeId" from "Resume"'
    tables = []
    where_filters = []
    for key in filters:
        if filters[key].check!=[] and key == "ResumeIdList":
            ResumesIds = dict(filters[key])["ResumeIdValue"][0]
            continue
        if filters[key].check!=[]:
            tables.append('"'+key+'"')
            for col in list(filters[key].check):
                print(dict(filters[key]))
                values = dict(filters[key])[col]
                lst=[]
                for i in values:
                    lst.append("'{}'".format(i))
                lst = ",".join(lst)
                print(dict(filters[key])[col])
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
        query= query + " WHERE "+ where_query
    # if "SkillName" in query:
    #     query = query+" GROUP BY 'Resume'.'ResumeId' HAVING COUNT( DISTINCT 'Skill'.'SkillName' ) = {};".format(len(dict(filters['Skill'])['SkillName']))
    # else:
    query = query+";"
    print(query,ResumesIds)
    cursor = conn.cursor()
    cursor.execute(query)
    resumesId = cursor.fetchall()
    lst=[]
    if len(resumesId)>0:
        for i in resumesId:
            lst.append(str(i[0]))
        if (len(ResumesIds)>0):
            lst = list(set(lst).intersection(set(ResumesIds)))
        if len(lst)==0:
            return []
        #     lst.append("'{}'".format(i[0]))
        # values = ",".join(lst)
        cursor = conn.cursor()
        # cursor.execute('SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","Role" FROM "Resume" INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId" INNER JOIN "Skill" ON "Skill"."ResumeId"="Resume"."ResumeId" INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId"= "Resume"."ResumeId" INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" WHERE "Resume"."ResumeId" IN ({}) ;'.format(values))
        query = '''SELECT "Resume"."ResumeId","FirstName","Category","Contact_value","Contact_type","SkillName","experience","Location","UpdatedDate" FROM "Resume"
        INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
        INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
        INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
        INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
        WHERE ("Contact"."Contact_type"='Email' OR "Contact"."Contact_type"='Phone_no') AND "Resume"."ResumeId" IN (%s);
        '''
        placeholders = ', '.join(['%s' for _ in lst])
        # Executing the query with the placeholders and values
        cursor.execute(query % placeholders, lst)
        resumes = cursor.fetchall()
        resumes = tocreate_json(resumes)
        return [len(resumes),resumes]
    else:
        return []


@app.post("/filter/",status_code=status.HTTP_201_CREATED)
async def filter_resume_data(filters:ResumeFilters):
    filters = dict(filters)
    ResumesIds=[]
    query = 'select "Resume"."ResumeId" from "Resume"'
    tables = []
    where_filters = []
    for key in filters:
        if filters[key].check!=[] and key == "ResumeIdList":
            ResumesIds = dict(filters[key])["ResumeIdValue"][0]
            continue
        
        if filters[key].check!=[]:
            tables.append('"'+key+'"')
            for col in list(filters[key].check):
                print(dict(filters[key]))
                values = dict(filters[key])[col]
                lst=[]
                for i in values:
                    lst.append("'{}'".format(i))
                lst = ",".join(lst)
                print(dict(filters[key])[col])
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
        query= query + " WHERE "+ where_query
    # if "SkillName" in query:
    #     query = query+" GROUP BY 'Resume'.'ResumeId' HAVING COUNT( DISTINCT 'Skill'.'SkillName' ) = {};".format(len(dict(filters['Skill'])['SkillName']))
    # else:
    query = query+";"

    print(query,ResumesIds)
    cursor = conn.cursor()
    cursor.execute(query)
    resumesId = cursor.fetchall()
    lst=[]
    if len(resumesId)>0:
        for i in resumesId:
            lst.append(str(i[0]))
        if ResumesIds:
            lst = list(set(lst).intersection(set(ResumesIds)))
       
        #     lst.append("'{}'".format(i[0]))
        # values = ",".join(lst)
        cursor = conn.cursor()
        # cursor.execute('SELECT "Resume"."ResumeId","FirstName","Contact_value","Contact_type","SkillName","Role" FROM "Resume" INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId" INNER JOIN "Skill" ON "Skill"."ResumeId"="Resume"."ResumeId" INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId"= "Resume"."ResumeId" INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" WHERE "Resume"."ResumeId" IN ({}) ;'.format(values)) 
#         query = '''SELECT "Resume"."ResumeId","Candidate"."FirstName","Contact"."Contact_value","Contact"."Contact_type","Skill"."SkillName","WorkExperience"."Role"
# FROM "Resume"
# INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
# INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
# INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
# INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
# WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s) 
# GROUP BY "Resume"."ResumeId"
# LIMIT 10;
#         '''
        query = '''SELECT DISTINCT("Resume"."ResumeId"),"FirstName","Contact_value","Contact_type","SkillName","Role" FROM "Resume"
        INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
        INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
        INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
        INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId" 
        WHERE "Contact"."Contact_type"='Email' AND "Resume"."ResumeId" IN (%s);
        '''

    
        placeholders = ', '.join(['%s' for _ in lst])

        # Executing the query with the placeholders and values
        cursor.execute(query % placeholders, lst)

        resumes = cursor.fetchall()
        # print("archit",resumes)
        processed = {}
        for item in resumes:
            if item[0] in processed:
                processed[item[0]][4].append(item[4])
                processed[item[0]][5].append(item[5])
            else:
                processed[item[0]] = [item[0], item[1],item[2], item[3], [item[4]], [item[5]] ]
        check = []
        for k,v in processed.items():
            v[4] = list(set(v[4]))
            v[5] = list(set(v[5]))
            check.append(v)


        # print(check[:10])

        return [len(check),check]
    else:
        return []

    

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
    return list(skill_category.keys())


@app.get("/skillmapCategory/",status_code=status.HTTP_201_CREATED)
def skills_mapping_Category(category:str):
    return skill_category[category]



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


    try:
    # print(skills["Web Developers"])
        cursor = conn.cursor()
        cursor.execute(f"""SELECT "Resume"."ResumeId" FROM "Resume" WHERE "Resume"."Category" = '{category_data}'  ;""")
        resumes =[]
        for item in cursor.fetchall():
            resumes.append(item[0])
        cursor.close()
        if len(resumes)>0:
            cursor = conn.cursor()
            query = '''SELECT "Resume"."ResumeId","FirstName","Category","Contact_value","Contact_type","SkillName","experience","Location","UpdatedDate" FROM "Resume"
            INNER JOIN "Candidate" ON "Resume"."ResumeId" = "Candidate"."ResumeId"
            INNER JOIN "Skill" ON "Skill"."ResumeId" = "Resume"."ResumeId"
            INNER JOIN "WorkExperience" ON "WorkExperience"."ResumeId" = "Resume"."ResumeId"
            INNER JOIN "Contact" ON "Resume"."ResumeId" = "Contact"."ResumeId"
            WHERE ("Contact"."Contact_type"='Email' OR "Contact"."Contact_type"='Phone_no') AND "Resume"."ResumeId" IN (%s);
            '''
            placeholders = ', '.join(['%s' for _ in resumes])
            cursor.execute(query % placeholders, resumes)
            resumes = cursor.fetchall()
            resumes = tocreate_json(resumes)
            return [len(resumes),resumes]
        else:
            return []
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return [0, "None"]



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
    cursor = conn.cursor()  
    cursor.execute(f'INSERT INTO "Contact" ("CandidateId", "ResumeId", "Contact_type","Contact_value") VALUES (\'{contact_details["CandidateId"]}\',\'{contact_details["ResumeId"]}\', \'{contact_details["Contact_type"]}\', \'{contact_details["Contact_value"]}\');')   
    cursor.close()  
    return "Sucessfully Added skills"


def add_candidate(details):
    cursor = conn.cursor()  
    cursor.execute(f'INSERT INTO "Candidate" ("ResumeId","Title", "FirstName","LastName","DOB", "Status", "experience") VALUES (\'{details["ResumeId"]}\', \'{details["Title"]}\',\'{details["FirstName"]}\',\'{details["LastName"]}\',\'{details["DOB"]}\', \'{details["Status"]}\',\'{details["experience"]}\')RETURNING   "Candidate"."Id";')   
    candidate_id = cursor.fetchone()[0]
    print(candidate_id)
    cursor.close()  
    return candidate_id


@app.post("/savefilter/",status_code=status.HTTP_201_CREATED)
def save_filter(filter_data):
    cursor = conn.cursor()  
    cursor.execute(f'INSERT INTO "SavedFilter" ("title", "content","createdby") VALUES (\'{filter_data["Title"]}\', \'{filter_data["Content"]}\',\'{filter_data["CreatedBy"]}\';')   
    # candidate_id = cursor.fetchone()[0]
    # print(candidate_id)
    cursor.close()  

    pass







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


from mapping_func import find_best_match

@app.post("/alldata/",status_code=status.HTTP_201_CREATED)
async def post_all_data(all_data:DataItem):
    print(all_data.Work_Experience)

    current_job_role = ""

    for k in all_data.Work_Experience:

        if all_data.Work_Experience[k][6]:
            current_job_role = k


    if all_data.Summary[0]!="":
        resume_category = find_best_match(all_data.Summary[0])
    elif current_job_role!="":        
        resume_category = find_best_match(current_job_role)
    else:
        resume_category="None"


    resume_id = add_resume(all_data.Resume_name, resume_category)
    experience = random.choice([0.0,1.0, 2.0, 3.0, 4.0])



    candidate_details = {

        "ResumeId":resume_id,
        "Title":"Unknown",
        "FirstName":" ".join(all_data.Name.split()[:-1]),
        "LastName":all_data.Name.split()[-1] if len(all_data.Name.split())>1 else "NA",
        "DOB":"",
        "Status":"Null",
        "experience":experience
    }

    candidate_id = add_candidate(candidate_details)

    print(resume_id, candidate_id)





    for key , value in all_data.Urls.items():

        contact_details = {
            "CandidateId":candidate_id,
            "ResumeId":resume_id,
            "Contact_type":key,
            "Contact_value":value

        }
        add_contacts(contact_details)

    for phone in all_data.Phn_no:
        contact_details = {
            "CandidateId":candidate_id,
            "ResumeId":resume_id,
            "Contact_type":"Phone_no",
            "Contact_value":phone

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





    for skill in all_data.Skills:
        add_skills(skill, resume_id)

    for key, value in all_data.Work_Experience.items():
            
            loc = random.choice(["noida", "bangalore", "hyderabad", "mumbai","delhi","mohali"])
            
            
            exp_data = {
                    "ResumeId":resume_id,
                    "CompanyName": all_data.Work_Experience[key][0] if all_data.Work_Experience[key] else "" ,
                    "DepName":all_data.Work_Experience[key][1],
                    "Role":all_data.Work_Experience[key][2], 
                    "StartDate": all_data.Work_Experience[key][3],
                    "EndDate": all_data.Work_Experience[key][4], 
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
                        "YearOfPassing":all_data.Education[key][1][1]
                        # "YearOfPassing":all_data.Education[key][1].split("-")[1],
                    }
            add_education(education)
        
    return all_data

def hello():
    print("hello2")


if __name__ == "__main__":
    # consumer_thread = threading.Thread(target=consumer_function)
    # consumer_thread.start()
    print('****************This function was reached, and launched uvicorn fastapi**********')
    uvicorn.run("main:app", host="0.0.0.0",port=8000, reload=True)

#database restart
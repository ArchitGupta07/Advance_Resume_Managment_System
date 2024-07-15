from resumeDB import conn

# def truncate_table():
#     try:
#         cursor = conn.cursor()
#         cursor.execute('Select count(*) from "Resume";')
#         records = cursor.fetchall()
#         cursor.close()
#         print("records got:", records[0][0])
#         #  records
#     except Exception as fetch_err:
#         print("Error fetching records:", fetch_err)
#     # todos = fetch_records()
#     return "DONE"


# truncate_table()

import json

# Open the JSON file and load its contents into a Python dictionary
with open('api/data/SkillsData/skillsMapping.json', 'r') as file:
    skills = json.load(file)

def skills_mapping(category_data):

    category = [i.capitalize() for i in category_data]
    cursor = conn.cursor()    
    cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in {tuple(category)} group by "Skill"."ResumeId";""")   
    # cursor.execute(f"""Select "Skill"."ResumeId" from "Skill" where "Skill"."SkillName" in ('Java','Python') group by "Skill"."ResumeId";""")   
    resumes =[]

    for item in cursor.fetchall():
        resumes.append(item[0])

    # print(resumes)
    cursor.close()


skills_mapping(skills["Web Developer"])
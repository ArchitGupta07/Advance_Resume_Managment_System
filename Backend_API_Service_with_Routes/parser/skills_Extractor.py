import pandas as pd
import spacy

import re
import nltk
from fuzzywuzzy import fuzz







def extract_skills(resume_text, threshold=92):
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(resume_text)

  
    tokens = [token.text for token in nlp_text if not token.is_stop]
#    D:\Ex2_Projects\TalenTrack\api\data\SkillsData\skillsFound.csv
    # data = pd.read_csv("api/data/SkillsData/skillsFound.csv")
    # data = pd.read_csv("D:/Ex2_Projects/TalenTrack/api/data/SkillsData/skillsFound.csv")
    # data = pd.read_csv("D:/EX2Projects/CurrentProjects/TalenTrackRepo/TalenTrack/api/data/SkillsData/skillsFound.csv")
    # data = pd.read_csv("data/SkillsData/skillsFound.csv")
    # skills = list(data.columns.values)
    with open("data/SkillsData/skillsFound.txt", "r") as file:
        skills = file.read()

    skills = skills.split(',')

# print(content.split(','))


    skillset = []

    for token in tokens:       
        checkToken = re.sub(r'[()\-\._]', '', token.lower())

        for skill in skills:
            if fuzz.ratio(checkToken, skill.lower())==100:
                skillset.append(skill.lower())
                # skillset.append(token.replace("\n",""))
            elif fuzz.ratio(checkToken, skill.lower()) >= threshold:
                if skill not in skillset:
                    # skillset.append(skill.replace("\n",""))
                    skillset.append(skill.lower())
                break

 
    noun_chunks = [chunk.text.lower().strip() for chunk in nlp_text.noun_chunks]

    # check for bi-grams and tri-grams (example: machine learning)
    for chunk in noun_chunks:
        for skill in skills:
            if fuzz.ratio(chunk, skill.lower()) >= threshold:
                # skillset.append(chunk.replace("\n", ""))
                skillset.append(skill.lower())
                break

    #
    final_skills = [i.capitalize() for i in set(skillset)]

    return list(set(final_skills))
    # return [i for i in set([i.lower() for i in skillset])]





    

def extract_skills_for_local(resume_text, threshold=80):
    nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(resume_text)

  
    tokens = [token.text for token in nlp_text if not token.is_stop]
#    D:\Ex2_Projects\TalenTrack\api\data\SkillsData\skillsFound.csv
    # data = pd.read_csv("api/data/SkillsData/skillsFound.csv")
    # data = pd.read_csv("D:/Ex2_Projects/TalenTrack/api/data/SkillsData/skillsFound.csv")
    # data = pd.read_csv("D:/EX2Projects/CurrentProjects/TalenTrackRepo/TalenTrack/api/data/SkillsData/skillsFound.csv")
    # data = pd.read_csv("data/SkillsData/skillsFound.csv")
    # skills = list(data.columns.values)
    with open("../data/SkillsData/skillsFound.txt", "r") as file:
        skills = file.read()

    skills = skills.split(',')

# print(content.split(','))


    skillset = []

    for token in tokens:       
        checkToken = re.sub(r'[()\-\._]', '', token.lower())

        for skill in skills:
            if fuzz.ratio(checkToken, skill.lower())==100:
                skillset.append(token.replace("\n",""))
            elif fuzz.ratio(checkToken, skill.lower()) >= threshold:
                if skill not in skillset:
                    skillset.append(skill.replace("\n",""))
                break

 
    noun_chunks = [chunk.text.lower().strip() for chunk in nlp_text.noun_chunks]

    # check for bi-grams and tri-grams (example: machine learning)
    for chunk in noun_chunks:
        for skill in skills:
            if fuzz.ratio(chunk, skill.lower()) >= threshold:
                skillset.append(chunk.replace("\n", ""))
                break

    return [i.capitalize() for i in set([i.lower() for i in skillset])]
    # return [i for i in set([i.lower() for i in skillset])]



import traceback

def add_newskills(newSkills):

    try:

        with open("data/SkillsData/skillsFound.txt", "r") as file:
            skills = file.read()

        # Split the skills into a list
        existing_skills = skills.split(',')

        # New skills to add
        

        # Add new skills to the existing skills list if they are not already present
        for new_skill in newSkills:
            if new_skill.lower().strip() not in existing_skills:
                existing_skills.append(new_skill.lower().strip())

        # Convert the skills list back to a comma-separated string
        updated_skills = ','.join(existing_skills)

        # Write the updated skills back to the file
        with open("data/SkillsData/skillsFound.txt", "w") as file:
            file.write(updated_skills)
        

        return "New Skills Added"
    
    except Exception as e:
        traceback.print_exc()

      # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return "Error happend in adding skills : ",str(e)

    


   

# from text_extractor import extract_text_from_pdf

# text=""
# for page in extract_text_from_pdf("D:/Ex2_Projects/TalenTrack/api/data/resumes/resume.pdf"):
#     text += ' ' + page 

# print(extract_skills(text))
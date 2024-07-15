from main_func2 import extract_work_ex
import re


def work_ex_date_mapping(text, job_roles, dates):
    mapped_work = {}
    # print("dates", dates)
    # print(text)

    mapped_dist = {}

    if dates:
        for date in dates:

            if text.find(date[0])==-1:
                continue
            
            if job_roles:
                # print(job_roles)

                for role in job_roles:

                    dist =0
                    if len(role)<3:
                        continue


                    #     continue
                    # print(date[0], text.find(date[0]), text.find(role), role )
                    # for r in role.split():
                    dist = abs(text.find(date[0]) - text.find(role))
                   


                    # print(role, date[0], dist)
                    
            # print(mapped_work)

       

    return mapped_work

















def extract_date2(text):
    # pattern1 = r"\b(([a-zA-Z]+’?'?(\s?\d\d)?),?\s?20\d{2})\s?-?–?–?‑?(to)?\s?((([a-zA-Z]+’?'?(\s?\d\d?)?),?\s?20\d{2})|(Present|Till Date|Current|current|present|ongoing))"
    pattern1 = r"\b(([a-zA-Z]+’?'?(\s?\d\d)?),?\s?(20)?\d{2})\s?-?–?–?‑?(to)??\s?((([a-zA-Z]+’?'?(\s?\d\d?)?),?\s?(20)?\d{2})|(Present|Till Date|Current|current|present|ongoing))"
    pattern2 = r"(20\d\d\s?)(-|–|to)(\s?20\d\d)"

    pattern3 = r"(\d\d\/20\d\d)\s?(-|–|to)\s?(\d\d\/20\d\d)"
    single_date_pattern1 = r"((\d\d)(\/|-)(\d\d)(\/|-)(\d\d\d\d))"


    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)
    matches3 = re.findall(pattern3,text)
    single_matches1 = re.findall(single_date_pattern1, text)

    # print(matches1)

    dates1 = []
    dates2 = []
    dates3 = []
    sin_dates1 = []

    if matches1:
        for match in matches1:
            dates1.append([match[0].strip(),match[5].strip()])
    else:
        pass
  
    for match in matches2:
        dates2.append([match[0].strip(),match[2].strip()])

    for match in matches3:
        dates3.append([match[0].strip(),match[2].strip()])

    for match in single_matches1:
        sin_dates1.append([match[0].strip()])   


    return dates1, dates2, dates3, sin_dates1


from skills_Extractor import extract_skills


def remove_characters(text):



    characters_to_remove = ",\"'{}()\\|>^!:;•"
    # Create a translation table
    # translation_table = str.maketrans("", "", characters_to_remove)
    translation_table = str.maketrans(characters_to_remove, ' ' * len(characters_to_remove))
    # Remove the characters
    cleaned_text = text.translate(translation_table)
    return cleaned_text

def skill_date_map(text):

    

    text = divide_resume_sections(text)["Experience"].lower()
    text = text.replace(".","").lower()
    clean_txt = remove_characters(text)
    # print(clean_txt)
    # print(clean_txt.replace("-","").replace("/"," "))
    skills = extract_skills(clean_txt.replace("-","").replace("/"," "))

    # print(skills)
    dates1,dates2,dates3, sin_dates1 = extract_date2(clean_txt)
    all_dates = dates1+dates2+dates3+sin_dates1

    # print(all_dates)
    # print(skills)
    # print("\n\n")
    # print(dates1)
    # print("\n\n")
    # print(dates2)
    # print("\n\n")
    # print(dates3)

    

    workex = extract_work_ex(divide_resume_sections(text)["Experience"].replace("-","").lower())

    text = clean_txt.replace("-","").lower()
    # work = 

    # print(text)

    mapped_skill = {}

   
            
    if skills:
        # print(job_roles)

        for skill in skills:

            dist =0
            # if len(skill)<3:
            #     continue
            date_before_skill  = None
            min_dist = 2000

            if not all_dates:
                print(mapped_skill)
                return mapped_skill

            for date in all_dates:
                if text.find(date[0])==-1:
                    continue



                # print(date[0], text.find(date[0]), text.find(skill.lower()), skill.lower())
                #     continue
                if text.find(skill.lower())==-1:
                    continue
                if text.find(date[0]) < text.find(skill.lower()):
                    # print("yyyyyyyyyyyyyyyyyyyy")
                    # print(date[0], text.find(date[0]),text.find(date[1]), text.find(skill.lower()), skill.lower())
                    # print("nnnnnnnnnnnnnnnnnnnn")

                    # print()
                    dist = abs(text.find(date[0]) - text.find(skill.lower()))
                    
                    if min_dist>dist:
                        min_dist =dist
                        date_before_skill = date

            mapped_skill[skill] = date_before_skill

        
    print(mapped_skill)
            
            # for r in role.split():
            # dist = abs(text.find(date[0]) + text.find(date[1]) - text.find(skill.lower()))
            


                # print(skill, date[0], dist)


    








from text_extractor import tika_text_extraction, divide_resume_sections


def process_file(file):
    text = tika_text_extraction(file)
    # print(text)

    text = remove_characters(text).replace("."," ")

    workex = extract_work_ex(divide_resume_sections(text)["Experience"].replace("-","").lower())

    print(f"file name is {file}")
    print("\n\n")

    print(f"work ex is {workex}")
    print("\n\n")
                    

                    # if not name:
    dates1,dates2,dates3, sin_dates1 = extract_date2(text)
    print(dates1)
    print("\n")
    print(dates2)
    print("\n")
    print(dates3)
    print("\n")
    print(sin_dates1)

    print(divide_resume_sections(text)["Experience"].lower().replace("-",""))
    print("\n\n\n")

    work_ex_date_mapping(divide_resume_sections(text)["Experience"].lower().replace("-",""), [k for k in workex], dates1+dates2+dates3)

import os

def process2(file):
    text = tika_text_extraction(file)

# process_file(fil)

    skill_date_map(text)



def process_all_files_in_folder(folder_path):

    try:
        
        count=0
        detected =0
        not_detected = 0 
        for filename in os.listdir(folder_path):
            if count>100:
                break

            try:
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):  # Ensure it's a file
                    count+=1

                    # process_file(file_path)

                    print(file_path)
                    process2(file_path)

                    print("\n\n\n\n")
                    
            except:
                print(f"failed to process {file_path}")

        print(f"Detected: {detected} and Not Detected : {not_detected}")
        return detected,not_detected
    
    except:

        print(f"error occured in {file_path}")
        
        return detected,not_detected

        
# check

# Example usage
folder_path = 'D:/Ex2_Projects/Resumes'
fil = 'D:/Ex2_Projects/Resumes/Annu_Resume_28.pdf'
# folder_path = 'data/resumes'
# folder_path = 'P:/Bhagyashri/Resume'
print(fil)
text = tika_text_extraction(fil)

# process_file(fil)

skill_date_map(text)
# process_all_files_in_folder(folder_path)

def get_common_words(str1, str2):
    # Tokenize the strings into words
    words1 = str1.split()
    words2 = str2.split()
    
    # Find the common words
    common_words = [word for word in words1 if word in words2]
    
    return ' '.join(common_words)
from fuzzywuzzy import fuzz

def check_similarity(str1, str2):
    # Compute the similarity ratios
    ratio = fuzz.ratio(str1, str2)
    partial_ratio = fuzz.partial_ratio(str1, str2)
    token_sort_ratio = fuzz.token_sort_ratio(str1, str2)
    token_set_ratio = fuzz.token_set_ratio(str1, str2)
    
    # Print the similarity scores
    print(f"Ratio: {ratio}")
    print(f"Partial Ratio: {partial_ratio}")
    print(f"Token Sort Ratio: {token_sort_ratio}")
    print(f"Token Set Ratio: {token_set_ratio}")

# Example usage
str1 = "fullstack developer intern"
str2 = "full developer"

# check_similarity(str1, str2)
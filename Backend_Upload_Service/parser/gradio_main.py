import spacy
from spacy.matcher import Matcher
from text_extractor import extract_text_from_pdf, divide_resume_sections, tika_text_extraction,extract_from_docx
from skills_Extractor import extract_skills
from edu_extract import extract_edu, education_info, extract_degree
from projects_extractor import projects_extraction
# from text_extractor import extract_text_from_pdf, divide_resume_sections
# from skills_Extractor import extract_skills
# from edu_extract import extract_edu, education_info, extract_degree
# from projects_extractor import projects_extraction


import traceback
import requests
import json
from collections import OrderedDict

import re

# from api\data\resumes\resume.pdf


# D:\Ex2_Projects\TalenTrack\api\parser\data\resumes\resume.pdf
# D:\Ex2_Projects\TalenTrack\api\data\resumes\resume.pdf


nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)


job_roles_suffix = [
        "intern",
        "trainee",
        "internship" ,
        "analyst",
        "developer",
        "manager",
        "engineer",
        "consultant",
        "designer",
        "specialist",
        "coordinator",
        "administrator",
        "executive",
        "assistant",
        "supervisor",
        "scientist",
        "specialist",
        "technician",
        "associate",
        "officer",
        # "leader",
        "expert",
        "advisor",
        "strategist",
        "resources",
        "tester",
        "lead",
        # "management",
        # "owner"
    ]


def extract_name(resume_text):

    # print(resume_text[:1000])
    # print(resume_text)
    global job_roles_suffix

    

    patt = re.compile(r'(?<=\b[A-Z]) (?=[A-Z]\b)')
    
    # Replace single spaces with no space
     # Replace single spaces with no space

    # print(resume_text)
    text = patt.sub('', resume_text.title())
    text = text[:800].lower().replace("curriculam","")
    text = text.replace("curriculum","")
    text = text.replace("vitae","")
    text = text.replace("resume"," ")
    text = text.replace("com"," ")
    text = text.replace("   "," ")

    
    text = text.replace("  "," ")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # text = 
    nlp_text = nlp(text.title())
    sents = []
    for sent in nlp_text.sents:
        # if len(sent.text.split())==1:
        sents+=sent.text.split()
            # print(sent.text.split())
    text = " ".join(i for i in sents)
    

    
    # print(text)

    # for token in nlp_text:
    #     print(token, token.dep_, token.pos_)

    # print(text)

    person = []
    for ent in nlp_text.ents:

        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_=="PERSON":
            person.append(" ".join(ent.text.split()[:3]))

        if len(person)>0:
            break
    # print(person)

    

    # pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    pattern = [{"POS": {"IN": ["NOUN", "PROPN"]}}, {"IS_SPACE": True, "OP": "*"},{"POS": "PROPN"}, {"POS": {"IN": ["PROPN"]},"OP": "*"}]
    # pattern = [{"POS": {"IN": ["NOUN", "PROPN"]}},{"IS_ALPHA": True, "LENGTH": 1, "OP": "*"}, {"IS_SPACE": True, "OP": "*"},{"IS_ALPHA": True, "LENGTH": 1, "OP": "*"}, {"POS": "PROPN"}, {"POS": {"IN": ["PROPN"]},"OP": "*"}]
    matcher.add("NAME", patterns=[pattern])
    matches = matcher(nlp_text)

    spans=[]
    for match_id, start, end in matches:
        
        span = nlp_text[start:end]

        check_span = len(span.text.split())

        # spans.append(span.text)
        spans.append(span.text.replace("\n","") if len(span.text.replace("\n","").split())==check_span else span.text.replace("\n"," ") )
        # return span.text
    # print(spans)

    filtered = []

    for s in spans[:10]:

        flag = True
        for word in s.lower().split():
            if word in job_roles_suffix:
                flag = False
        if flag:
            filtered.append(s)
                
    

    # print(filtered)




    # if person :
    #     inter = list(set(person).intersection(set(spans)))
    #     # print(inter)
    #     # print(spans)
    #     if inter:
    #         return inter[0]
    #     elif spans:
    #         return spans[0]
    #     else:
    #         return None
    # elif spans:
    #     return spans[0]
    # else: return None       
    if filtered:
        return filtered[0] 
    else:
        return None
def extract_name_print(resume_text):
    patt = re.compile(r'(?<=\b[A-Z]) (?=[A-Z]\b)')
    
    # Replace single spaces with no space
    text = patt.sub('', resume_text)
    text = text.replace("   "," ")
    text = text.replace("  "," ")
    # print(text)
    text = text[:800].lower().split()
    nlp_text = nlp(" ".join(i.capitalize() for i in text))


    # for token in nlp_text:
    #     print(token, token.dep_, token.pos_)

    person = []
    for ent in nlp_text.ents:

        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_=="PERSON":
            person.append(" ".join(ent.text.split()[:3]))

        if len(person)>0:
            break
    # print(person)

    

    # pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    pattern = [{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": "PROPN"}, {"POS": {"IN": ["PROPN"]},"OP": "*"}]
    matcher.add("NAME", patterns=[pattern])
    matches = matcher(nlp_text)

    spans=[]
    for match_id, start, end in matches:
        
        span = nlp_text[start:end]
        spans.append(span.text)
        # return span.text

    if person :
        inter = list(set(person).intersection(set(spans)))
        # print(inter)
        # print(spans)
        if inter:
            return inter[0]
        elif spans:
            return spans[0]
        else:
            return "Name"
    elif spans:
        return spans[0]
    else: return "Name"        

    # return "name"


# =============================================Phone==================

def extract_mobile_number(text):
    phone = re.findall(
        re.compile(
            r"(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4,5})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"
        ),
        text,
    )
    phn_no = []
    if phone:
        for p in phone:
            number = "".join(p)
            if len(number) > 10:
                phn_no.append("+" + number)
            else:
                phn_no.append(number)
    return phn_no


#  ====================================EMAILS ====================


def extract_email(text):
    patterns = [r"[a-z0-9A-Z!#$%&*()-_+,./~]+@[^\s]+"]

    for pattern in patterns:
        email_regex = re.compile(pattern)
        emails = set(email_regex.findall(text))
        # for email in emails:
        # print(email)
    return list(emails)


#  ====================================URLS ====================


def extract_urls(text):

    url_pattern1 = r"((https?://)?(www\.)?([a-zA-Z]+)\.com/([^/\s]+)/?([^\s]+)?)"
    # url_pattern1 = r"(https?://)?(www\.)?([a-zA-Z]+)\.com/([^/\s]+)/?([^\s]+)?"
    url_pattern2 = (
        r"(https?:\/\/|www\.)([a-z0-9A-Z_]+)\.([a-z0-9A-Z_]+)?(com)?\.?([a-z0-9A-Z]+)?"
    )
    links = re.findall(url_pattern1, text)
    links += re.findall(url_pattern2, text)
    links = set(links)
    urls = {}
    

    # print(links)

    for i, link in enumerate(links):
        # urls[link[2]] = "/".join(l for l in link if l != "")
        urls[link[3]] = link[0]

    # print(urls)
    return urls


def extract_date_ranges(text):
    # Define the regular expression pattern

    # print(text)
    # pattern = r"\b(([a-zA-Z]+(\s?\d\d?)?)?,?\s?\d{4})\s?-?–?–?‑?(to)?\s?((([a-zA-Z]+(\s?\d\d?)?)?,?\s\d{4})|Present|Till Date|Current|current|present)"
    pattern = r"\b(([a-zA-Z]+’?'?(\s?\d\d?)?)?,?\s?\d{2,4})\s?-?–?–?‑?(to)?\s?((([a-zA-Z]+’?'?(\s?\d\d?)?)?,?\s?\d{2,4})|Present|Till Date|Current|current|present)"
    pattern2 = r"\b(([a-zA-Z]+\’?\'?\d{2}\s?)\-(\s?[a-zA-Z]+\’?\'?\d{2}))\b"
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    matches2 = re.findall(pattern2, text)

    # print("matches",matches2)

    # Extracted date ranges
    extracted_ranges = []
    for match in matches:
        extracted_ranges.append([match[0], match[4]])
    # print("extracted ranges:",extracted_ranges)

    for match in matches2:
        extracted_ranges.append([match[1], match[2]])

    return extracted_ranges





def extract_date2(text):
    pattern1 = r"\b(([a-zA-Z]+’?'?(\s?\d\d)?),?\s?20\d{2})\s?-?–?–?‑?(to)?\s?((([a-zA-Z]+’?'?(\s?\d\d?)?),?\s?20\d{2})|(Present|Till Date|Current|current|present|ongoing))"
    pattern2 = r"(20\d\d\s?)(-|–|to)(\s?20\d\d)"
    single_date_pattern1 = r"(\d\d)(\/|-)(\d\d)(\/|-)(\d\d\d\d)"


    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)
    matches3 = re.findall(single_date_pattern1, text)

    print(matches3)

    dates1 = []
    dates2 = []
    dates3 = []

    if matches1:
        for match in matches1:
            dates1.append([match[0],match[4]])
    else:
        pass
  
    for match in matches2:
        dates2.append([match[0],match[2]])
    for match in matches3:
        dates3.append([match[0],match[2],match[4]])   


    return dates1, dates2, dates3


from datetime import datetime


def to_date(start_date, end_date):

    start_date = re.sub(r"[\"'`’]" ," ", start_date )
    end_date = re.sub(r"[\"'`’]" ," ", end_date )

    # start_date, end_date = start_date.split(), end_date.split()

    # print(start_date, end_date)
    try:

        if len(start_date.split())==2:
        # Parse the dates into datetime objects
            start_date = start_date.split()
            start_date[0]=start_date[0][:3]
            if len(start_date[1])==2:
                start_date[1]= "20"+start_date[1]
            start_date = " ".join(start_date)
            # print(start_date)
            start_date_obj = datetime.strptime(start_date.title(), "%b %Y")
        else:
            start_date_obj = datetime.strptime(start_date.title(), "%Y")
            

        if len(end_date.split())==2:
            end_date = end_date.split()
            end_date[0]=end_date[0][:3]
            if len(end_date[1])==2:
                end_date[1]= "20"+end_date[1]
            end_date = " ".join(end_date)
            # print(end_date)
            end_date_obj = datetime.strptime(end_date.title(), "%b %Y")
        else:
            if end_date.lower() in ["present", "current"]:
                end_date_obj = datetime.now()
            else:
                end_date_obj = datetime.strptime(end_date.title(), "%Y")

        # Calculate the difference in months
        months_diff = (end_date_obj.year - start_date_obj.year) * 12 + end_date_obj.month - start_date_obj.month

        # print("Duration in months:", months_diff)
        return months_diff/12
    except ValueError:
        # print("Invalid date format. Please use a format like 'Jun 2022'.")
        return 0
    
def latest_date(dates1,dates2):
    date1 = re.sub(r"[\"'`’]" ," ", dates1 )
    date2 = re.sub(r"[\"'`’]" ," ", dates2 )
    try:

        if len(date1.split())==2:
        # Parse the dates into datetime objects
            date1 = date1.split()
            date1[0]=date1[0][:3]
            if len(date1[1])==2:
                date1[1]= "20"+date1[1]
            date1 = " ".join(date1)
            # print(date1)
            date1_obj = datetime.strptime(date1.title(), "%b %Y")
        else:
            date1_obj = datetime.strptime(date1.title(), "%Y")
            

        if len(date2.split())==2:
            date2 = date2.split()
            date2[0]=date2[0][:3]
            if len(date2[1])==2:
                date2[1]= "20"+date2[1]
            date2 = " ".join(date2)
            # print(date2)
            date2_obj = datetime.strptime(date2.title(), "%b %Y")
        else:
            if date2.lower() in ["present", "current"]:
                date2_obj = datetime.now()
            else:
                date2_obj = datetime.strptime(date2.title(), "%Y")
        
        if date1_obj > date2_obj:
            return dates1
        elif date1_obj < date2_obj:
            return dates2
        else:
            return "None"
    except:
        return "None"

    pass


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')

def remove_prepositions(query):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(query)
    filtered_query = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_query)

from geotext import GeoText

def extract_locations(text):
    # capitalized_text =[word.capitalize() for word in text.split()]
    # print(capitalized_text)

    text = remove_prepositions(text)
    # print(text)

    cities = []
    countries = []

    for i in text.split():

        if i in ["of","Of","march","March"]:
            continue

        places = GeoText(i.capitalize())
        if places.cities:
            cities.append(i)
        elif places.countries:
            countries.append(i)


    # Extract states, cities, and countries
    # states = places.states
        # return states, cities, countries
    return list(set(cities))


import locationtagger

nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_locations2(resume_text):
    place_entity = locationtagger.find_locations(text=resume_text)
 


    country_cities = dict(place_entity.country_cities)

    # print(place_entity.country_cities)
    print(place_entity.regions)
    

    if "India" in country_cities:
        print("india")
        return country_cities["India"]
    else:
        return []
   


def extract_prev_job_roles(text):
    job_roles = [
        "intern",
        "trainee",
        "internship" ,
        "analyst",
        "developer",
        "manager",
        "engineer",
        "consultant",
        "designer",
        "specialist",
        "coordinator",
        "administrator",
        "executive",
        "assistant",
        "supervisor",
        "scientist",
        "specialist",
        "technician",
        "associate",
        "officer",
        # "leader",
        "expert",
        "advisor",
        "strategist",
        "resources",
        "tester",
        "lead",
        # "management",
        # "owner"
    ]

    text = text.replace("\n", " ")
    text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("-","")
    text = text.replace("js","")
    text = text.replace("  "," ")
    # print(text)
    matcher = Matcher(nlp.vocab)
    # pattern = [ {"POS": {"IN": ["PROPN"]},"DEP": "compound", "OP": "*"},
    #              {"POS": {"IN": ["NOUN"]},"DEP": "compound", "OP": "*"},
    #              {"POS": {"IN": ["NOUN", "PROPN"]},"DEP": "compound", "OP": "*"},
    #             {"POS": {"IN": ["NOUN", "PROPN"]},"DEP": "compound", "OP": "*"},]
    pattern = [
    {"POS": {"IN": ["PROPN", "NOUN","VERB"]}, "DEP": {"IN": ["compound", "nsubj","ROOT"]}, "OP": "*"},
    {"POS": {"IN": ["PROPN", "NOUN","VERB"]}, "DEP": {"IN": ["compound", "nsubj"]}, "OP": "*"},
    {"POS": {"IN": ["PROPN", "NOUN","VERB"]}, "DEP": {"IN": ["compound", "nsubj"]}, "OP": "*"},
    {"POS": {"IN": ["PROPN", "NOUN","VERB"]}, "DEP": {"IN": ["compound", "nsubj","appos","dep", "ROOT","nmod"]}, "OP": "*"}
]
    matcher.add("PROPER_NOUNS", [pattern], greedy="LONGEST")
    doc = nlp(text)

    # print(text)

    for token in doc:
        print(token, token.dep_, token.pos_)

    jobs = []
    matches = matcher(doc)
    longest_matches = []
    seen_tokens = set()

    for match_id, start, end in sorted(matches, key=lambda x: (x[1], x[2] - x[1]), reverse=True):
        if not any(tok in seen_tokens for tok in range(start, end)):
            longest_matches.append((match_id, start, end))
            seen_tokens.update(range(start, end))

    
    for match in longest_matches:
        check_role = str(doc[match[1] : match[2]]).lower()
        print(check_role)

        for role in job_roles:
            if role in check_role.split() :
                # print(check_role.split(), role)

                role_arr = check_role.split()
                
                j_r = " ".join(role_arr[role_arr.index(role)-2:role_arr.index(role)+1]) if role_arr.index(role)!=0 and len(role_arr)>3 else check_role
                
                jobs.append(re.sub(re.escape("experience"), '', j_r, flags=re.IGNORECASE) )
    

    jobs = list(OrderedDict.fromkeys(jobs))

    
    for j in job_roles:
        if len(jobs)>1:
            if j in jobs:
                jobs.remove(j)

    
    # print(jobs)
    # print(list(OrderedDict.fromkeys(jobs)))
    # print("uuuuu",OrderedDict.fromkeys(jobs))
    return jobs



def work_city_mapping(text, job_roles,cities):
    mapped_cities = {}

    # text = re.sub(r"[\[\](){}<>\"'`_\\n]", " ", text)
    # print(cities)
    for role in job_roles:         
        job_pos = text.find(role)  
        min_distance = float('inf')
        closest_city = None
        if cities:
            
            for city in cities:   
                dist = abs(job_pos - text.find(city))
                # print(role, city, dist)             
                if dist < min_distance:
                    min_distance = dist
                    closest_city = city
            mapped_cities[role]=closest_city


    return mapped_cities



def work_ex_date_mapping(text, job_roles, dates):
    mapped_work = {}
    # print("dates", dates)
    # print(text)

    mapped_dist = {}

    if dates:
        for date in dates:
            min_distance = float('inf')
            closest_role = None

            if job_roles:
                # print(job_roles)

                for role in job_roles:

                    dist =0
                    if len(role)<3:
                        continue


                    #     continue

                    for r in role.split():
                        dist += abs(text.find(date[0]) - text.find(r))
                    if role in mapped_work:
                        if mapped_dist[role]<dist:
                            continue


                    # print(role, date[0], dist)
                    if dist < min_distance:
                        min_distance = dist
                    
                        closest_role = role
                mapped_work[closest_role]=date
                mapped_dist[closest_role]=dist
            # print(mapped_work)

       

    return mapped_work


def extract_work_ex(text):
    # text = divide_resume_sections(text)["Experience"].lower()
    # print(text)
   
    job_roles = list(set(extract_prev_job_roles(text)))
    # print("yolo",job_roles)
    #   work_ex_section =
    company_name = "unknown"
    dep_name = "unknown"
    location = "unknown"
    # current_job_status = False
    job_details = "NA"

    work_ex = {}
    dates = extract_date_ranges(text)
    # print(dates)
    cities  = extract_locations(re.sub(r"[\[\](){}<>\"'`_]", " ", text))
    # print(job_roles)
    # print(dates)
    # print(cities)
    # print(text)
    # if len(dates)<len(job_roles):



    mapped_work = work_ex_date_mapping(text, job_roles, dates)
    mapped_cities = work_city_mapping(text,job_roles,cities)
    # print(mapped_cities)

    recent_job_date = "apr 2001"
    recent_job = ""
    for i in range(len(job_roles)):
        
        if job_roles[i] :

            work_ex[job_roles[i]]=[
                    company_name,
                    dep_name,
                    job_roles[i],
                    mapped_work[job_roles[i]][0] if job_roles[i] in mapped_work else "",
                    mapped_work[job_roles[i]][1] if job_roles[i] in mapped_work else "",
                    mapped_cities[job_roles[i]] if job_roles[i] in mapped_cities else "",
                    True if job_roles[i] in mapped_work and mapped_work[job_roles[i]][1].lower() in ["current", "present"] else False ,
                    job_details,
                    
                ]
            


            work_ex[job_roles[i]].append(to_date(work_ex[job_roles[i]][3],work_ex[job_roles[i]][4]) )
            # print("check recent", recent_job_date,work_ex[job_roles[i]][4])
            recent_job_date = latest_date(recent_job_date,work_ex[job_roles[i]][4] )
            # print("check recent",recent_job_date)
            if recent_job_date==work_ex[job_roles[i]][4]:
                
                recent_job_date = work_ex[job_roles[i]][4]
                recent_job = job_roles[i]

    if recent_job in work_ex:
        work_ex[recent_job][6]= True                    
            

    return work_ex


def summary_parser(text):
    text = text[:1000]
    # print(text)
    skills = extract_skills(text)
    roles = extract_prev_job_roles(text)
    exp_pattern = r"(\d.?\d?)\s?(\+|plus)?"
    exp = 0

    matches = re.findall(exp_pattern, text)
  
    if matches:
        exp = matches[0][0]
    if roles:

        return [roles[0], exp, skills]
    else: 
        return ["None", exp, skills]
    


def extract_urls2(text):
    # Regular expression pattern for URLs
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    urls = re.findall(url_pattern, text)
    return urls





def contact_details(text):
    Phn_no=str(extract_mobile_number(text)),
    Email= list(extract_email(text)),
    Urls=dict(extract_urls(text)),

# import magic

# def check_file_type(file_path):
#     # Create a magic.Magic object
#     mime = magic.Magic(mime=True)
    
#     # Check the file type
#     file_type = mime.from_file(file_path)
#     return file_type


def main(filePath):
    # for i in range(2,19,1):
# <<<<<<< HEAD
    #
    #     file = "resume"+str(i)+".pdf"
    # print(filePath+file)

    # print(check_file_type(filePath))
    try:
        # if check_file_type(filePath) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        #     text = extract_from_docx(filePath)

        # elif check_file_type(filePath)=='application/pdf':
        #     text = ""
        #     for page in extract_text_from_pdf(filePath):        
        #         text += " " + page
        # else:
            text = tika_text_extraction(filePath)
    except Exception as e:
        traceback.print_exc()
        # print(f"An error occurred: {e}")
        return None
    

    
    # check_text = text.replace(" ","").replace("\n","").split(" ")
    check_text = text.replace(" ","").replace('\x0c',"")
    # check_text = text.split(" ")
    emergency_text = tika_text_extraction(filePath)
    # print(emergency_text)

    # print(len(check_text))
    # print(check_text)


    # print(check_text)
    if check_text.replace("\n","") == "":
        text = tika_text_extraction(filePath)
    else:
        # print(check_text.replace("\n","1"))
        print("popat")


    # print(text)str(extract_name(text)),
    file_name=filePath

    try:
        data = {
            "LogId":1,
            "Resume_name":file_name.split("/")[-1],
            "Summary":summary_parser(divide_resume_sections(text)["Summary"]),        
            "Name": str(extract_name(text)),
            "Phn_no": list(extract_mobile_number(emergency_text)),
            "Email":list(extract_email(emergency_text)),
            "Urls":dict(extract_urls(emergency_text)),
            # "Education":extract_edu(text),
            "Education":dict(education_info(emergency_text)),
            "Skills":extract_skills(emergency_text),
            "Degree":(extract_degree(text)),
            # "Work Experience":extract_prev_job_roles(text),
            "Work_Experience":dict(extract_work_ex(divide_resume_sections(emergency_text)["Experience"].lower())),
            "Projects":list(projects_extraction(divide_resume_sections(text)["Projects"])),
            "Locations":extract_locations2(emergency_text)
        }

        if data["Work_Experience"]=={}:
            # print("yolo3")
            data["Work_Experience"] = dict(extract_work_ex(divide_resume_sections(emergency_text)["Experience"].lower()))
    # =======
        if data["Work_Experience"]=={}:
            data["Work_Experience"]  = dict(extract_work_ex(emergency_text))


        # file = "resume"+".pdf"
        # try:
        #     url = "http://localhost:8000/alldata"
        #     # url = " http://127.0.0.1:8000/alldata"
        #     headers = {"Content-type": "application/json", "Accept": "application/json"}

        #     json_object = json.dumps(data, indent = 4) 
        #     # print(json_object)


        #     response = requests.post(
        #         url,
        #         json=data,
        #         headers=headers,
        #     )
        #     response.raise_for_status()  # Radata=json.dumps(data), headers=headersise an exception for HTTP errors
        #     print("Data sent successfully:", response.json())
        #     # return response.json()
        # except requests.exceptions.HTTPError as http_err:
        #     print(f"HTTP error occurred: {http_err}")
        # except Exception as err:
        #     print(f"An error occurred: {err}")

        print("\n\n\n\ninside main func\n")
        for key , value in data.items():
            print(f'{key} : {data[key]}', end="\n")
        print("\n\n\n\n\n")
        # print("LOCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
        return data


    except Exception as err:
        traceback.print_exc()
        print(f"An error occurred in data extraction: {err}")
        return None
    


# main("data/resumes/resume12.pdf")
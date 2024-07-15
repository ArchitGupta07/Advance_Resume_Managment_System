import dateparser.search
import spacy
from spacy.matcher import Matcher
from text_extractor import extract_text_from_pdf, divide_resume_sections, tika_text_extraction,extract_from_docx
from skills_Extractor import extract_skills,extract_skills_for_local
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
from fb_duckling import Duckling
from new_dateExtractor import extract_locations_from_text

import re

from misc_funcs import extract_locations2

# from api\data\resumes\resume.pdf


# D:\Ex2_Projects\TalenTrack\api\parser\data\resumes\resume.pdf
# D:\Ex2_Projects\TalenTrack\api\data\resumes\resume.pdf


nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)


def extract_name(resume_text):
    patt = re.compile(r'(?<=\b[A-Z]) (?=[A-Z]\b)')
    
    # Replace single spaces with no space
    text = patt.sub('', resume_text)
    text = text.replace("   "," ")
    text = text.replace("  "," ")
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
def extract_name_print(resume_text):
    patt = re.compile(r'(?<=\b[A-Z]) (?=[A-Z]\b)')
    
    # Replace single spaces with no space
    text = patt.sub('', resume_text)
    text = text.replace("   "," ")
    text = text.replace("  "," ")
    print(text)
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
    print(person)

    

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
        print(inter)
        print(spans)
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

    url_pattern1 = r"(https?://)?(www\.)?([a-zA-Z]+)\.com/([^/\s]+)/?([^\s]+)?"
    url_pattern2 = (
        r"(https?:\/\/|www\.)([a-z0-9A-Z_]+)\.([a-z0-9A-Z_]+)?(com)?\.?([a-z0-9A-Z]+)?"
    )
    links = re.findall(url_pattern1, text)
    links += re.findall(url_pattern2, text)
    urls = {}
    

    for i, link in enumerate(links):
        urls[link[2]] = "/".join(l for l in link if l != "")

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

from datetime import datetime
import re

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

# Function to find all positions of a word in the text
def find_positions(word, text):
    return [m.start() for m in re.finditer(word, text, re.IGNORECASE)]

def get_closest_location_to_present(text,words):
    # text = """
    # experience 

    # idc technologies pvt. ltd noida
    # flutter developer (sde-2) 14/02/ 2023 – present

    # craft silicon loan banking (under develop)

    #  working with responsive ui for mobile and tablet support.

    #  flutter localization, authentication biometric, face & pin code.

    # another example line with Present keyword
    # """

    # # Define the array of words to check
    # words = ['manage', 'noida', 'mobile']

    

    # Find positions of 'present' in lowercase
    present_positions = find_positions('present', text.lower())

    # Initialize a dictionary to hold the minimum distance for each word
    min_distances = {word: float('inf') for word in words}

    # Iterate over each word and find the minimum distance to 'present'
    for word in words:
        word_positions = find_positions(word, text.lower())
        for p_pos in present_positions:
            for w_pos in word_positions:
                distance = abs(p_pos - w_pos)
                if distance < min_distances[word]:
                    min_distances[word] = distance

    if min_distances:
        # Find the word with the smallest distance
        closest_word = min(min_distances, key=min_distances.get)

        # Print the closest word
        print(f"The word closest to 'present' is: {closest_word} for file name: {filename}")

def get_closest_location_to_till_date(text,words):
    # text = """
    # experience 

    # idc technologies pvt. ltd noida
    # flutter developer (sde-2) 14/02/ 2023 – present

    # craft silicon loan banking (under develop)

    #  working with responsive ui for mobile and tablet support.

    #  flutter localization, authentication biometric, face & pin code.

    # another example line with Present keyword
    # """

    # # Define the array of words to check
    # words = ['manage', 'noida', 'mobile']

    

    # Find positions of 'present' in lowercase
    present_positions = find_positions('till date', text.lower())

    # Initialize a dictionary to hold the minimum distance for each word
    min_distances = {word: float('inf') for word in words}

    # Iterate over each word and find the minimum distance to 'present'
    for word in words:
        word_positions = find_positions(word, text.lower())
        for p_pos in present_positions:
            for w_pos in word_positions:
                distance = abs(p_pos - w_pos)
                if distance < min_distances[word]:
                    min_distances[word] = distance

    if min_distances:
        # Find the word with the smallest distance
        closest_word = min(min_distances, key=min_distances.get)

        # Print the closest word
        print(f"The word closest to 'till date' is: {closest_word} for file name: {filename}")

def get_closest_location_to_current(text,words):
    # text = """
    # experience 

    # idc technologies pvt. ltd noida
    # flutter developer (sde-2) 14/02/ 2023 – present

    # craft silicon loan banking (under develop)

    #  working with responsive ui for mobile and tablet support.

    #  flutter localization, authentication biometric, face & pin code.

    # another example line with Present keyword
    # """

    # # Define the array of words to check
    # words = ['manage', 'noida', 'mobile']

    

    # Find positions of 'present' in lowercase
    present_positions = find_positions('current', text.lower())

    # Initialize a dictionary to hold the minimum distance for each word
    min_distances = {word: float('inf') for word in words}

    # Iterate over each word and find the minimum distance to 'present'
    for word in words:
        word_positions = find_positions(word, text.lower())
        for p_pos in present_positions:
            for w_pos in word_positions:
                distance = abs(p_pos - w_pos)
                if distance < min_distances[word]:
                    min_distances[word] = distance

    if min_distances:
        # Find the word with the smallest distance
        closest_word = min(min_distances, key=min_distances.get)

        # Print the closest word
        print(f"The word closest to 'current' is: {closest_word} for file name: {filename}")


def get_closest_location_to_email(text,words,email):
    email = email.lower()
    # text = """
    # experience 

    # idc technologies pvt. ltd noida
    # flutter developer (sde-2) 14/02/ 2023 – present

    # craft silicon loan banking (under develop)

    #  working with responsive ui for mobile and tablet support.

    #  flutter localization, authentication biometric, face & pin code.

    # another example line with Present keyword
    # """

    # # Define the array of words to check
    # words = ['manage', 'noida', 'mobile']

    

    # Find positions of 'present' in lowercase
    present_positions = find_positions(email, text.lower())

    # Initialize a dictionary to hold the minimum distance for each word
    min_distances = {word: float('inf') for word in words}

    # Iterate over each word and find the minimum distance to 'present'
    for word in words:
        word_positions = find_positions(word, text.lower())
        for p_pos in present_positions:
            for w_pos in word_positions:
                distance = abs(p_pos - w_pos)
                if distance < min_distances[word]:
                    min_distances[word] = distance

    if min_distances:
        # Find the word with the smallest distance
        closest_word = min(min_distances, key=min_distances.get)

        # Print the closest word
        print(f"The word closest to {email} is: {closest_word} for file name: {filename}")


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
        "owner"
    ]

    text = text.replace("\n", " ")
    text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("-","")
    # print(text)
    matcher = Matcher(nlp.vocab)
    # pattern = [ {"POS": {"IN": ["PROPN"]},"DEP": "compound", "OP": "*"},
    #              {"POS": {"IN": ["NOUN"]},"DEP": "compound", "OP": "*"},
    #              {"POS": {"IN": ["NOUN", "PROPN"]},"DEP": "compound", "OP": "*"},
    #             {"POS": {"IN": ["NOUN", "PROPN"]},"DEP": "compound", "OP": "*"},]
    pattern = [
    {"POS": {"IN": ["PROPN", "NOUN"]}, "DEP": {"IN": ["compound", "nsubj"]}, "OP": "*"},
    {"POS": {"IN": ["PROPN", "NOUN"]}, "DEP": {"IN": ["compound", "nsubj"]}, "OP": "*"},
    {"POS": {"IN": ["PROPN", "NOUN"]}, "DEP": {"IN": ["compound", "nsubj"]}, "OP": "*"},
    {"POS": {"IN": ["PROPN", "NOUN"]}, "DEP": {"IN": ["compound", "nsubj","appos","dep", "ROOT","nmod"]}, "OP": "*"}
]
    matcher.add("PROPER_NOUNS", [pattern], greedy="LONGEST")
    doc = nlp(text)

    # print(text)

    # for token in doc:
    #     print(token, token.dep_, token.pos_)

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
        # print(check_role)

        for role in job_roles:
            if role in check_role.split() :
                # print(check_role.split(), role)

                
                j_r = " ".join(check_role.split()[check_role.split().index(role)-2:check_role.split().index(role)+1]) if check_role.split().index(role)!=0 else check_role
                
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
                print(job_roles)

                for role in job_roles:

                    dist =0
                    if role in mapped_work:
                        continue

                    for r in role.split():
                        dist += abs(text.find(date[0]) - text.find(r))
                    print(role, date[0], dist)
                    if dist < min_distance:
                        min_distance = dist
                        closest_role = role
                mapped_work[closest_role]=date
                mapped_dist[closest_role]=dist





    # for role in job_roles:

         
    #     job_pos = text.find(role)  
    #     min_distance = float('inf')
    #     closest_date = None
    #     if dates:
    #         for date in dates:                
    #             dist = abs(job_pos - text.find(date[0]))
    #             # print(role, date, dist)
    #             if dist < min_distance:
    #                 min_distance = dist
    #                 closest_date = date
    #         mapped_work[role]=closest_date
                
        
        
       

    return mapped_work


def find_present_line(text):

    # Split the text into lines
    lines = text.split('\n')
    arr = []

    # Iterate through the lines and print the ones that contain 'present' in any case
    for line in lines:
        if 'present' in line.lower():
            print('line with present: ',line.strip())
            arr.append(line.strip())
    return arr


def extract_work_ex(text):
    # text = divide_resume_sections(text)["Experience"].lower()
    print('work exp text: ',text)
   
    job_roles = list(set(extract_prev_job_roles(text)))
    print("yolo",job_roles)
    #   work_ex_section =
    company_name = "unknown"
    dep_name = "unknown"
    location = "unknown"
    # current_job_status = False
    job_details = "NA"

    latest_date_line = find_present_line(text)

    for date in latest_date_line:
        extract_date_ranges(date)

    work_ex = {}
    dates = extract_date_ranges(text)
    print('dates extracted: ', dates);
    if len(dates)>0 and len(dates[0])>0:
        maxDate = dates[0][0];
        for i in dates:
            maxDate = latest_date(maxDate,i[0])
            maxDate = latest_date(maxDate,i[1])
        
        print('max date is: ', maxDate)
        

    print(dates)
    # cities  = extract_locations(re.sub(r"[\[\](){}<>\"'`_]", " ", text))
    cities = extract_locations(text)
    # get_closest_location(text,cities)

    # print('cities are: ', cities)
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


def summary_parser(text,data):

    print('This is data: ',data,':::: Data Ends')

    dummy = re.sub(r'\s+', '', text);

    if(len(dummy)<20):
        skillArr = data['Skills']
        text = f"{data['Name']} is a {data['Work Experience'][0]} with proficiency in "
        for i in skillArr:
            text += i+', '
        text = text[:-2]
    else:
        print('ssssss*****************',repr(text),'**************ssssss')
        index = text.find(' \n\n')
        
        # # Define the pattern to find \n\n not preceded by 'SUMMARY' followed by any number of spaces
        # pattern = r'(?<!\bSUMMARY\s*)\n\n'

        # # Find the match
        # match = re.search(pattern, text, re.IGNORECASE)

        # # Get the index if a match is found
        # index = match.start() if match else -1

        # print('index::',index)
        
        text = text[:index]
    
        
    print('Summary Starts**********************************\n ', text)
    print('\nSummary Ends************************************')


    if text:
        return text
    else:
        return None
    # text = text[:1000]
    # print(text)
    # skills = extract_skills_for_local(text)
    # roles = extract_prev_job_roles(text)
    # exp_pattern = r"(\d.?\d?)\s?(\+|plus)?"
    # exp = 0

    # matches = re.findall(exp_pattern, text)
  
    # if matches:
    #     exp = matches[0][0]
    # if roles:

    #     return [roles[0], exp, skills]
    # else: 
    #     return ["None", exp, skills]
    
    







def contact_details(text):
    Phn_no=str(extract_mobile_number(text)),
    Email= list(extract_email(text)),
    Urls=dict(extract_urls(text)),

import magic

def check_file_type(file_path):
    # Create a magic.Magic object
    mime = magic.Magic(mime=True)
    
    # Check the file type
    file_type = mime.from_file(file_path)
    return file_type

def find_dates(text):
    # duckling = Duckling(locale="en_US")
    # duckling("All work and no play makes jack@gmail.com a dull boy 0102030405")
    # Define a list of regex patterns for different date formats

    print('this is text:[',text,']')
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',                    # 12-05-2023, 12/05/23, etc.
        r'\b\d{1,2}\s[ADFJMNOSadfjmnos]\w*\s\d{2,4}\b',           # 12 Dec 2023, 12 December 23, etc.
        r'\b[ADFJMNOSadfjmnos]\w*\s\d{1,2},?\s\d{2,4}\b',         # December 12, 2023, Dec 12, 23, etc.
        r'\b\d{1,2}(st|nd|rd|th)?\s[ADFJMNOSadfjmnos]\w*\s\d{2,4}\b', # 12th Dec 2023, 1st January 23, etc.
        r'\b[ADFJMNOSadfjmnos]\w*\s\d{1,2}(st|nd|rd|th)?,?\s\d{2,4}\b', # Dec 12th, 2023, December 1st, 23, etc.
    ]
    # Combine all patterns into a single pattern
    combined_pattern = '|'.join(date_patterns)
    # Compile the combined pattern
    date_regex = re.compile(combined_pattern)
    # Find all matches in the text
    matches = date_regex.findall(text)
    print('these are mactches ::',matches)


    

def main(filePath):
    # for i in range(2,19,1):
# <<<<<<< HEAD
    #
    #     file = "resume"+str(i)+".pdf"
    # print(filePath+file)

    print(check_file_type(filePath))
    try:
        if check_file_type(filePath) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_from_docx(filePath)

        elif check_file_type(filePath)=='application/pdf':
            text = ""
            for page in extract_text_from_pdf(filePath):        
                text += " " + page
        else:
            text = tika_text_extraction(filePath)
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")
        return None
    

    
    # check_text = text.replace(" ","").replace("\n","").split(" ")
    check_text = text.replace(" ","").replace('\x0c',"")
    # check_text = text.split(" ")
    emergency_text = tika_text_extraction(filePath)

    # print(len(check_text))
    # print(check_text)


    # print(check_text)
    if check_text.replace("\n","") == "":
        text = tika_text_extraction(filePath)
    else:
        # print(check_text.replace("\n","1"))
        print("popat")

    print('now')
    find_dates(divide_resume_sections(emergency_text)["Experience"].lower())
    # print(text)str(extract_name(text)),
    file_name=filePath
    data = {

        # s"Resume_name":file_name.split("/")[-1],
        # "Summary":summary_parser(divide_resume_sections(text)["Summary"]),        
        "Name": str(extract_name(text)),
        #s "Phn_no": list(extract_mobile_number(text)),
        # s"Email":list(extract_email(text)),
        # s"Urls":dict(extract_urls(text)),
        # "Education":extract_edu(text),
        # s"Education":dict(education_info(emergency_text)),
        "Skills":extract_skills_for_local(text),
        #s"Degree":(extract_degree(text)),
        "Work Experience":extract_prev_job_roles(text),
        "Work_Experiences":dict(extract_work_ex(divide_resume_sections(emergency_text)["Experience"].lower())),
        #s"Projects":list(projects_extraction(divide_resume_sections(text)["Projects"]))
    }



    emailForLocation = list(extract_email(text))

    print('email for location ',emailForLocation)

    try:
        workExText = divide_resume_sections(emergency_text)["Experience"].lower()
        
        firstExtraction = extract_locations(emergency_text)
        
        print('first extraction of location: ', firstExtraction)
        extractedText = " ".join(firstExtraction)
        new_cities = extract_locations_from_text(extractedText)
        print('new cities!!: ', new_cities)
        print('cities after joinig: ',extractedText.title())
        cities = extract_locations2(extractedText.title())
        
        get_closest_location_to_present(workExText,cities)
        get_closest_location_to_current(workExText,cities)
        get_closest_location_to_till_date(workExText,cities)
        get_closest_location_to_email(workExText,cities,emailForLocation[0])
        print('cities are: ', cities)
    except:
        print('exception is here!!')
    
    

    # summary = summary_parser(divide_resume_sections(text)["Summary"], data), 

    return;

    if data["Work_Experience"]=={}:
        # print("yolo3")
        data["Work_Experience"] = dict(extract_work_ex(divide_resume_sections(emergency_text)["Experience"].lower()))
# =======
    if data["Work_Experience"]=={}:
        data["Work_Experience"]  = dict(extract_work_ex(emergency_text))


        # file = "resume"+".pdf"


    print("\n\n\n\ninside main func\n")
    for key , value in data.items():
        print(f'{key} : {data[key]}', end="\n")
    print("\n\n\n\n\n")

    


    try:
        url = "http://localhost:8000/alldata"
        # url = " http://127.0.0.1:8000/alldata"
        headers = {"Content-type": "application/json", "Accept": "application/json"}

        json_object = json.dumps(data, indent = 4) 
        # print(json_object)


        response = requests.post(
            url,
            json=data,
            headers=headers,
        )
        response.raise_for_status()  # Radata=json.dumps(data), headers=headersise an exception for HTTP errors
        print("Data sent successfully:", response.json())
        # return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


import os
def process_file(filePath):
    # Your function to process each file

    print(check_file_type(filePath))
    try:
        if check_file_type(filePath) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_from_docx(filePath)

        elif check_file_type(filePath)=='application/pdf':
            text = ""
            for page in extract_text_from_pdf(filePath):        
                text += " " + page
        else:
            text = tika_text_extraction(filePath)
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")
        return None
    # print(f"Processing file: {filePath} and name is {str(" ".join(extract_name(text).split()[:2]))}")
    # Add your file processing code here

def process_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  # Ensure it's a file
            process_file(file_path)

# Example usage
folder_path = 'D:/Ex2_Projects/Resumes'
# process_all_files_in_folder(folder_path)


# main("D:/Ex2_Projects/ARMSS_Backend/data/resumes/resume7.pdf")
# main('D:/Ex2_Projects/Resumes/resume33_u.pdf')
filename = ''
for i in range(2,20):
    filename = f"resume{i}.pdf"

    try:

        main(f"../data/resumes/{filename}")
    except Exception as e:
        print(f"a exception {e} occured at: {filename}")
# main("../../data/resumes/resume.pdf")



# text=""
# # for page in extract_text_from_pdf("D:/Ex2_Projects/TalenTrack/api/data/resumes/resume.pdf"):
# for page in extract_text_from_pdf("D:/Archit/Programming_Career/ExSquared/TalenTrack/api/data/resumes/resume.pdf"):
#     text += ' ' + page

# print(extract_work_ex(text))
# print(extract_date_ranges(text))
# print(text)


# print(text)

# print(find_com_urls(text))
# print(extract_education(text))
# print(extract_skills(text))

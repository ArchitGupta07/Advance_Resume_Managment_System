import nltk
import spacy
from spacy.matcher import Matcher
import re
# from spacy.matcher import PhraseMatcher
# from text_extractor import extract_text_from_pdf
from collections import OrderedDict

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

nlp = spacy.load("en_core_web_sm")
 
 
RESERVED_WORDS = [
    'school',
    'college',
    'univers',
    'university',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'kolej',
    'ünivers',
    'okul',
    'vishwavidhyala',
    "vidhyala"

]
 
undergrad = ['college',
    'univers',
    'university',    
    'faculty',
    'institute',]
 
def extract_education(input_text):
    organizations = []
 
    # first get all the organization names using nltk
    for sent in nltk.sent_tokenize(input_text):
        # print(sent, end="\n\n")
        # print(nltk.word_tokenize(sent), end="\n\n")
        # print(nltk.pos_tag(nltk.word_tokenize(sent)), end="\n\n")
        # print(nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))), end="\n\n")
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))
 
    # we search for each bigram and trigram for reserved words
    # (college, university etc...)
    education = set()
    for org in organizations:
        for word in RESERVED_WORDS:
            if org.lower().find(word) >= 0:
                education.add(org)
 
    return education


    


# Load the English NER model
def extract_edu(input_text):

    
    doc = nlp(input_text)


    org_names = OrderedDict()
    for ent in doc.ents:
        # print(ent, ent.label_, "check", end="\n\n")      
        org_name = " ".join(ent.text.split("/"))
        
        if any(word in org_name.lower() for word in RESERVED_WORDS):  
            # org_names.append(org_name.replace("\n",""))
            org_names[re.sub(r'\s+', ' ', org_name.replace("\n",""))] = []
            # org_names.add(org_name)

    # print("Organization Names:",list(set(org_names)))

    return org_names


def extract_degree(text):
    # pattern = r'\b(?:((B|b|M|m)\.[a-zA-Z]{1,5})|BBA|MBA|BCA|MCA|)\b'
    pattern = r'\b(((B|b|M|m)\.[a-zA-Z]{1,5})|BBA|MBA|BCA|MCA|BE|BA|btech)\b'
   

    lines = text.split('\n') 
    deg=[]      
    for line in lines:
        # print(line)
        match1 = list(re.findall(pattern, line, flags=re.IGNORECASE))
        # match2 = list(re.findall(per_pattern, line))


        if match1!=[] and match1[0][0]!="":
            # print(match)
            
            deg.append(match1[0][0].lower())
            # print(match1)
    degree_pattern = [
        {"LOWER": {"IN": ["bachelor", "masters", "phd", "doctorate", "post graduate","diploma"]}},
        {"LOWER": {"IN": ["in", "of"]}, "OP": "?"},
        {"IS_SPACE": True, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
        {"LOWER": {"IN": ["in"]}, "OP": "?"},
        {"IS_SPACE": True, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
    ]
    # print(jobs)

    levels =["bachelor", "masters", "phd", "doctorate", "post graduate","diploma"]

    degree_pattern[0]["LOWER"]["IN"]+=deg
    # print(degree_pattern)


    matcher = Matcher(nlp.vocab)
    matcher.add("PROPER_NOUNS", [degree_pattern], greedy='LONGEST')
    doc = nlp(text)

    # for token in doc:
    #     print(token, token.pos_)
    matches = matcher(doc)
    # print (len(matches), "matches got")
    degrees={}
    edu_level = ""
    for match in matches[:10]:
        # print (match, doc[match[1]:match[2]])
        
        # print(match)    

        for t in doc[match[1]:match[2]]:
            # print(t, "archit", degree_pattern[0]["LOWER"]["IN"])
            # print(t)
            if str(t).lower() in levels:
                edu_level = str(t).lower()
            elif str(t).lower() in deg:
                if str(t)[0].lower() == "b":
                    edu_level = "bachelors"
                elif str(t)[0].lower() == "m":
                    edu_level ="masters"                   
            
            
        m = str(doc[match[1]:match[2]]).split()
        branch = ""
        for i in range(len(m)):
            if m[i].lower()=="in":
                branch = " ".join(m[i+1:])
                break
        degrees[edu_level] = [str(doc[match[1]:match[2]]), branch]
        # degrees.append([doc[match[1]:match[2]], edu_level])
   
    return degrees



    
    
def extract_scores(text):
    CGPA_pattern = r'((CGPA)?:?\s*\(?(\b\d\.\d\d?)(/\d\d)?\)?)'
    per_pattern = r'\b\d\d\.?\d?\s?%'

    lines = text.split('\n') 
    ans=[]      
    for line in lines:
        # print(line)
        match1 = list(re.findall(CGPA_pattern, line))
        match2 = list(re.findall(per_pattern, line))


        if match1!=[]:
            # print(match)
            ans.append(match1[0][2])
        if match2!=[]:
            # print(match2)
            ans.append(match2[0])

    return ans


def extract_date_ranges(text):
# Define the regular expression pattern
    pattern = r"\b(([a-zA-Z]+(\s?\d\d?)?)?,?\s?\d{4})\s?-?–?–?‑?(to)?\s?((([a-zA-Z]+(\s?\d\d?)?)?,?\s\d{4})|Present|Till Date|Current)"
    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Extracted date ranges
    extracted_ranges = []
    for match in matches:
        extracted_ranges.append([match[0],match[4]])

    return extracted_ranges



def edu_map_dates(text, orgs, dates):
    mapped_dates = {}
    text = text.lower()
    log = {}
    for org in orgs:
        org_start = text.find(org.lower())  
        min_distance = float('inf')
        closest_date = "None"
        if dates:
            for date in dates:  
                # print(date, dates)
                if date[0] in log:
                    continue              
                dist = abs(org_start - min(text.find(date[0].lower()),text.find(date[1].lower())))
                if dist < min_distance:
                    min_distance = dist
                    closest_date = date
                    # print("closent",closest_date)

            if closest_date!="None":   
                log[closest_date[0]]=0
            mapped_dates[org] = closest_date
    return mapped_dates

def edu_map_scores(text, orgs, scores):
    mapped_scores = {}
    text = text.lower()
    log = {}
    for org in orgs:
        org_start = text.find(org.lower())  
        min_distance = float('inf')
        closest_score = "None"
        if scores:
            for score in scores:  
                if score[0] in log:
                    continue              
                dist = abs(org_start - text.find(score[0]))
                if dist < min_distance:
                    min_distance = dist
                    closest_score = score
            if closest_score!="None": 
                log[closest_score]=0
            mapped_scores[org] = closest_score
        
    return mapped_scores



def education_info(text):

    orgs = extract_edu(text)
    scores = extract_scores(text)
    dates = extract_date_ranges(text)

    # print(orgs)
    # print(scores)
    # print(dates)
    # print("scores=", scores)
    # closest_orgs = {}

    mapped_score = edu_map_scores(text, orgs, scores)
    mapped_dates = edu_map_dates(text, orgs, dates)


    for org in orgs:
        orgs[org].append(mapped_score[org] if org in mapped_score else "")
        orgs[org].append(mapped_dates[org] if org in mapped_dates else [])
        
                
    return orgs



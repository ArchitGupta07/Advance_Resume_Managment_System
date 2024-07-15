from parser.job_roles_extractor import extract_prev_job_roles
from parser.skills_Extractor import extract_skills
from parser.edu_extract import education_info, extract_degree
from parser.new_location import all_locs
# query = "get me resume which have experience in java and Python or live in Noida"

# def bool_finder(query):
#     query = query.lower()
#     boolean_operators = ["or", "not", "and", "&&", "||", "!"]
#     query_tokens = query.split()

#     query_split = {}

#     for i in range(len(query_tokens)):
#         if query_tokens[i] in boolean_operators:
#             if query_tokens[i] in query_split:
#                 query_split[query_tokens[i]].append(" ".join(query_tokens[:i]))
#             else:
#                 query_split[query_tokens[i]] = [" ".join(query_tokens[:i])]
#     return query_split

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def remove_prepositions(query):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(query)
    filtered_query = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_query)

import re
def extract_scores(text):
        CGPA_pattern = r'((CGPA)?:?\s*\(?(\b\d\.?\d?\d?)(\/\d\d)?\)?)'
        # per_pattern = r'\b\d\d\.?\d?\s?%'

        lines = text.split('\n') 
        ans=[]      
        for line in lines:
            # print(line)
            match1 = list(re.findall(CGPA_pattern, line))
            # match2 = list(re.findall(per_pattern, line))


            if match1!=[]:
                # print(match)
                ans.append(match1[0][2])
           

        return ans

from geotext import GeoText
def extract_locations(text):


    text = remove_prepositions(text)
    # capitalized_text =[word.capitalize() for word in text.split()]
    # print(capitalized_text)
    print(text)

    cities = []
    countries = []

    for i in text.split():

        if i in ["of","Of","march","March", "along"]:
            continue

        places = GeoText(i.capitalize())
        if places.cities:
            cities.append(i.lower())
        elif places.countries:
            countries.append(i)
    print(list(set(cities)))
    return list(set(cities))

from parser.main_func import exp_duration

def data_extractor(query):
        
        category = check_category(query)

        
        get_roles = extract_prev_job_roles(query)
        skills = extract_skills(query)   

        category_string = ""

        if category:
            for k,v in category.items():
                category_string += v.strip().lower().title()


            refined_skills = []

            for skill in skills:
                if skill not in category_string.split():
                    refined_skills.append(skill)
            skills = refined_skills
                  

        # score = extract_scores(query)
        score = []
        # level = ""
        degree = extract_degree(query)
        deg = []
        for k in degree:
            deg.append(k)
        # locations = extract_locations(query)
        locations = all_locs(query)

        exp_years = exp_duration(query) if exp_duration else []
        if category:
             get_roles = []
        else:
             category = {}

        return get_roles, skills, score, deg, locations, exp_years, category



def filter_extractor(query):
        get_roles, skills, score, deg, locations, exp_years,category = data_extractor(query)



        if not get_roles and not skills and not locations and not exp_years and not category:
             filter_flag = False
        else:
             filter_flag = True

       
        resume_filters = {
        "Candidate": {
            "check": [],
           
        },
        "Education": {
            "check": [],
            
        },
        "WorkExperience":{
            "check": [],

        },
        "Contact": {
            "check": [],
          
        },
        "Address":{
             "check":[]
        },
        "Skill": {
            "check": [],
           
        },

    };

        # amount = 0
        resume_filters["Skill"]["check"] = []
        resume_filters["Education"]["check"] = []
        resume_filters["WorkExperience"]["check"] = []
        resume_filters["Candidate"]["check"] = []
        resume_filters["Address"]["check"] = []

        if skills:
            
            resume_filters["Skill"]["check"].append("SkillName")
            resume_filters["Skill"]["SkillName"] = skills
        
        if score:
            
            resume_filters["Education"]["check"].append("Score")
            resume_filters["Education"]["Score"] = score
        
        if deg:
            
            resume_filters["Education"]["check"].append("Degree")
            resume_filters["Education"]["Degree"] = deg

        if get_roles:

            resume_filters["WorkExperience"]["check"].append("Role")
            resume_filters["WorkExperience"]["Role"] = get_roles
           
        if locations:
            resume_filters["Address"]["check"].append("City")
            resume_filters["Address"]["City"] = locations
        if exp_years:
            resume_filters["Candidate"]["check"].append("Experience")
            resume_filters["Candidate"]["Experience"] = exp_years

        if category:
                r_c = [v.lower() for k,v in category.items()]
                resume_filters["Candidate"]["check"].append("RoleCategory")
                resume_filters["Candidate"]["RoleCategory"] = r_c
  
        return resume_filters , filter_flag



import json
from fuzzywuzzy import fuzz

def check_category(query):
        categories = {}
        with open('data/SkillsData/Category.json', 'r') as file:
            skill_category = json.load(file) 

        for key, values in skill_category.items():
            for v in values:
                # similarity_ratio = fuzz.token_set_ratio(v, query)
                similarity_ratio = fuzz.partial_ratio(v, query)
                if similarity_ratio>=80:
                    # print(similarity_ratio)
                    categories[key]  = v   
        # print(categories)
        return categories

def bool_finder(query):
# Split the query into individual terms
    terms = query.split()

    # Initialize variables to store the separated query parts
    query_list = []
    boolean_operators = []
    current_part = []

    # Iterate through the terms to separate based on boolean operators
    for term in terms:
        if term.lower() in ['and', 'or']:
            # Store the current part and boolean operator
            query_list.append(" ".join(current_part))
            boolean_operators.append('and' if term.lower()=='in' else term.lower())
            current_part = []
        else:
            # Add the term to the current part
            current_part.append(term)

    # Add the last part of the query
    query_list.append(" ".join(current_part))

    # Display the separated query parts
    print("query_list:", query_list)
    print("Boolean Operators:", boolean_operators)
    return query_list, boolean_operators

# print(bool_finder(query))


def filter_finder(query, showFlag):

    filter_flag = False
    query_list , boolean_operators = bool_finder(query)

    filters_list = []
    for query in query_list:
         
        fils, filter_flag = filter_extractor(query)

        if filter_flag or showFlag:
            filters_list.append(fils)
        else:
            filters_list.append(filter_flag)
    

    
    print(filters_list)

    return filters_list, boolean_operators
        


      
# query = "get me resume which have experience in java and Python or live along in Noida"

# print(filter_finder(query))

print(bool_finder("get me resumes of python and java in mumbai"))
     
     
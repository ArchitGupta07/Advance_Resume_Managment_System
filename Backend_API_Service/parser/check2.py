# import re

# def join_split_words(text):
#     # Use regular expressions to find and replace single spaces within sequences of capital letters
#     pattern = re.compile(r'(?<=\b[A-Z]) (?=[A-Z]\b)')
    
#     # Replace single spaces with no space
#     return pattern.sub('', text)

# # Example input
# text = """
# Y A S H   S H A R M A

# S O F T W A R E   E N G I N E E R

# C O N T A C T

# P R O F I L E

# +91 9818580167

# syash520@gmail.com

# https://syash5.github.io/bio/

# Delhi, India

# E D U C A T I O N

# Guru Gobind Singh Indraprastha University
# (2016-2020)

# Bachelor of Technology in Computer Science

# CGPA: 8.25
# """

# # Process the text
# cleaned_text = join_split_words(text)

# print(cleaned_text.replace("   "," "))
from fuzzywuzzy import fuzz
import json

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
    print(categories)
    return categories
    # return None


check_category("get me project manager and frontend developers with 2+ years of experience")
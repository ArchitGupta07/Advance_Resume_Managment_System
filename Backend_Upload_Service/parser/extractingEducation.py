from edu_extract import extract_degree
from text_extractor import divide_resume_sections
import traceback

from tika import parser
def tika_text_extraction(file_path):   
    parsed_file = parser.from_file(file_path)
    text = parsed_file["content"]
    return text



import re

def extract_degrees(text):
    # Define a regex pattern to capture the degrees and the subsequent text until a delimiter
    pattern = r"\b(Bachelor of Technology|B\.Tech|Master of|Bachelor of|diploma|PGDRM|B\.Com|B\.Com\(H\)|B\.Tech in Computer Science|Btech in Computer Science|PG-DAC|B\.E|BE|B\. Tech\. in Computer Science and Engineering|B\.Tech, Artificial Intelligence And Machine Learning|MBA|Bachelor of Technology in Computer Science and Engineering|Bachelor of Information Technology|MBA/PGDBM, Information Technology and Marketing \(Dual Specialization\)|Bachelor of Technology in Information Technology|B-Tech|B\.E|B\.E\.)[^\n|]*"

    # Define delimiters: 2 or more spaces or |
    delimiters = r"\s{2,}|\|"

    # Split the text into lines to ensure we capture entire lines
    lines = text.splitlines()

    # List to store the extracted degrees
    extracted_degrees = []

    for line in lines:
        # Find all matches in the line
        matches = re.findall(pattern, line, re.IGNORECASE)
        if matches:
            # Append the entire line as it contains the degree
            extracted_degrees.append(line.strip())

    return extracted_degrees

import os
def process_file(filePath):
    
    try:
        # print('here')
        text = tika_text_extraction(filePath)
        # data = divide_resume_sections(text)
        data = extract_degrees(text)
        # print('\n\n\n\n',data,'\n\n\n\n')

    
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
folder_path = 'C:/Users/yaggarwal/Documents/AdvancedResume/Deployments/UploadService/data/resumes'
process_all_files_in_folder(folder_path)




# Test the function with an example input
text = """
Bachelor of Technology in Computer Science  Other text not part of the degree
B.Tech | Some unrelated text
Master of Science  More unrelated text
Bachelor of Arts
diploma in Engineering
PGDRM  Random text
B.Com(H) More text
B.Tech in Computer Science  More text
Btech in Computer Science | Additional text
PG-DAC
B.E in Mechanical Engineering  Another degree
BE | Random unrelated text
B. Tech. in Computer Science and Engineering  Unrelated text
B.Tech, Artificial Intelligence And Machine Learning  More text
MBA in Finance and Marketing  Another unrelated text
Bachelor of Technology in Computer Science and Engineering  Unrelated
Bachelor of Information Technology | More text
MBA/PGDBM, Information Technology and Marketing (Dual Specialization)  Unrelated
Bachelor of Technology in Information Technology  More text
B-Tech | Random text
B.E in Civil Engineering
B.E. in Electrical Engineering  Unrelated text
"""

# degrees = extract_degrees(text)
# print(degrees)



# Bachelor of Technology
# B.Tech
# Master of 
# Bachelor of 
# diploma
# PGDRM
# B.Com
# B.Com(H)
# B.Tech in Computer Science
# Btech in Computer Science
# PG-DAC
# B.E
# BE
# B. Tech. in Computer Science and Engineering
# B.Tech, Artificial Intelligence And Machine Learning
# MBA
# Bachelor of Technology in Computer Science and Engineering
# Bachelor of Information Technology
# MBA/PGDBM, Information Technology and Marketing (Dual Specialization)
# Bachelor of Technology in Information Technology
# B-Tech
# B.E
# B.E.
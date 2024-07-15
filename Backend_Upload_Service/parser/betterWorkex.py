# from parser.check3 import remove_characters
from text_extractor import tika_text_extraction, divide_resume_sections

# from main_func2 import summary_parser

from check3 import category_finder


from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def extract_font_info(pdf_path):
    font_info = []
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            font_info.append({
                                'text': character.get_text(),
                                'fontname': character.fontname,
                                'size': character.size
                            })
    return font_info

# pdf_path = 'your_pdf_file.pdf'  # Replace with your PDF file path
fil = 'D:/Ex2_Projects/Resumes/Amol_Resume.pdf'
# font_data = extract_font_info(fil)

# for data in font_data:
#     print(f"Text: {data['text']}, Font: {data['fontname']}, Size: {data['size']}")


def remove_characters(text):



    characters_to_remove = ",\"'{}()\\|>^!:;•"
    # Create a translation table
    # translation_table = str.maketrans("", "", characters_to_remove)
    translation_table = str.maketrans(characters_to_remove, ' ' * len(characters_to_remove))
    # Remove the characters
    cleaned_text = text.translate(translation_table)
    return cleaned_text

import traceback
import re
def summary_exp_duration(text):
    try:
        text = text[:2000]        
        exp_pattern = r"((\d.?\d?)\s?(\+|plus)?\s?(years|year|yrs))"
        exp = 0
        matches = re.findall(exp_pattern, text)
        
        if matches:
            # print(matches)
            exp = float(matches[0][1].replace("+",""))

        if exp:
            return exp
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return None
    

   

# def process_file(file):
#     text = tika_text_extraction(file)
#     # print(text)

#     text = remove_characters(text).replace("."," ")

#     workex = extract_work_ex(divide_resume_sections(text)["Experience"].replace("-","").lower())

#     print(f"file name is {file}")
#     print("\n\n")

#     print(f"work ex is {workex}")
#     print("\n\n")
                    

#                     # if not name:
#     dates1,dates2,dates3, sin_dates1 = extract_date2(text)
#     print(dates1)
#     print("\n")
#     print(dates2)
#     print("\n")
#     print(dates3)
#     print("\n")
#     print(sin_dates1)

#     print(divide_resume_sections(text)["Experience"].lower().replace("-",""))
#     print("\n\n\n")

#     work_ex_date_mapping(divide_resume_sections(text)["Experience"].lower().replace("-",""), [k for k in workex], dates1+dates2+dates3)

import os

# def process2(file):
#     text = tika_text_extraction(file)

# # process_file(fil)

#     skill_date_map(text)



from main_func2 import extract_prev_job_roles



def get_workex(filepath):
    text = tika_text_extraction(filepath)

    work_text = divide_resume_sections(text)["Experience"]

    if not work_text.strip() or len(work_text.strip().split())<10 :
        work_text = text
    

    
    work_text = work_text.replace("-","").lower().title()

    work_text = remove_characters(work_text)

    # print(filepath)
    roles = extract_prev_job_roles(work_text)
    # print(roles)   


    # extract_prev_job_roles()

   
    category = {}
    for role in roles:
        cat = category_finder(role)
        category[role] = cat

    # print(category)
    print("\n\n\n\n")

    return category


from edu_extract import extract_edu, extract_degree

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
                    # text = divide_resume_sections(tika_text_extraction(file_path))["Summary"]
                    text = tika_text_extraction(file_path)
                    category = extract_edu(text)
                    category1 = extract_degree(text)
                    print(file_path)
                    print(category)
                    print(category1)
                    print("\n\n\n")

                    if category:
                        detected+=1
                    else:
                        not_detected+=1
                    
            except:
                print(f"failed to process {file_path}")

        print(f"Detected: {detected} and Not Detected : {not_detected}")
        return detected,not_detected
    
    except:

        print(f"error occured in {file_path}")
        
        return detected,not_detected

        
# check

# Example usage
# folder_path = 'P:/Bhagyashri/Resume'
folder_path = 'D:/Ex2_Projects/Resumes'
fil = 'D:/Ex2_Projects/Resumes/Android_Resume.pdf'
# folder_path = 'data/resumes'
# print(fil)
text = tika_text_extraction(fil)

# process_file(fil)
# extract_font_info(fil)

# url = "https://minio-endpoint.skilldify.ai/armss-dev/%5B313%5D-86bef92ffe6fc059fe4bf23221761070f2932795ed62bcf2494fd771c690d74d%21%40%26Amit_CV%20%282%29.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240607%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240607T020707Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=2ee1c9e6e32f15805e70cb4ef6926ba6ba5c037be6766fa80b31dc56726d510d"



# get_workex(fil)
# get_workex(url)
# skill_date_map(text)
# print(extract_edu(text))

# process_all_files_in_folder(folder_path)
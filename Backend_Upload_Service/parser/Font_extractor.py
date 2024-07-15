
import fitz
import re


from fuzzywuzzy import fuzz
import traceback

import requests

def download_pdf(url, path):
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)



def check_similarity(words, email):
    max_similarity = 0
    max_similarity_word = ""
    
    for word in words:
        
        if word and word.lower()!=email.lower():  # Ensure the word is not an empty string
            similarity = fuzz.ratio(word.lower(), email.lower().split("@")[0])
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_word = word
    # print(f"Most similar word: {max_similarity_word}, Similarity: {max_similarity}")
    return max_similarity_word.lower().title(), max_similarity

def extract_email(text):
    patterns = [r"[a-z0-9A-Z!#$%&*()-_+,./~]+@[^\s]+"]

    for pattern in patterns:
        email_regex = re.compile(pattern)
        emails = set(email_regex.findall(text))
        # for email in emails:
        # print(email)
    return list(emails)


from docx import Document

def extract_text_with_fonts_docx(docx_path):
    doc = Document(docx_path)
    text_with_fonts = []

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            text = run.text
            font = run.font.name
            size = run.font.size.pt if run.font.size else 0
            if text.replace(" ", "") != "":
                text_with_fonts.append((text, font, size))
    # print(text_with_fonts)
    return text_with_fonts

def extract_text_with_fonts(pdf_path):
    
    text_with_fonts = []

    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:  
                            text = span["text"]
                            font = span["font"]
                            size = span["size"]
                            if text.replace(" ","") != "":
                                text_with_fonts.append((text, font, size))
    except Exception as e:
        print(f"An error occurred pdf font extractor: {e}")
        traceback.print_exc()

    return text_with_fonts

def determine_case(text):
    if text.isupper():
        return "uppercase"
    elif text.islower():
        return "lowercase"
    else:
        return "mixed case"

def is_valid_text(text):
    keywords_to_ignore = {"resume", "summary","dsa","education", "certifications","certificates", "interests","languages","organizations", "skills", "contact", "email", "experience", "date","declaration","personal","details","place","cgpa","projects","strengths","objective","contacts","interest","about","hindi","english","software","dsa","technology","science"}
    words = text.strip().replace(",", "").lower().split()
    return all(len(" ".join(words)) >= 3 and word.lower() not in keywords_to_ignore for word in words)

def clean_text(text):
    characters_to_remove = ",\"'{}()\\|>^!:;•"
    translation_table = str.maketrans("", "", characters_to_remove)
    return text.translate(translation_table)

# Usage example

filepath = "D:/Ex2_Projects/Resumes/ankush.pdf"
# filepath = "D:/Ex2_Projects/Resumes/Anubhav-PA.pdf"


import math


def get_name(filepath, skills):

    font_data = extract_text_with_fonts(filepath)
    # font_data = extract_text_with_fonts_docx(filepath)

    max_size = 0
    words = []
    emails = []

    # First pass to determine the max font size

    # print(font_data)
    for text, font, size in font_data:

        if is_valid_text(text) and len(text)>=3:

            
            # print(f"Text: {text.strip()}, Font: {font}, Size: {size}")
            max_size = max(max_size, size)

    # Second pass to collect words based on the criteria

    max_size = math.floor(max_size)
    for text, font, size in font_data:

        
        cleaned_text = clean_text(text).strip()
        # print(cleaned_text)
        emails += extract_email(cleaned_text)

        if len(cleaned_text.split("/"))>1:
            continue
        if is_valid_text(cleaned_text) and len(cleaned_text)>=3 and  "@" not in text and cleaned_text.lower() not in skills:
        
            if size >= max_size:
                words.append(cleaned_text)
            text_case = determine_case(cleaned_text)
            if text_case == "uppercase":
                words.append(cleaned_text)

    # Remove duplicates
    words = list(set(words))
    

    # print("\n\n\n")
    # # print("Max font size:", max_size)
    # print("Max font size:", math.floor(max_size))
    # print("Words:", words)
    # print("Emails:", emails)
    # print("filepath: ",filepath)
    name = None
    if emails:

        name, sim_score = check_similarity(words, emails[0].lower())


        if sim_score<=33:
            return None
    
    # elif words:
    #     name = words[0]
    else:
        return None

    # print(name)

    if name and len(name.split())<2:
        for i in range(len(font_data)):

            # print(font_data[i][0].strip().lower(),name.lower())
            if font_data[i][0].strip().lower() == name.lower():
                # print("gotcha")

                if i>0:
                    if font_data[i-1][2] == font_data[i][2]:
                        name = font_data[i-1][0]+ " " + name
                        break
                if i<len(font_data):
                    if font_data[i+1][2] == font_data[i][2]:
                        name = name + " " + font_data[i+1][0]
                        break

        name = name.lower().capitalize()
        # print(name.lower().capitalize())
        print("\n\n\n")
    #     return name
    # else: 

    if len(name.strip().split())>4 or bool(re.search(r'\d', name)):
        return None
    
        
    return name



import os

    
def process_all_files_in_folder(folder_path):

    try:
        count=0
        detected =0
        not_detected = 0 
        for filename in os.listdir(folder_path):

            try:
                if count>100:
                    break


                

                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):  # Ensure it's a file
                    count+=1
                    check = get_name(file_path)
                    print(count)

                    if check:
                        # print(check)
                        detected+=1
                    else:
                        not_detected+=1
            except:
                print("error")


        print(f"Detected: {detected} and Not Detected : {not_detected}")
        return detected,not_detected
    
    except:
        print("error")
        
        return detected,not_detected

        

# Example usage
# folder_path = 'D:/Ex2_Projects/Resumes'
folder_path = 'data/resumes'

pdf_url = "https://minio-endpoint.skilldify.ai/armss-dev/%5B80%5D-b432ae9362cafc2e08ba89ec01cd65038081ae6e9b8cd795ccdded5868903726vineetaSharma%5B0_0%5D.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240529%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240529T045722Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=96b165f52e976557fa5f50f6c2daeb566096d43b36acdc4dcb4dfe9638dce13f"
local_pdf_path = "downloaded.pdf"
# process_all_files_in_folder(folder_path)

# get_name("D:/Ex2_Projects/Resumes/anand_prakash_jaiswal.pdf")
# print(get_name("P:/Bhagyashri/Resume/201B257-SHRAMIT-GUPTA-Resume.docx.pdf",[]))
# get_name("data/resumes/resume2.pdf",[])
# download_pdf(pdf_url,local_pdf_path)
# name = get_name(local_pdf_path)
    
# if name = 


# print(extract_email("omikoundal45@gmail.com"))
# print(get_name(filepath))
# Usage example
# font_data = extract_text_with_fonts('D:/Ex2_Projects/Resumes/Anand_Flutter_and_React_Native.pdf')
# print(font_data)

# for text, fontname, fontsize in font_data:
#     print(f"Text: {text.strip()}, Font: {fontname}, Size: {fontsize}")


# name at last : AmitK_SM_PO.docx, Anamika_Test_Engineer_check.pdf

#resolved: Anagha_V_Resume_.pdf,ANUBHAV_ADHYAYAN.pdf, ANILA_V_NAIR_CV1.pdf, Ankit_cv_07_2023.pdf, ANTONY_K_JOSE_SE_IN.pdf,  Anser_resume.pdf ,  Annu_Resume-28th june 2023.pdf, Anmol_Resume.docx, Ankur_Garg_Agile.pdf

# image: AnujSharma_UI_Designer.pdf, Aniket_Meghani_Resume_2023_check.pdf, \resume28.pdf
#check: anand_prakash_jaiswal.pdf - spacing between name letters
# urls issue : Ankita_Singh_Fresher_Resume.pdf
#small name :  D:/Ex2_Projects/Resumes\ankit.docx, 
# skills removal issue: Ankit_verma.pdf,
#similarity score: Anany_Verma_Resume.docx, 


#try earlier approach ankit.docx, 

# checlll
# from parser.main_func import extract_prev_job_roles
from collections import OrderedDict
import re

import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)


def tocheckbesideDates(lst):
  print(lst)
  nlst=[]
  for i in range(len(lst)-1):
    if lst[i+1][0] - lst[i][-1]<10:
      nlst.append([lst[i],lst[i+1]])
  if len(nlst)>0:
    return nlst[0]
  else:
    return [None,None]
def totalExperience(d1,d2,total=0):
  date1 = datetime.strptime(d1, '%Y-%m-%d')
  date2 = datetime.strptime(d2, '%Y-%m-%d')
  # Calculate the difference
  difference = (date1 - date2).days
  difference_years = difference / 365.25
  total = total+difference_years
  return total
def tocheckNearRole(dateslst,roleslst,text):
  # text = text.lower()
  # text = re.sub(r"[^A-Za-z0-9]"," ",text)
  #   # text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
  # text = re.sub(r'\s+', ' ', text)
  nearest_word = None
  min_distance = float('inf')  # Initialize with infinity
  for word in roleslst:
      distance = abs(word[-1] - dateslst[0][0])
      # print(word,text.find(word) ,dateslst[0][0])
      if distance < min_distance:
          min_distance = distance
          nearest_word = word
  return nearest_word[0], min_distance
def toExtract_Experience_Rolewise(text):
  i=[]
  j=[]
  # or doc.ents[entity].label_ == "ORG"
  # text = text.lower()
  # text = re.sub(r"[^A-Za-z0-9\/-]"," ",text)
  #   # text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
  # text = re.sub(r'\s+', ' ', text)
  value,dates = ExtractDates(text)
  roles = togetRoles(text)
  # print(roles)
  # print(dates)
  # toExtract_location(text)
  total=0
  dictexperience={}
  status=True
  if len(value)>1:
    print(value)
    for i in range(len(value)-1):
      for m in range(i+1,len(value)):
        dat1 = value[i]
        dat2 = value[m]
        lst=[]
        for k,j in dates.items():
          if j==dat1 or j==dat2:
            lst.append(k)
        print(lst)
        string1 , string2 = tocheckbesideDates(lst)
        # print(string1,string2)
        if (string1!=None and string2!=None ):
          if len(roles)>0:
            role,distance = tocheckNearRole([string1,string2],roles,text)
          else:
            role = "Not Found"
          print(dat1, "--", dat2)
          dictexperience[dat1+" -- "+dat2]=[role,round(totalExperience(dat1,dat2),2),status]
          status=False
          total = totalExperience(dat1,dat2,total)
          # print(role)
      dictexperience["total"]= round(total,2)
    return dictexperience
  else:
    dictexperience["total"]=   total
    return dictexperience
    # print(text)
from dateutil.parser import parse
from datetime import datetime
def ExtractDates(text):
  # NOt USing date_pattern = r"(?:\d{1,2}[ -]?)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b[ -]\d{1,2}[ -]?\d{2,4}"
  # Using But date_pattern = r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))\s+(\d{2,4})\b\s*(.*?)\s*(?:\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))\s+(\d{2,4})\b|(\bPresent|Till|Current\b))\b"
  date_pattern =  r"\b(?:\d{1,2})[/\s,-]+(?:\d{1,2})[/\s,-]+\d{4}\b|\b(?:\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)\b|\d{2})(?:\b[\s\,'/-]+?)(\d{2,4})\b|(\bPresent|Till|Current(?:ly)?|Now|Ongoing|Working Current(?:ly)\b)|(?:\b20\d{2}\b))\b"
  # date_pattern =  r"\b(?:\d{1,2})[/\s,-]+(?:\d{1,2})[/\s,-]+\d{4}\b|\b(?:\d{2})[/\s,-]+(?:\d{2,4})|(?:\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)\b)(?:\b[\s\,/-]+?)(\d{2,4})\b|(\bPresent|Till|Current(?:ly)?|Now|Ongoing\b))\b"
  dates_iter =   re.finditer(date_pattern, text , re.IGNORECASE)
  potential_dates = {datevalue.span():"".join(datevalue.group()) for datevalue in dates_iter}
  # potential_dates = [" ".join(datevalue) for datevalue in re.findall(date_pattern, text , re.IGNORECASE)]
  # print(potential_dates)
  # print(text)
  parsed_dates = []
  for key, date_str in potential_dates.items():
      try:
        if date_str.lower().strip() in ["present","till","current","currently"]:
          date_str = datetime.now().isoformat()
        elif len(date_str.strip().split(" ")[-1])==2:
             date_str = date_str.strip().split(" ")
             date_str[-1] = "20"+date_str[-1]
             date_str = " ".join(date_str)
        parsed_date = parse(date_str, fuzzy=True)
        potential_dates[key]=parsed_date.strftime("%Y-%m-%d")
        parsed_dates.append(parsed_date.strftime("%Y-%m-%d"))
      except ValueError:
          # Skip if parsing fails
          pass
  # Print the parsed dates
  return sorted(list(set(parsed_dates)),reverse= True),potential_dates
  # for date in parsed_dates:
  #     print(date.strftime("%Y-%m-%d %H:%M:%S"))




import numpy as np
from flashtext import KeywordProcessor
loaded_array = np.load('data/titles.npy')
keyword_processor = KeywordProcessor()
keyword_processor.add_keyword('Mobile App', 'Mobile Application')
keyword_processor.add_keywords_from_dict({
"Front End Developer": ["Frontend Developer"],
 "Back End Developer": ["Backend Developer"],
 "Software Engineer" : ["Software Engineering"]
})
keyword_processor.add_keywords_from_list(list(loaded_array))
def togetRoles(text):
  text = keyword_processor.replace_keywords(text)
  pattern = r"[^A-Za-z0-9\/\.]"
  text = re.sub(pattern," ",text, flags=re.MULTILINE)
  text = re.sub(r"\s+"," ",text)
  keywords_found = keyword_processor.extract_keywords(text,span_info=True)
  return keywords_found

#     try:
        
#         count=0
#         detected =0
#         not_detected = 0 
#         for filename in os.listdir(folder_path):
#             if count>30:
#                 break

#             try:
#                 file_path = os.path.join(folder_path, filename)
#                 if os.path.isfile(file_path):  # Ensure it's a file
#                     count+=1

#                     # process_file(file_path)
#                     # get_workex(file_path)
#                     print(file_path)
#                     text = tika_text_extraction(file_path)
#                     print(toExtract_Experience_Rolewise(text))
#                     print("\n\n\n\n")

                    
                    
#             except:
#                 print(f"failed to process {file_path}")

#         print(f"Detected: {detected} and Not Detected : {not_detected}")
#         return detected,not_detected
    
#     except:

#         print(f"error occured in {file_path}")
        
#         return detected,not_detected



# # url = 

# folder_path = 'D:/Ex2_Projects/Resumes'
fil = 'D:/Ex2_Projects/Resumes/Amit_Maurya_Resume.pdf'
# folder_path = 'data/resumes'
folder_path = 'P:/Bhagyashri/Resume'
# print(fil)
# text = tika_text_extraction(fil)

# process_file(fil)
# extract_font_info(fil)

# get_workex(fil)
# skill_date_map(text)

# text = tika_text_extraction(fil)

# print(
# extract_font_info(fil)

# get_workex(fil)
# skill_date_map(text)
# process_all_files_in_folder(folder_path)
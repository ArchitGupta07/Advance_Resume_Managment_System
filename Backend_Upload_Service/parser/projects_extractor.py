
import re


import spacy

from spacy.matcher import Matcher

from geotext import GeoText
# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

from fuzzywuzzy import fuzz


# def search_(query):
#     try:
#         # Search for a query
#         results = wikipedia.search(query)

#         # Print the search results
#         # print("Search results for", query)
#         # for result in results:
#         #     print("-", result)

#         # Get the summary of the first search result
#         if results:
#             first_result_summary = wikipedia.summary(results[0], auto_suggest=False)[:40]
#             if "city" in first_result_summary:
#                 return True

#             # print("\nSummary of the first search result:")
#             # print(first_result_summary)
#     except wiki_exceptions.DisambiguationError as e:
#         print("DisambiguationError: There are multiple possible Wikipedia pages for this query. Please be more specific.")
#         # print("Possible options:")
#         # for option in e.options:
#         #     print("-", option)
#         return False
#     except wiki_exceptions.PageError:
#         print("PageError: The Wikipedia page for the given query does not exist.")
#     except Exception as e:
        # traceback.print_exc()

#         print("An error occurred:", e)
#     return False





def is_similar(string1, string2, threshold=60):
    similarity = fuzz.ratio(string1, string2)
    return similarity >= threshold

def projects_extraction(text):
    matcher = Matcher(nlp.vocab)

    project_prefix = ["application","app","system","project"]
  
    pattern =  [
    {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
    {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
    {"POS": "NOUN", "OP": "?"},
    {"ORTH": "-", "OP": "?"},
    {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
    {"LOWER": {"IN": ["clone", "website", "application", "app"]}, "OP": "?"}
]
    matcher.add("PROPER_NOUNS", [pattern], greedy='LONGEST')
   
    doc = nlp(text)
    matches = matcher(doc)
    
    projects = [(match_id, doc[match[1]:match[2]]) for match_id, match in enumerate(matches)]
    
    projects.sort(key=lambda x: x[1].start)
    
    
    project_names = [project[1].text for project in projects if len(project[1].text.split()) >=2]
    
  
    # check_projects = []
    # for sents in (doc.sents):
    #     for j , sen in enumerate(sents.text.split("\n")):
    #         # print(" ".join(sen.split()) ,j)
            
    #         if any(is_similar(" ".join(sen.split()), project_name) for project_name in project_names):
                
    #             check_projects.append(" ".join(sen.split()) )
        
    
    # # return project_names, check_projects
    # return check_projects


    for proj in project_names: 
        doc2 = nlp(proj)
        # for token in doc2:
        #     print(token, token.dep_, token.pos_)
        for ent in doc2.ents:
            # print(ent.text, ent.label_)
            if ent.label_=="PERSON" and proj in project_names:
                project_names.remove(proj)
                continue

        # if search_wikipedia(proj):
        #     project_names.remove(proj)
        #     continue
        # print(proj.lower().split())
        places = GeoText(proj)
        if places.cities:
            if proj in project_names:
                project_names.remove(proj)
            # continue
            # print("A")
              
        elif re.match(r'\d?\d\/20\d\d\s*-\s*\d?\d\/20\d\d', proj) and proj in project_names:
            project_names.remove(proj)
            # continue
            # print("B")
        elif len(proj.split("/"))>1 and proj in project_names:
            project_names.remove(proj)
        elif "certiﬁcate" in list(proj.lower().split()) or "certificate" in proj.lower().split() and proj in project_names:
            # print("certi")
            project_names.remove(proj)

            
    check_projects = []
    for sents in (doc.sents):
        for j , sen in enumerate(sents.text.split("\n")):
            # print(" ".join(sen.split()) ,j)
            
            if any(is_similar(" ".join(sen.split()), project_name) for project_name in project_names):
                if len(sen.split())<=4:
                    check_projects.append(" ".join(sen.split()) )
                else:
                    p = len(sen.split())-5
                    check_projects.append(" ".join(sen.split()[p:]) )
        
    if len(check_projects)<1:
        return list(set(project_names))
    else:
        return  list(set(check_projects))


# from text_extractor import extract_text_from_pdf, divide_resume_sections,tika_text_extraction

# text = ""
# for page in extract_text_from_pdf("data/resumes/resume17.pdf"):
# # for page in extract_text_from_pdf(filePath+file):
#     text += " " + page

# # # print(divide_resume_sections(text)["Projects"])

# # # print(list(text))

# # # print(list(projects_extraction(text)))
# print(list(projects_extraction(divide_resume_sections(text)["Projects"])))

# # resume17, resume2, resume, 




# import os

    
# def process_all_files_in_folder(folder_path):

#     try:
#         count=0
#         detected =0
#         not_detected = 0 
#         for filename in os.listdir(folder_path):

#             try:
#                 if count>100:
#                     break


                

#                 file_path = os.path.join(folder_path, filename)
#                 if os.path.isfile(file_path):  # Ensure it's a file
#                     count+=1
#                     print(file_path)
#                     text = tika_text_extraction(file_path)
#                     check = list(projects_extraction(divide_resume_sections(text)["Projects"]))
#                     print(check)

#                     print("\n\n\n")

#                     if check:
#                         # print(check)
#                         detected+=1
#                     else:
#                         not_detected+=1
#             except:
#                 print("error")


#         print(f"Detected: {detected} and Not Detected : {not_detected}")
#         return detected,not_detected
    
#     except:
#         print("error")
        
#         return detected,not_detected

        

# # Example usage
# # folder_path = 'D:/Ex2_Projects/Resumes'
# folder_path = 'data/resumes'


# process_all_files_in_folder(folder_path)
# # search_wikipedia("india")
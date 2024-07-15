import spacy
# from ski import extract_fuzzy_skills
import requests
import json
import pandas as pd
import re
import spacy
from spacy.matcher import Matcher
import sys
import traceback
# sys.path.append("D:\\Ex2_Projects\\Resume_parser\\components")
from parser.job_roles_extractor import extract_prev_job_roles
from parser.skills_Extractor import extract_skills
from parser.edu_extract import education_info, extract_degree
from parser.boolean_search import filter_finder , bool_finder
from parser.misc_funcs import extract_locations
from fuzzywuzzy import fuzz

from parser.main_func import exp_duration

# from sections import divide_resume_sections

nlp = spacy.load("en_core_web_sm")


class ResumeBot:

    def __init__(self, query, resume_filters,count):
        self.resume_filters=resume_filters
        self.query = str(query)
        self.count = count
        self.reply = self.match_reply(query)
        self.summary = self.search_summary(query)
        # return self.match_reply(query)
    # resume_filters = {
    #     "Candidate": {
    #         "check": [],
           
    #     },
    #     "Education": {
    #         "check": [],
            
    #     },
    #     "WorkExperience":{
    #         "check": [],

    #     },
    #     "Contact": {
    #         "check": [],
          
    #     },
    #     "Skill": {
    #         "check": [],
           
    #     },

    # };
    exit_commands = ("exit","quit","pause","goodbye","bye","later")
    search_terms = ["find","search","retrieve","show", "get","give","provide"]
    management_terms = ["save","update","delete", "add","create", "count","many","much","number"]
    role_category=["Web Developers", "UI UX Developers","Quality Assurance and Testing","Data and Analytics"]
    edu_level_patter = r""
    management_queries = ["Update filter","Delete filter","Save filter", "add filter", "Create Filter"]
    category = {
        "Education":r'(?i)education',
        "Experience":r'(?i)experience',        
    }
    
    # count = 0

   


    def extract_scores(self,text):
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
    



    

    def preprocessing(self,query):
    # Define the characters to remove
        chars_to_remove = '.,\'"{}[]()/?'       
        pattern = '[' + re.escape(chars_to_remove) + ']'        
        clean_query = re.sub(pattern, ' ', query)
        print(clean_query)
        return clean_query

    def greet(self):
        # self.name = input("what is your name ?\n")
        first_response = input(
            f"Hello, I am Resume bot.\n I can help you managing the resumes?\n")
        # if first_response in self.negative_res:
        #     print("have nice earth day!")
        #     return 
        self.chat()

    def make_exit(self, reply): 

        for cmd in self.exit_commands:
            rep = self.preprocessing(reply).split()
            # print(rep)
            if cmd in rep:        
        # if reply in self.exit_commands:
        #     print("have a nice day!!")
                return True
        # print("false")
        return False
        
    def chat(self):
        reply = input("What can I do for you: ")
        while not self.make_exit(reply.lower()):
            # print("another reply: ", end="")
            reply = input(self.match_reply(reply))
            print("\n")

    def match_reply(self, reply):

        print("reply send to us : ",reply)

        if not self.make_exit(reply.lower()):

            matched = False

            for a in self.management_terms:
                    # print("firstr trying to manage", a, reply.lower())
                    if a in reply.lower():                
                        matched = True
                        # print("match",a)
                        records = self.manage_query(reply, a)
                        # print("hogaya")
                        # return self.manage_query(reply, a) 
                        if type(records)==str:
                            print(records, "count string")
                            return  [records,self.resume_filters,self.count]  
                        else:                         
                            return [records,self.resume_filters,self.count]   
            # print("match_reply")
            
                    
                
            if not matched:
                for a in self.search_terms:
                    if a in reply.lower():                
                        matched = True
                        print("search_query")
                        records = self.search_query(reply)
                        if records is None:           
                            print("No records found")
                            return ["No records found", self.resume_filters, self.count]
                        
                        return [records,self.resume_filters,self.count]   
            
            if not matched:
                return ["Try Again\n", self.resume_filters,self.count]
            else:
                # print(self.resume_filters)
                return ["What Else do you want ?\n",self.resume_filters,self.count]
        else:
            return  ["exit",self.resume_filters,self.count]  

        

    def call_api(self,api_name, data):

        if type(data)==str:
            data = {
                "cat_name":str(data)
            }

        # print("data",data)
        try:
            # url = "https://armss-be.exitest.com/"+api_name
            url = "http://localhost:8000/"+api_name
            headers = {"Content-type": "application/json", "Accept": "application/json"}

            json_object = json.dumps(data, indent = 4) 
         
            response = requests.post(
                url,
                json=data,
                headers=headers,
            )
            response.raise_for_status()  # Radata=json.dumps(data), headers=headersise an exception for HTTP errors
            # print("Data sent successfully:", response.json())
            # self.count = response.json()[0]
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}") 
        return None



    def search_summary(self,query):


        get_roles, skills, score, deg, loc, exp_years = self.data_extractor(query)
        
        summary = "Showing resumes"
        if skills:

            if len(skills)>=2:

                summary+= f" Proficient in {', '.join(skills[:-1])} and {skills[-1]}"
            
            else:
                summary+=f" Proficient in  {skills[-1]}"

        if get_roles:

            if len(get_roles)>=2:
                summary+=f". Have experience in {', '.join(get_roles[:-1])} and {get_roles[-1]}"
            else:
                summary+=f". Have experience in {get_roles[-1]}"
        
        if loc:

            if len(loc)>=2:
                summary+= f" based in {', '.join(loc[:-1])} and {loc[-1]} "
            else:
                summary+= f" based in {loc[-1]} "

        if exp_years:
            summary+=f"and having an experience of {exp_years[0]} plus years"
                

        print("summmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm", summary)

        return  summary+"."


    def data_extractor(self, query):
        
        get_roles = extract_prev_job_roles(query)
        skills = extract_skills(query)   

        # score = self.extract_scores(query)
        score = []
        # level = ""
        degree = extract_degree(query)
        deg = []
        for k in degree:
            deg.append(k)

        loc = extract_locations(query)
        exp_years = exp_duration(query) if exp_duration else []
        # print("Locations extracted: ", loc)


        return get_roles, skills, score, deg, loc, exp_years
        # branch = ""
        # institute = ""
        # print(education_info(query))

    def filter_extractor(self, query):

        get_roles, skills, score, deg, loc, exp_years = self.data_extractor(query)
        # self.summary=self.search_summary(get_roles,skills,loc,exp_years)
        # print(self.summary,"...............................")
        print(get_roles, skills, score, deg, loc, exp_years)
        amount = 0
        print("Resume :",self.resume_filters)
        self.resume_filters["Skill"]["check"] = []
        self.resume_filters["Education"]["check"] = []
        self.resume_filters["WorkExperience"]["check"] = []
        self.resume_filters["Candidate"]["check"] = []

        if skills:
            
            self.resume_filters["Skill"]["check"].append("SkillName")
            self.resume_filters["Skill"]["SkillName"] = skills
        
        if score:
            
            self.resume_filters["Education"]["check"].append("Score")
            self.resume_filters["Education"]["Score"] = score
        
        if deg:
            
            self.resume_filters["Education"]["check"].append("Degree")
            self.resume_filters["Education"]["Degree"] = deg

        if get_roles:

            self.resume_filters["WorkExperience"]["check"].append("Role")
            self.resume_filters["WorkExperience"]["Role"] = get_roles
        
        if loc:
            self.resume_filters["WorkExperience"]["check"].append("Location")
            self.resume_filters["WorkExperience"]["Location"] = loc

        if exp_years:
            self.resume_filters["Candidate"]["check"].append("Experience")
            self.resume_filters["Candidate"]["Experience"] = exp_years



        print("after_filter_extraction", self.resume_filters)
       
        try:
            # search_results = self.call_api("displayfilter", self.resume_filters)
            search_results = self.call_api("chatbotfilter", self.resume_filters)

            if search_results:
                self.count = len(set(search_results))
            return search_results
        except Exception as e:
            traceback.print_exc()

            print(f"An error occurred: {e}")
            return None 
        
   

    def check_category(self,query):
        with open('data/SkillsData/Category.json', 'r') as file:
            skill_category = json.load(file) 

        for key, values in skill_category.items():
            for v in values:
                similarity_ratio = fuzz.partial_ratio(v, query)
                if similarity_ratio>=80:
                    return {key:v}
        
        return None


     
              

    def search_query(self,query):
        
        try:

            category = self.check_category(query)

            if category:
                return category
            else:

                query = self.preprocessing(query)
                query_list, bools = bool_finder(query)
                print("search_query after bool finder:",query_list,bools)
                resumes= []
                for query in query_list:
                    print("something1")
                    resumes.append(self.filter_extractor(query))
                print(resumes)
                # exp_filter = self.filter_extractor(query)
                print("something")
                if bools:
                    for i in range(len(bools)):
                        if bools[i]=="and":

                            print("first",len(resumes[i+1]))
                            intersection = set(resumes[i]).intersection(set(resumes[i+1]))
                            # resumes[i] = intersection
                            resumes[i+1] = intersection
                            print("second",len(resumes[i+1]))
                            
                        else:
                            union = set(resumes[i]).union(set(resumes[i+1]))
                            resumes[i+1]=union
                # print(len(resumes[-1]))
                return resumes[-1]
        except Exception as e:
            traceback.print_exc()
            print(f"Chatbot Search Query error occurred: {e}")
            return None
    

 
    

    def filter_addition(self, query):
        get_roles, skills, score, deg, loc, exp_years = self.data_extractor(query)
        amount = 0
        if skills:
            if "SkillName" not in  self.resume_filters["Skill"]["check"]:
                self.resume_filters["Skill"]["check"].append("SkillName")
                self.resume_filters["Skill"]["SkillName"] = skills
            else:
                self.resume_filters["Skill"]["SkillName"] += skills

            
        if score:
            if "Score" not in  self.resume_filters["Education"]["check"]:
                self.resume_filters["Education"]["check"].append("Score")
                self.resume_filters["Education"]["Score"] = score
            else:
                self.resume_filters["Education"]["Score"] += score           
        
        if deg:
            if "Degree" not in  self.resume_filters["Education"]["check"]:
                self.resume_filters["Education"]["check"].append("Degree")
                self.resume_filters["Education"]["Degree"] = deg
            else:
                self.resume_filters["Education"]["Degree"] += deg
           

        if get_roles:
            if "Role" not in  self.resume_filters["WorkExperience"]["check"]:
                self.resume_filters["WorkExperience"]["check"].append("Role")
                self.resume_filters["WorkExperience"]["Role"] = get_roles
            else:
                self.resume_filters["WorkExperience"]["Role"] += get_roles
        if loc:
            if "Location" not in  self.resume_filters["WorkExperience"]["check"]:
                self.resume_filters["WorkExperience"]["check"].append("Location")
                self.resume_filters["WorkExperience"]["Location"] = loc
            else:
                self.resume_filters["WorkExperience"]["Location"] += loc
        
        if exp_years:

            if "Experience" not in  self.resume_filters["Candidate"]["check"]:
                self.resume_filters["Candidate"]["check"].append("Experience")
                self.resume_filters["Candidate"]["Experience"] = exp_years
            else:
                self.resume_filters["Candidate"]["Experience"] += exp_years
            

    

        # print(self.resume_filters)
        # search_results = self.call_api("filter", self.resume_filters)

        try:
            search_results = self.call_api("chatbotfilter", self.resume_filters)
            if search_results:
                self.count = len(set(search_results))
            
            print("added", search_results)
            return search_results
        except Exception as e:
            traceback.print_exc()

            print(f"An error occurred: {e}")
            return None 


        # pass

    def filter_deletion(self, query):
        get_roles, skills, score, deg, loc, exp_years = self.data_extractor(query)
        amount = 0
        if skills:
            if "SkillName" in  self.resume_filters["Skill"]["check"]:

                for skill in self.resume_filters["Skill"]["SkillName"]:
                    if skill in skills:
                        self.resume_filters["Skill"]["SkillName"].remove(skill)
                        self.resume_filters["Skill"]["check"].remove("SkillName")          

            
        if score:
            if "Score" in  self.resume_filters["Education"]["check"]:
                for s in self.resume_filters["Education"]["Score"]:
                    if s in score:
                        self.resume_filters["Education"]["Score"].remove(s)  
                        self.resume_filters["Education"]["check"].remove("Score")
        
        if deg:
            if "Degree" in  self.resume_filters["Education"]["check"]:
               for d in self.resume_filters["Education"]["Degree"]:
                    if d in deg:
                        self.resume_filters["Education"]["Degree"].remove(d) 
                        self.resume_filters["Education"]["check"].remove("Degree")

        if get_roles:
            if "Role" in  self.resume_filters["WorkExperience"]["check"]:
                for r in self.resume_filters["WorkExperience"]["Role"]:
                    if r in get_roles:
                        self.resume_filters["WorkExperience"]["Role"].remove(r)
                        self.resume_filters["WorkExperience"]["check"].remove("Role") 
        if loc:
            if "Location" in  self.resume_filters["WorkExperience"]["check"]:
                for l in self.resume_filters["WorkExperience"]["Location"]:
                    if l in loc:
                        self.resume_filters["WorkExperience"]["Location"].remove(l)
                        self.resume_filters["WorkExperience"]["check"].remove("Location") 
        if exp_years:
            if "Experience" in  self.resume_filters["Candidate"]["check"]:
                for l in self.resume_filters["Candidate"]["Experience"]:
                    if e in exp_years:
                        self.resume_filters["Candidate"]["Experience"].remove(e)
                        self.resume_filters["Candidate"]["check"].remove("Experience") 

        # print(self.resume_filters)

        try:
            search_results = self.call_api("chatbotfilter", self.resume_filters)
            if search_results:
                self.count = len(set(search_results))
            
            # print("added", search_results)
            print("after deletion:",self.count)
            return search_results
        except Exception as e:
            traceback.print_exc()

            print(f"An error occurred: {e}")
            return None 


        # pass


    def saving_filter(self, query):
        data = str(self.resume_filters)
        try:
            url = "http://localhost:8000/filter"
            headers = {"Content-type": "application/json", "Accept": "application/json"}

            json_object = json.dumps(data, indent = 4) 
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
        
        return "Filter saved! "

    def count_resume(self, query):

        print("check count")
        present_category = []
        for cate in self.role_category:
            # print(cate.lower())
            
            if cate.lower() in query.lower():
                print(f"'{cate}' is present in the query.")
                present_category.append(cate)

        if present_category:
            for item in present_category: 
                print(item, "category inside")               
                mapped_data =  self.call_api("skillmap",item)
                self.count = mapped_data[0]
                return f"{self.count} records found for {item}"

        else:

        
        # print("count fucntion activated")
            get_roles, skills, score, deg, loc, exp_years = self.data_extractor(query)

            # print("count exp", get_roles, skills, score, deg, loc, exp_years)
            amount = 0

            if skills or score or deg or get_roles or loc or exp_years:
                self.resume_filters["Skill"]["check"] = []
                self.resume_filters["Education"]["check"] = []
                self.resume_filters["WorkExperience"]["check"] = []
                self.resume_filters["Candidate"]["check"] = []

                if skills:
                    self.resume_filters["Skill"]["check"].append("SkillName")
                    self.resume_filters["Skill"]["SkillName"] = skills
                
                if score:
                    self.resume_filters["Education"]["check"].append("Score")
                    self.resume_filters["Education"]["Score"] = score
                
                if deg:
                    self.resume_filters["Education"]["check"].append("Degree")
                    self.resume_filters["Education"]["Degree"] = deg

                if get_roles:
                    self.resume_filters["WorkExperience"]["check"].append("Role")
                    self.resume_filters["WorkExperience"]["Role"] = get_roles
                if loc:
                    self.resume_filters["WorkExperience"]["check"].append("Location")
                    self.resume_filters["WorkExperience"]["Location"] = loc
                if exp_years:

                    # print("check exp_years")
                    self.resume_filters["Candidate"]["check"].append("Experience")

                    # print("check check array",self.resume_filters["Candidate"]["check"] )
                    self.resume_filters["Candidate"]["Experience"] = exp_years


                data = self.resume_filters
                # print("count resume filters", self.resume_filters)
                count_Result = self.call_api("chatbotfilter", data)

                if count_Result:
              
                    self.count = len(set(count_Result))
                # return f"{self.count} records found"
                return count_Result
            
                
             
                
            else:

                # return f"{self.count} records found in previous filter"
                return []


    def manage_query(self, query, cmd):

        print("entering manage query")
        query = self.preprocessing(query)
        # exp_filter = self.filter_extractor(query)  

        try: 
            if cmd == "add":
                add_filter = self.filter_addition(query)   
                return add_filter
            elif cmd=="delete":
                # delete_filter = self.filter_deletion(query)  
                return self.filter_deletion(query)  
                
            elif cmd == "save":
                save_filter = self.saving_filter(query)  
            elif cmd in ["many","much","count","number"]:
                print("entering count query")
                query = self.preprocessing(query)
                query_list, bools = bool_finder(query)
                
                counts= []
                for query in query_list:
                    # print("something1")
                    counts.append(self.count_resume(query))
                # print("counts array: ",counts)
                # exp_filter = self.filter_extractor(query)
         
                if bools:
                    for i in range(len(bools)):
                        if bools[i]=="and":

                            print("first",len(counts[i+1]))
                            intersection = set(counts[i]).intersection(set(counts[i+1]))
                            # resumes[i] = intersection
                            counts[i+1] = intersection
                            print("second",len(counts[i+1]))
                            
                        else:
                            union = set(counts[i]).union(set(counts[i+1]))
                            counts[i+1]=union
                # counts = []
                # resume_count = self.count_resume(query)
                if counts[-1]:
                    resume_count =len(set(counts[-1]))


                

                    print("count........................................", resume_count)
                    self.count = resume_count
                    return f"{resume_count} records found"
                else:
                    # return f"{self.count} records found in previous filter"
                    return "No Records Found"

                # print(resume_count)  
        except Exception as e:
            traceback.print_exc()

              # Rollback the transaction if an error occurs
            print(f"Manage query Error occurred: {str(e)}")
            return []     

        
        return "something got managed\n"
    



# bot = ResumeBot()
# bot.greet()
# bot.filter_education("Find resumes with project management experience montfort school, institute 7.6 cgpa")
# bot.search_query("""hlo """)

    

# don't type . in btech
    # nlp = spacy.load("en_core_web_md")  # make sure to use larger package!
    # doc1 = nlp("Help me in adding this filter int o the current filters we have applied")







    # for q in management_queries:
    #     doc2 = nlp(q)
    #     print(doc1, "<->", doc2, doc1.similarity(doc2))



# print(extract_fuzzy_skills('Can you help me find resumes with experience in cat waling'))
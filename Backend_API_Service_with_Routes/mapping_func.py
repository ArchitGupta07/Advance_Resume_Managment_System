def calculate_max_skills_match(skills_list_1, skills_list_2):
    max_matches = 0
    for skill_1 in skills_list_1:
        matches = sum(1 for skill_2 in skills_list_2 if skill_1.lower() == skill_2.lower())
        max_matches = max(max_matches, matches)
    return max_matches

# Example list of roles
import json 
with open('data/SkillsData/Category.json', 'r') as file:
    skills_map = json.load(file)
with open('data/SkillsData/categorySubs.json', 'r') as file:
    categorySubs = json.load(file)



def find_best_match(given_role):

    min_distance = float('inf')
    best_match = "None"


    best_key = "None"
    min_key_distance = float('inf')   

    print(given_role.lower().split())
    if "developer" in given_role.lower().split():
        print("developer detected")
        for v in skills_map["Software Development & Engineering"]:
            distance = levenshtein_distance(given_role.lower(), v.lower())
            # print(distance, v)
            if distance < min_distance:
                min_distance = distance
                best_match = v

    else: 
        for key ,value in skills_map.items():
            distance = levenshtein_distance(given_role.lower(), key.lower())
            # print(distance, key,",==============================================)")
            if distance < min_key_distance:
                min_key_distance = distance
                best_key = key
        # print(best_key)
        for v in skills_map[best_key]:
            distance = levenshtein_distance(given_role.lower(), v.lower())
            # print(distance, v)
            if distance < min_distance:
                min_distance = distance
                best_match = v

    
    return best_match, "letter"
  


    

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]





from fuzzywuzzy import fuzz


# def category_finder(given_role):
#     max_match=0
#     best_match=None

#     best_key = None


#     for key  in skills_map:
#         if fuzz.ratio(key.lower(), given_role)>=20:
#             max_match=max(max_match, fuzz.ratio(key.lower(), given_role))
#             if max_match == fuzz.ratio(key.lower(), given_role):
#                 best_key = key
#     # for key ,value in skills_map.items(): 
#     print("best key-----------------------",best_key)   
#     max_match=0

#     if best_key:
#         for v in skills_map[best_key]:

#             if v in categorySubs and categorySubs[v]:

#                 for s in categorySubs[v]:
#                     if fuzz.ratio(s.lower(), given_role)>=75:
#                         max_match=max(max_match, fuzz.ratio(s.lower(), given_role))
#                         if max_match == fuzz.ratio(s.lower(), given_role):
#                             best_match = v.lower()




#             else:
#             # print(v.lower(),given_role.lower(),fuzz.ratio(v.lower(), given_role))        
#                 if fuzz.ratio(v.lower(), given_role)>=60:
#                     max_match=max(max_match, fuzz.ratio(v.lower(), given_role))
#                     if max_match == fuzz.ratio(v.lower(), given_role):
#                         best_match = v.lower()
#     return best_match


def category_finder(given_role):
    max_match=0
    best_match=None

    best_key = None


    for key  in skills_map:
    #     if fuzz.ratio(key.lower(), given_role)>=20:
    #         max_match=max(max_match, fuzz.ratio(key.lower(), given_role))
    #         if max_match == fuzz.ratio(key.lower(), given_role):
    #             best_key = key
    # # for key ,value in skills_map.items(): 
    # print("best key-----------------------",best_key)   
    # max_match=0

    # if best_key:
        for v in skills_map[key]:

            if v in categorySubs and categorySubs[v]:

                for s in categorySubs[v]:

                    fuzz_score = fuzz.partial_ratio(s.lower(), given_role)
                    print(fuzz_score, s)
                    if fuzz_score>=75:

                        # if 
                        max_match=max(max_match, fuzz_score)
                        if max_match == fuzz_score:

                            best_match = v.lower()




            else:
                fuzz_score_v = fuzz.partial_ratio(v.lower(), given_role)
                print(fuzz_score_v, v)
            # print(v.lower(),given_role.lower(),fuzz.ratio(v.lower(), given_role))        
                if fuzz_score_v>=60:
                    # max_match=max(max_match, fuzz.ratio(v.lower(), given_role))
                    max_match=max(max_match, fuzz_score_v)
                    if max_match == fuzz_score_v:
                        best_match = v.lower()
    return best_match
        

def skill_based_category(resumeSkills):
    with open('data/SkillsData/skillsMapping.json', 'r') as file:
        categories = json.load(file)
    max_per = 0
    max_match = None

    resumeSkills = [i.lower() for i in resumeSkills]
    # print(categories)

    for category, category_skills in categories.items():

        matching_skills = set(category_skills) & set(resumeSkills)
        percentage_matched = (len(matching_skills) / len(category_skills)) * 100


        print(matching_skills, category,percentage_matched )
        max_per = max(max_per, percentage_matched)
        if max_per==percentage_matched:
            max_match=category

    return max_match

    





# given_role = "  software intern   "
# given_role = "Tech functional Business Analyst"

# print("besttttttttttttttttttttt",category_finder(' '.join(given_role.split()).lower()))


# Given role
# print(skills_map)

# 
# given_role = "wowddfwfweewvw back end developer"


# best_match = find_best_match(" software developer    ")
# print("Best match:", best_match)
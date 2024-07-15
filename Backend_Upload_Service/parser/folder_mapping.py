import json

import os

def file_exists(filename):
    return os.path.exists(filename)

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

log_data = read_json_file("api/data/SkillsData/skillsMapping.json")

# print(log_data["Frontend Developer"])

from collections import defaultdict
from nltk.tokenize import word_tokenize

roles = {
    "Software Development & Engineering": ["Frontend Developer", "Backend Developer", "Full Stack Developer", "DevOps Engineer", "Software Architect", "UI/UX Developer", "Mobile App Developer", "Embedded Systems Engineer", "Quality Assurance Engineer"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue", "angular", "typescript", "responsive design"],
    "Backend Developer": ["node", "express", "django", "flask", "ruby on rails", "asp.net", "sql", "mongodb"],
    "Full Stack Developer": [],
    "DevOps Engineer": []
}

def calculate_similarity(roles, experience_roles):
    similarity_scores = defaultdict(float)
    for role in roles:
        for exp_role in experience_roles:
            role_tokens = set(word_tokenize(role.lower()))
            exp_role_tokens = set(word_tokenize(exp_role.lower()))
            similarity = len(role_tokens.intersection(exp_role_tokens)) / len(role_tokens.union(exp_role_tokens))
            similarity_scores[role] = max(similarity_scores[role], similarity)
    return similarity_scores

def map_experience_to_folder(experiences):
    max_similarity = defaultdict(float)
    max_role = {}
    for exp in experiences:
        exp_roles = exp["roles"]
        # print(exp_roles, roles.values())
        similarity_scores = calculate_similarity(roles.values(), exp_roles)
        for role, similarity in similarity_scores.items():
            if similarity > max_similarity[exp["id"]]:
                max_similarity[exp["id"]] = similarity
                max_role[exp["id"]] = role

    experience_folder_map = defaultdict(list)
    for exp_id, role in max_role.items():
        experience_folder_map[role].append(exp_id)

    return experience_folder_map

# Example experiences
experiences = [
    {"id": 1, "roles": ["Frontend Developer", "UI/UX Developer"]},
    {"id": 2, "roles": ["Backend Developer", "SQL"]},
    {"id": 3, "roles": ["Mobile App Developer", "iOS", "Android"]},
    {"id": 4, "roles": ["DevOps Engineer", "AWS", "Docker"]}
]

folder_map = map_experience_to_folder(experiences)
for role, exp_ids in folder_map.items():
    # print(f"Folder for {role}: {exp_ids}")
    pass

import re
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

def extract_prev_job_roles(text):
    job_roles = [
        "intern",
        "trainee",
        "internship" ,
        "analyst",
        "developer",
        "manager",
        "engineer",
        "consultant",
        "designer",
        "specialist",
        "coordinator",
        "administrator",
        "executive",
        "assistant",
        "supervisor",
        "technician",
        "associate",
        "officer",
        # "leader",
        "expert",
        "advisor",
        "strategist",
        "resources",
        "tester",
    ]

    text = text.replace("\n", " ")
    text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # print(text)
    matcher = Matcher(nlp.vocab)
    pattern = [ {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
                {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},]
    matcher.add("PROPER_NOUNS", [pattern], greedy="LONGEST")
    doc = nlp(text)

    # for token in doc:
    #     print(token, token.dep_, token.pos_)

    jobs = []
    matches = matcher(doc)

    for match in matches:
        check_role = str(doc[match[1] : match[2]]).lower()

        for role in job_roles:
            if role in check_role.split() and role != check_role:
                # print(check_role)
                jobs.append(" ".join(check_role.split()[:check_role.split().index(role)+1]))

    return list(set(jobs))
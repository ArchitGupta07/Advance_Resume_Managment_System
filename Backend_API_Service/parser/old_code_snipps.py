def extract_degree(text):
    pattern = r'\b(?:((B|b|M|m)\.[a-zA-Z]{1,5})|BBA|MBA|BCA|MCA|)\b'
   

    lines = text.split('\n') 
    deg=[]      
    for line in lines:
        # print(line)
        match1 = list(re.findall(pattern, line))
        # match2 = list(re.findall(per_pattern, line))


        if match1!=[] and match1[0][0]!="":
            # print(match)
            
            deg.append(match1[0][0].lower())
            # print(match1)
    degree_pattern = [
        {"LOWER": {"IN": ["bachelor", "masters", "phd", "doctorate", "post graduate","diploma"]}},
        {"LOWER": {"IN": ["in", "of"]}, "OP": "?"},
        {"IS_SPACE": True, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
        {"LOWER": {"IN": ["in"]}, "OP": "?"},
        {"IS_SPACE": True, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "*"},
    ]
    # print(jobs)

    degree_pattern[0]["LOWER"]["IN"]+=deg
    # print(degree_pattern)


    matcher = Matcher(nlp.vocab)
    matcher.add("PROPER_NOUNS", [degree_pattern], greedy='LONGEST')
    doc = nlp(text)

    # for token in doc:
    #     print(token, token.pos_)
    matches = matcher(doc)
    # print (len(matches), "matches got")
    degrees=[]
    for match in matches[:10]:
        # print (match, doc[match[1]:match[2]])
        degrees.append(doc[match[1]:match[2]])

      

    # print(ans[0][2])
    return degrees



# ============================================Phone===================================================================

def extract_mobile_number(text):
    phone = re.findall(
        re.compile(
            r"(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4,5})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"
        ),
        text,
    )

    if phone:
        number = "".join(phone[0])
        if len(number) > 10:
            return "+" + number
        else:
            return number
        
        #  ============================================Phone===================================================================
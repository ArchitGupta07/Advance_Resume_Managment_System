

from main_func import extract_name, extract_skills, extract_locations2,extract_email, extract_urls
from Font_extractor import get_name, download_pdf


import os
def process_file(text,skills,locations,emails,urls):
    # Your function to process each file

    
    if skills:
        # print(skills)
        for s in skills:
            text = text.replace(s.lower(),"")

    if locations:
        # print(locations)
        for l in locations:
            if l.lower() not in ["kumar","anand"]:
                text = text.replace(l.lower(),"")
    if emails:
        # print(emails)
        for e in emails:
            text = text.replace(e.lower(),"")

    if urls:
        # print(urls)
        for u in urls:
            # for part in u.split("/"):
                # print(part)

                # if part.lower() not in ["in"] and len(part.lower())>=3:
                    text = text.replace(u.lower(),"")
                    
    text = text.replace("linkedin", "")
    text = text.replace("github", "")
    text = text.replace("hub","")    
    text = text.replace("_"," ")
    text = text.replace("-","")    

    # print(text[:1000])
    print("\n\n")

    # print(f"gives name {extract_name(text)}")
    print("\n\n")

    return text






folder_path = 'data/resumes'

pdf_url = "https://minio-endpoint.skilldify.ai/armss-dev/%5B80%5D-b432ae9362cafc2e08ba89ec01cd65038081ae6e9b8cd795ccdded5868903726vineetaSharma%5B0_0%5D.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240529%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240529T045722Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=96b165f52e976557fa5f50f6c2daeb566096d43b36acdc4dcb4dfe9638dce13f"
local_pdf_path = "downloaded.pdf"

download_pdf(pdf_url,local_pdf_path)

name = get_name(local_pdf_path)

if name:
     print(name)
else:
     name = extract_name(process_file(pdf_url))
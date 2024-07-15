# import fitz  # PyMuPDF
# # from main_func import extract_name

# pdf_path = "data/resumes/resume32.pdf"
# pdf_document = fitz.open(pdf_path)
# text = ""
# for page_num in range(pdf_document.page_count):
#     page = pdf_document.load_page(page_num)
#     text += page.get_text("text")
# pdf_document.close()
# print(text)


# # import pdfplumber

# # pdf_path = "data/resumes/resume32.pdf"
# # with pdfplumber.open(pdf_path) as pdf:
# #     text = ""
# #     for page in pdf.pages:
# #         text += page.extract_text()
# # print(text)

# def capitalize_words(input_string):
#     return ' '.join(word.capitalize() for word in input_string.split())

# import spacy
# from spacy.matcher import Matcher
# nlp = spacy.load("en_core_web_sm")

# matcher = Matcher(nlp.vocab)


# def extract_name(resume_text):
#     nlp_text = nlp(capitalize_words(resume_text.lower()))
    

#     # print(text)

#     for token in nlp_text:
#         print(token, token.dep_, token.pos_, token.ent_type_)
#     pattern = [{"POS": "PROPN", "DEP": {"IN": ["compound", "ROOT"]}}, {"POS": "PROPN", "DEP": {"IN": ["compound", "ROOT"]}}]
#     # "DEP": {"IN": ["compound", "nsubj"]}
#     matcher.add("NAME", patterns=[pattern])
#     matches = matcher(nlp_text)
#     for match_id, start, end in matches:
#         span = nlp_text[start:end]
#         return span.text


from tika import parser

pdf_path = "https://minio-endpoint.skilldify.ai/armss-dev/Pratyush_resume%20%281%29.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240508%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240508T110749Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a87bd3f9fc95e86ecbb098b53080271b2fe3a6b2ff0ace5bf8bb936950ef0973"
parsed_pdf = parser.from_file(pdf_path)
text = parsed_pdf["content"]
# print(text)

# print(extract_name(text))
# print(extract_name("flutter python"))

# import magic

# def check_file_type(file_path):
#     # Create a magic.Magic object
#     mime = magic.Magic(mime=True)
    
#     # Check the file type
#     file_type = mime.from_file(file_path)
#     return file_type


import requests

# # url = "https://minio-endpoint.skilldify.ai/armss-dev/Pratyush_resume%20%281%29.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240508%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240508T110749Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a87bd3f9fc95e86ecbb098b53080271b2fe3a6b2ff0ace5bf8bb936950ef0973"

# url ="D:\Ex2_Projects\Resume_parser\Resumes\demo.docx"
# url ="https://morth.nic.in/sites/default/files/dd12-13_0.pdf"
# url =  "https://minio-endpoint.skilldify.ai/armss-dev/Pratyush_resume%20%281%29.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240508%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240508T110749Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a87bd3f9fc95e86ecbb098b53080271b2fe3a6b2ff0ace5bf8bb936950ef0973"
url="https://minio-endpoint.skilldify.ai/armss-dev/resume.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240509%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240509T043019Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=369107137f6ca5e4bf745bc2b4e729d94df2c28dd4dc7805a7580b2693a0bbf1"


print(url.split("?")[0].split("."))
response = requests.head(url.split("?")[0].split("."))
content_type = response.headers.get('Content-Type')

print(f"File type: {content_type}")
# print(f"File type: {check_file_type("https://morth.nic.in/sites/default/files/dd12-13_0.pdf")}")

# print("file type",check_file_type("https://minio-endpoint.skilldify.ai/armss-dev/Pratyush_resume%20%281%29.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gNT1ijYwEy1ZcEmX%2F20240508%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240508T110749Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a87bd3f9fc95e86ecbb098b53080271b2fe3a6b2ff0ace5bf8bb936950ef0973"))
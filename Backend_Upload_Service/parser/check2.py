import re


def join_split_words(text):
    # Use regular expressions to find and replace single spaces within sequences of capital letters
    pattern = re.compile(r'(?<=\b[a-zA-Z]) (?=[a-zA-Z]\b)')
    
    # Replace single spaces with no space
    return pattern.sub('', text)

# Example input
text = """
y a s h   S H A R M A

i w o r words


S O F T W A R E   E N G I N E E R

C O N T A C T

P R O F I L E

+91 9818580167

syash520@gmail.com

https://syash5.github.io/bio/

Delhi, India

E D U C A T I O N

Guru Gobind Singh Indraprastha University
(2016-2020)

Bachelor of Technology in Computer Science

CGPA: 8.25
"""

# # Process the text
# cleaned_text = join_split_words(text)

# print(cleaned_text.replace("   "," "))

from text_extractor import tika_text_extraction

url = "https://minio-endpoint.exitest.com/armss-dev/%5B449%5D-4ee2fc8bb8c97e6e2871de12635d4d40072b581a5e503e83fe93de5bd16695fa%21%40%26Hasanmk-6.pdf-1%281%29.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=3G1coIOGQpk2Yvrxp9Ao%2F20240613%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20240613T045556Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=e1d1919a9491be32607cfbba8ec14ae5fb060c4f960f2b47857e84457ff04945"

text = tika_text_extraction(url)
cleaned_text = join_split_words(text)
# print(cleaned_text.replace("   "," "))


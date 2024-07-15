from text_extractor import extract_text_from_pdf, tika_text_extraction, extract_from_docx
import traceback
import os

os.environ['STANFORD_MODELS'] = '/path/to/stanford-ner/classifiers'
os.environ['CLASSPATH'] = '/path/to/stanford-ner/stanford-ner.jar'




# filePath = ""
# text = ""
# for page in extract_text_from_pdf(filePath):        
#     text += " " + page

import magic

def check_file_type(file_path):
    # Create a magic.Magic object
    mime = magic.Magic(mime=True)
    
    # Check the file type
    file_type = mime.from_file(file_path)
    return file_type


# import os
import nltk
from nltk.tag import StanfordNERTagger

# Set up environment variables (if not set globally)


# Initialize the tagger
stanford_tagger = StanfordNERTagger(
    model_filename='/path/to/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', 
    path_to_jar='/path/to/stanford-ner/stanford-ner.jar'
)

# Function to extract names
def extract_names(text):
    words = nltk.word_tokenize(text)
    tags = stanford_tagger.tag(words)
    names = [word for word, tag in tags if tag == 'PERSON']
    return names

# Example usage


# import os
def process_file(filePath):
    # Your function to process each file

    print(check_file_type(filePath))
    try:
        if check_file_type(filePath) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = extract_from_docx(filePath)

        elif check_file_type(filePath)=='application/pdf':
            text = ""
            for page in extract_text_from_pdf(filePath):        
                text += " " + page
        else:
            text = tika_text_extraction(filePath)
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")
        return None
    print(f"Processing file: {filePath} and name is {extract_names(text)}")
    # Add your file processing code here

def process_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):  # Ensure it's a file
            process_file(file_path)

# Example usage
folder_path = 'D:/Ex2_Projects/Resumes'
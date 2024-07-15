from geotext import GeoText
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')

def remove_prepositions(query):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(query)
    filtered_query = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_query)



def extract_locations(text):
    # capitalized_text =[word.capitalize() for word in text.split()]
    # print(capitalized_text)

    text = remove_prepositions(text)
    # print(text)

    cities = []
    countries = []

    for i in text.split():

        if i in ["of","Of","march","March","along"]:
            continue

        places = GeoText(i.capitalize())
        if places.cities:
            cities.append(i)
        elif places.countries:
            countries.append(i)


    # Extract states, cities, and countries
    # states = places.states
        # return states, cities, countries
    return list(set(cities))

import locationtagger

nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')

import logging

def extract_locations2(resume_text):

    try:
        place_entity = locationtagger.find_locations(text=resume_text.title())
        country_cities = dict(place_entity.country_cities)  

        if "India" in country_cities:
            # print("india")
            return country_cities["India"]
        else:
            return []
        
    except Exception as e:
        logging.error(f"An error occurred while extracting locations: {e}")
        return []
        
    
# query ="get all of hisar"

# print(query.title())

# print(extract_locations2(query))
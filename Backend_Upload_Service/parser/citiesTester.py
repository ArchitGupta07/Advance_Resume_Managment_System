from text_extractor import extract_text_from_pdf, divide_resume_sections, tika_text_extraction,extract_from_docx
from new_dateExtractor import extract_locations_from_text
from geotext import GeoText

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def main(filePath):
  
    emergency_text = tika_text_extraction(filePath)

    # emailForLocation = list(extract_email(text))

    # print('email for location ',emailForLocation)

    try:

        print('Extraction for ', filename, ' Starts Here\n\n')

        print('Raw Extraction: ', extract_locations_from_text(remove_prepositions(emergency_text).lower()),'\n\n')
        # workExText = divide_resume_sections(emergency_text)["Experience"].lower()
        
        firstExtraction = extract_locations(emergency_text.lower())
        
        print('first extraction of location: ', firstExtraction, '\n\n')

        extractedText = " ".join(firstExtraction)

        new_cities = extract_locations_from_text(extractedText.lower())

        print('new cities!!: ', new_cities,'\n\n')

        print('\n\nExtraction for ', filename, ' Ends Here\n\n')

        # print('cities after joinig: ',extractedText.title())
        # cities = extract_locations2(extractedText.title())
        
        # get_closest_location_to_present(workExText,cities)
        # get_closest_location_to_current(workExText,cities)
        # get_closest_location_to_till_date(workExText,cities)
        # get_closest_location_to_email(workExText,cities,emailForLocation[0])
        # print('cities are: ', cities)
    except:
        print('exception is here!!')


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

        if i in ["of","Of","march","March"]:
            continue

        places = GeoText(i.capitalize())
        if places.cities:
            cities.append(i)
        elif places.countries:
            countries.append(i)


    return list(set(cities))


# Gurugram
#pilani
#delhi public school
#sonipat
#resume18


filename = ''
for i in range(2,20):
    filename = f"resume{i}.pdf"

    try:

        main(f"../data/resumes/{filename}")
    except Exception as e:
        print(f"a exception {e} occured at: {filename}")
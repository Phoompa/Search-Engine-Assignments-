import os
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Download nltk stuff
nltk.download('punkt')
nltk.download('stopwords')

#Set up stop words
stop_words = set(stopwords.words('english'))

preprocessed_directory = 'preprocessed_data'
all_words = set()
#Loop through each file in the directory
for filename in os.listdir('data'):
    #Constructs file path for a specific file in data folder
    file_path = os.path.join('data',filename)
    print(file_path)
    
    # Had errors reading certain files, so try different encodings
    try:
        #Use utf-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        #Try with a different encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
        
    #Convert to lowercase
    content_lower = content.lower()
    #Create tokens
    tokens = word_tokenize(content_lower)
    #Remove stop words 
    filtered_tokens = [word for word in tokens if word not in stop_words]
    #Remove non-alphanumeric characters 
    processed_tokens = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in filtered_tokens]
    #Remove singly occurring characters like 'm' or 'a'
    processed_tokens = [word for word in processed_tokens if len(word) > 1]

    #Add processed tokens to the set
    all_words.update(processed_tokens)
    processed_text = ' '.join(processed_tokens)

    #Gets the file path to write the processed data
    preprocessed_file_path = os.path.join(preprocessed_directory, filename)

    #Write processed text to preprocessed_data
    with open(preprocessed_file_path, 'w', encoding='utf-8') as file:
        file.write(processed_text)
        
print("Complete")
print(f"Total unique words: {len(all_words)}")
print(type(processed_tokens))


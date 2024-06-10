import os
import nltk
import numpy as np
import pandas as pd
import matplotlib as plt
import re
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

DOC_TOTAL = 249

#Download nltk stuff
nltk.download('punkt')
nltk.download('stopwords')

#Set up stop words
stop_words = set(stopwords.words('english'))

preprocessed_directory = 'preprocessed_data'
all_words = set()
# list of all file names
filenames = []
#Loop through each file in the directory
for filename in os.listdir('data'):
    #Constructs file path for a specific file in data folder
    file_path = os.path.join('data',filename)
    filenames.append(filename)
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
    #Remove punctuation 
    processed_tokens = [re.sub(r'[\W_]+', '', word) for word in tokens if word]  # Remove punctuation
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
        
    
        
print(f"Total unique words: {len(all_words)}")
print("Question 1 Completed")

#initialize the positional index as a dictionary
positional_index = {}

#Load all words from preprocessed files and build the positional index:
for filename in os.listdir(preprocessed_directory):
    file_path = os.path.join(preprocessed_directory,filename)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = content.split()
        
        #iterate through each word and its index:
        for index, word in enumerate(words):
            if word not in positional_index:
                positional_index[word] = {}
            if filename not in positional_index[word]:
                positional_index[word][filename] = []
            positional_index[word][filename].append(index)
#position that the word occurs in is relative to the list of words and not the number of characters. So if document contains "This is", "This" is at position 0 and "is" at position 1
            
            
# Write positional index to a file:
with open('positional_index.txt', 'w') as file:
    for word, documents in positional_index.items():
        file.write(f"{word}: ")
        entries = []
        for doc, positions in documents.items():
            positions_str = ', '.join(map(str, positions))  # Convert list of positions to string
            entries.append(f"{doc} [{positions_str}]")
        document_positions = '; '.join(entries)  # Join all document entries with semicolon
        file.write(f"{document_positions}\n")
        file.write("\n")

print("Positional index complete")

while True:
    phrase = input("Please enter a phrase:   ")
    phrase = phrase.lower()

    words = phrase.split()
    if len(words) > 5:
        print("Query length must be less than 5.")
    else:
        break

#Dictionary to store the combined document positions for the phrase.
phrase_positions = {}


#collect positions for each word in the phrase
for word in words:
    if word in positional_index:
        for document, positions in positional_index[word].items():
            if document not in phrase_positions:
                phrase_positions[document] = []
            phrase_positions[document].extend(positions)
            
#sorting the positions in each document
for doc in phrase_positions:
    phrase_positions[doc].sort()

#print:
#for doc, positions in phrase_positions.items():
    #print(f"{doc}: {positions}")
    
results = {}

# Check for sequences of consecutive numbers matching the phrase length
for doc, positions in phrase_positions.items():
    if len(positions) < len(words):
        continue  # Skip if there aren't enough positions

    # Search for consecutive positions
    for i in range(len(positions) - len(words) + 1):
        # Check if the next positions are consecutive
        if all(positions[i + j] == positions[i] + j for j in range(len(words))):
            if doc not in results:
                results[doc] = []
            results[doc].extend(positions[i:i+len(words)])  # Extend flat list

# Output the results:
for doc, pos_list in results.items():
    print(f"{doc}: {sorted(set(pos_list))}")  # Remove duplicates and sort
    print("\n")


##################################################################
# TF-IDF MATRIX
"""
Term Frequency
Inverted Document Frequency

Matrix = columns[[row],[row],[row]] <-- way to reduce storage size?


same dataset as Q1

"""

tf_dic = {}
doc_count = {}

for word in positional_index:
    d = {}
    for doc in positional_index[word]:
        d.update({doc : len(positional_index[word][doc])})
        
    tf_dic.update({word : d.copy()})
    doc_count.update({word : len(positional_index[word])})
    
    
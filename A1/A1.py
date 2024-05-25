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
        
print(f"Total unique words: {len(all_words)}")
print("Question 1 Completed")

#Initialize the inverted index as a dictionary
inverted_index = {}
#iterate through each word in all_words
for word in all_words:
    #assign an empty set for each word in the dictionary
    inverted_index[word] = set()


#Iterate through preprocessed files.
for filename in os.listdir(preprocessed_directory):
    file_path = os.path.join(preprocessed_directory, filename)
    print("Adding file to inverted index: ", filename)
    
    with open(file_path, 'r', encoding = 'utf-8') as file:
        content = file.read()
        #Create a set of words in the document
        words = set(content.split())
        
        #iterates through each word 
        for word in words:
            #if word appears in dictionary, add filename to the corresponding set.
            if word in inverted_index:
                inverted_index[word].add(filename)
                
#print out the inverted index to see the structure
#k and v represent key-value pairs. for key k, convert the set v into a list for each item in dictionary
#print("Inverted Index: ", {k: list(v) for k, v in inverted_index.items()})  # Print a small sample for clarity
#print("Inverted Index: ", inverted_index)

#Decided to use this so I could view the entire dictionary. The print code above ^^ only showed me a sample
# Write to a text file
with open('inverted_index.txt', 'w') as file:
    for key, values in inverted_index.items():
        # Convert the set to a list and join with commas
        values_list = ', '.join(values)
        file.write(f"{key}: {values_list}\n")
        
        
########################################################################
# QUERY INPUT

# input number of queries wanted
while True:
    try:
        number = int(input("Number of Queries: "))
    except:
        print("ERROR: please type a number")
        continue
    break

# run for as many queries as asked
for n in range(number):
    
    #Repeats asking for input if invalid
    while True:
        
        #sentence input
        input_s = input("Input sentence: ")
        #OPERATIONS INPUT FORMATTED AS op1,op2,... (i.e. OR,AND NOT)
        input_o = input("Input operation sequence: ")
        input_o = input_o.upper()
        query_o = input_o.split(',')
        
        ## preprocess query sentence, similar to how tokens are preprocessed
        input_s = input_s.lower()
        input_s = word_tokenize(input_s)
        q_tokens = [word for word in input_s if word not in stop_words]
        q_tokens = [re.sub(r'[^a-zA-Z0-9]+', '', word) for word in q_tokens]
        query_s = [word for word in q_tokens if len(word) > 1]
        
        #Error handling
        if len(query_s) != len(query_o)+1:
            print("ERROR: Unmatching number of tokens/ops, try again")
            print("Tokens: {}".format(query_s))
            print("Operations: {}".format(query_o))
            print("---")
            continue
        elif query_o not in ['AND','OR','OR NOT','AND NOT']:
            print("ERROR: Invalid operator(s), try again")
            print("Tokens: {}".format(query_s))
            print("Operations: {}".format(query_o))
            print("---")
            continue
        break
    
    #Initializes retrieved document set to first token from query
    doc_list = inverted_index[query_s[0]] 
    
    i = 1
    comp = 0
    while i < len(query_s):
        word = query_s[i]
        op = query_o[i-1]
        
        #different actions taken depending on operation specified
        match op:
            case 'AND':
                # intersection with current doc_list
                doc_list.intersection(inverted_index[word])
                
            case 'OR':
                # add searched word doc_list to current list
                doc_list.update(inverted_index[word])
                
            case 'AND NOT':
                #get word document list, check if any in doc_list, delete from list
                for d in list(inverted_index[word]):
                    doc_list.discard(d)
                    comp +=1 
                
            case 'OR NOT':
                #get every document which does not have current word
                for fn in filenames:
                    if fn not in doc_list and fn not in inverted_index[word]:
                        doc_list.add(fn)
                        comp +=1    
        i+=1
        
    #print query output
    print("QUERY #{}".format(n+1))
    print("Tokens: {}")
    print("Number of matched documents: {}".format((len(doc_list))))
    print("Minimum number of comparisons required: {}".format(comp))
    print("Retrieved document names: {}".format(list(doc_list)))
    print("---")



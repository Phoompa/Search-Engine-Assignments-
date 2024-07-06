import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#Retrieve the web page
url = "https://en.wikipedia.org/wiki/List_of_Canadian_provinces_and_territories_by_historical_population"
#sends a GET request to the url and stores the response
response = requests.get(url)

#Check if the request was successful
if response.status_code == 200: #status code of 200 indicates a successful request
        raw_html = response.text
        print("Webpage retrieved successfully")
        
        #Decode the raw html using beautifulSoup
        
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        print(soup.prettify(formatter="html")) #formats html and prints it
        
        #extract relevant tables
        tables = soup.find_all('table', {'class' : 'wikitable'})
        
        #print # of tables ()
        print(len(tables))
        #display the first table
        if tables:
            print(tables[0].prettify())
            
        #merge relevant data into a dictionary
        tables_dict = {}
        
        for table in tables: #iterate through each table found on the url
            headers = [(th.get_text()).strip() for th in table.find_all('th')] #extracts all header cell text, sanitizes it, then stores the clean text in a list 
            
            for row in table.find_all('tr')[1:]: #Loops through all rows in a given table except the header row
                cells = row.find_all(['td','th']) # Finds all data cells ('<td>') and header cells ('<th>') in the given row
                if len(cells) == len(headers): #ensure that only rows with the correct # of columns are processed
                    for i, cell in enumerate(cells): #Iterate through each cell in a row
                        header = headers[i] #get corresponding header
                        value = (cell.get_text()).strip() #extract value of the cell
                        if header not in tables_dict:
                            tables_dict[header] = [] #append header to dictionary if it doesn't already exist
                            
                        tables_dict[header].append(value)
                        
        #print the complete dictionary
        print(tables_dict)
        print()
        
        print("Printing all <h2> text elements:")
        h2_list = soup.find_all("h2") #find all <h2> tags
        for h2 in h2_list:
            print(h2.text) #print out extracted text from <h2> tags
        
        print()
        print("Creating list of hyperlinks found in the table list:")
        hyperlinks = [] 
        for table in tables:
            for link in table.find_all('a'): #find all links
                hyperlinks.append(link.get('href')) #extract text from links
        print(hyperlinks)
            
        dir = "webpages" #directory for downloaded webpages
        
        print()
        print("Downloading other webpages from hyperlinks:")
        hyperlinks = list(dict.fromkeys(hyperlinks)) # remove duplicates
        
        for link in hyperlinks:
            if link.startswith('#'): #skip over citation notes
                continue
            
            url = "https://en.wikipedia.org"+link #combine domain url + page link
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to retrieve webpage: {response.status_code}")
                break
            
            raw_html = response.text
            soup = BeautifulSoup(raw_html, 'html.parser')
            fn = soup.title.string #name file names after titles of downloaded webpages
            fp = os.path.join(dir, fn +".html")
            print("Downloading webpage: " + fn)
            f = open(fp,"wb")
            f.write(soup.encode('utf8')) #convert unicode to utf-8 for writing purposes
            f.close()
            
            
        
else:
    print(f"Failed to retrieve webpage: {response.status_code}")
            
        

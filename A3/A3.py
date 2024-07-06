import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Retrieve the web page
url = "https://en.wikipedia.org/wiki/List_of_Canadian_provinces_and_territories_by_historical_population"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:  # status code of 200 indicates a successful request
    raw_html = response.text
    print("Webpage retrieved successfully")
    
    # Decode the raw HTML using BeautifulSoup
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Extract relevant tables
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    # Print number of tables
    print(f"Number of tables found: {len(tables)}")
    
    # Function to sanitize text
    def sanitize(text):
        return text.strip()
    
    # Initialize an empty dictionary to hold all data
    all_data = {}
    all_periods = []
    
    for table in tables: #Iterate through each table
        headers = [(th.get_text()).strip() for th in table.find_all('th')] #extract and sanitize headers
        all_periods.extend(headers[1:])  # Collect all period headers excluding the 'Name' header
        
        for row in table.find_all('tr')[1:]:  # skip header row and iterate through each row in the table
            cells = row.find_all(['td', 'th']) #extract all cells in the given row
            if len(cells) == len(headers): 
                name = sanitize(cells[0].get_text()) #get the name from the first cell
                if name not in all_data: #Initialize the name entry if the name doesn't already exist
                    all_data[name] = {header: "N/A" for header in all_periods}
                
                for i in range(1, len(headers)): #Loop through the remaining cells
                    period = headers[i] #get the period header
                    value = sanitize(cells[i].get_text())
                    all_data[name][period] = value #assign value to the corresponding time period.
    
    # Remove duplicates from all_periods while maintaining order
    seen = set() #Create a set to track seen periods
    ordered_periods = []
    
    for period in all_periods: #Iterate through each stored time period
        if period not in seen:
            ordered_periods.append(period)
            seen.add(period)
    
    # Convert the dictionary to a format suitable for pandas DataFrame
    formatted_data = {'Name': [], **{period: [] for period in ordered_periods}}
    
    for name, values in all_data.items(): # Iterate through each name and its associated values
        formatted_data['Name'].append(name) # add the name to the 'Name' list
        for period in ordered_periods: 
            formatted_data[period].append(values.get(period, "N/A")) # Add the value for each period, "N/A" if it is missing
    print(formatted_data)
    print("------------------------------------")
    
    # Convert the final dictionary to a pandas DataFrame
    df = pd.DataFrame(formatted_data)
    
    #print the dataframe
    df.head(60)
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

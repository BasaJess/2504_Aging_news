# SpringerNature Publication retrieval agent
'''Here's a Python script that fetches up to 500 documents related to "longevity" from the Springer Nature Metadata API and stores them locally. This script adheres to Springer Nature's API usage policies to ensure compliance and avoid potential blacklisting.

🔧 Prerequisites
API Key:
'''

# Imports
import os
import time
import requests
import json
#-----------------------------------------------
# Load credentials
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env', verbose=True)
#-----------------------------------------------
# Retrieve the Hugging Face token from environment variables
sn_api_key = os.getenv('SPRINGERNATURE_API_KEY')
#---------------------------------------------
# Last day the Publications were retrieved Date
def get_last_retrieval_date():
    # Open and read the JSON file
    with open('../data/SpringerNature_last_retrieval_date.json', 'r') as json_file:
        data = json.load(json_file)

    # Extract the date value
    date_string = data.get('date')

    print(f"Retrieved date: {date_string}")
    return date_string
#---------------------------------------------------------
# Update the date of Last time the publications were retrieved to todays date
from datetime import date
def update_last_retrieval_date():
    # Get today's date in ISO 8601 format (YYYY-MM-DD)
    today = date.today().isoformat()

    # Create a dictionary with the date
    data = {'date': today}

    # Write the dictionary to a JSON file
    with open('../data/SpringerNature_last_retrieval_date.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Today's date has been saved to 'SpringerNature_last_retrieval_date.json'")
#--------------------------------------------------------------
# Retrieve API key and set up constants
API_KEY = sn_api_key
QUERY = "journalid:43587 AND onlinedatefrom:" + get_last_retrieval_date()
MAX_RESULTS = 400
PAGE_SIZE = 10  # Maximum allowed by the API is 100
OUTPUT_DIR = '../data/springer_longevity_docs'
API_ENDPOINT = 'https://api.springernature.com/openaccess/json'
# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
#--------------------------------------------------------------
# Fetch the documents function
'''Query String Parameters
This section introduces key fields such as 'q' for the query, 's' for the starting result, and p for the number of results per page. The following query string parameters can be passed to the API to customize how the results are displayed:

|Parameter|Description|Required|Default Value|
|---|---|---|---|
|q|The query to be performed by the API. Supports various filters.|yes||	
|s|Return results starting at the number specified.|no|1|
|p|Number of results to return in the request. (See section Pagination and Limits for more details.)|no|10|
|api_key|The key identifying your application.|yes||
	
If the p parameter is not included, 10 results will be returned by default. If the s parameter is omitted, the results will start from the first entry. The q parameter offers flexible options, allowing you to build complex queries.'''

def fetch_documents():
    total_fetched = 0
    start = 0  # Springer API uses 1-based indexing

     #'q': f'{QUERY} sort:date',
    while total_fetched < MAX_RESULTS:
        params = {
        #'query': "Keyword:lifespan",
        'api_key': API_KEY,
        'q' : QUERY,
        's' : start
        }

        try:
            response = requests.get(API_ENDPOINT, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                print("No more records found.")
                break

            for record in records:
                if record:
                    doc_id = record.get('identifier', f'doc_{start}')
                    # Attempt to retrieve full-text URL
                    full_text_url = None
                    for link in record.get('url', []):
                        if link.get('format') == '':
                            full_text_url = link.get('value')
                            print("fulltexturl:" + full_text_url)
                            break

                    if full_text_url:
                        try:
                            full_text_response = requests.get(full_text_url, timeout=10)
                            full_text_response.raise_for_status()
                            full_text_content = full_text_response.text
                            full_text_filename = OUTPUT_DIR + "/" + f"{doc_id.replace(':', '_').replace('/', '_')}_fulltext.xml"
                            print("Full text filename: "+full_text_filename)
                            #full_text_filename = os.path.join(OUTPUT_DIR, f"{safe_doc_id}_fulltext.xml")
                            with open(full_text_filename, 'w', encoding='utf-8') as ft_file:
                                ft_file.write(full_text_content)
                        except requests.exceptions.RequestException as e:
                            print(f"Failed to retrieve full text for {doc_id}: {e}")        

            fetched_count = len(records)
            total_fetched += fetched_count
            print(f"Fetched {fetched_count} records. Total fetched: {total_fetched}")

            if fetched_count < PAGE_SIZE:
                # Fewer records than page size indicates no more data
                break

            start += PAGE_SIZE

            # Respectful delay between requests
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

#----------------------------------------------------------------
# Function to be used from other script
def fetch_papers_from_SpringerNature():
    print("Fetching papers from SpringerNature...")
    fetch_documents()
    update_last_retrieval_date()
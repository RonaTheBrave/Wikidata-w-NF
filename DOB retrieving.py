import pandas as pd
import requests
from datetime import datetime


# Function to get Wikipedia article creation date
def get_wikipedia_creation_date(page_url):
    if pd.isna(page_url):
        return None
    page_title = page_url.split('/')[-1]
    endpoint = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvdir=newer&titles={page_title}&format=json"

    response = requests.get(endpoint)
    data = response.json()
    page_id = next(iter(data['query']['pages']))

    if 'revisions' in data['query']['pages'][page_id]:
        creation_date = data['query']['pages'][page_id]['revisions'][0]['timestamp']
        creation_date = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%SZ')
        return creation_date
    else:
        return None


# Function to get Wikidata item creation date
def get_wikidata_creation_date(wikidata_url):
    if pd.isna(wikidata_url):
        return None
    entity_id = wikidata_url.split('/')[-1]
    endpoint = f"https://www.wikidata.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvdir=newer&titles=Item:{entity_id}&format=json"

    response = requests.get(endpoint)
    data = response.json()
    page_id = next(iter(data['query']['pages']))

    if 'revisions' in data['query']['pages'][page_id]:
        creation_date = data['query']['pages'][page_id]['revisions'][0]['timestamp']
        creation_date = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%SZ')
        return creation_date
    else:
        return None


# Load the Excel file
file_path = 'Opioid corpus Wikipedia + Wikidata links 01.07.2024.xlsx'
data = pd.read_excel(file_path)

# Add new columns for creation dates
data['Wikipedia Creation Date'] = data['page url'].apply(get_wikipedia_creation_date)
data['Wikidata Creation Date'] = data['wikidata_url'].apply(get_wikidata_creation_date)

# Save the updated dataframe to a new Excel file
output_file_path = 'Opioid_corpus_with_creation_dates.xlsx'
data.to_excel(output_file_path, index=False)

print(f"Updated file saved as {output_file_path}")

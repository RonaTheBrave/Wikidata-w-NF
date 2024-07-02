import requests
import pandas as pd

# Load your Excel file
file_path = 'opioid_26092023corpus.xlsx'
data = pd.read_excel(file_path)

def get_wikidata_url(wikipedia_url):
    # Extract the article title from the URL
    title = wikipedia_url.split('/wiki/')[-1]
    # Query the Wikidata API
    response = requests.get(f'https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&titles={title}&format=json')
    data = response.json()
    entities = data.get('entities')
    if entities:
        entity_id = list(entities.keys())[0]
        if entity_id != '-1':
            return f'https://www.wikidata.org/wiki/{entity_id}'
    return ''

# Apply the function to the DataFrame
data['wikidata_url'] = data['page url'].apply(get_wikidata_url)

# Save the DataFrame to a new Excel file
output_path = 'updated_opioid_26092023corpus.xlsx'
data.to_excel(output_path, index=False)
print(f"Updated file saved to {output_path}")

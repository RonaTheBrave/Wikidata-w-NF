import pandas as pd
import requests

# Load the updated Excel file with Wikidata URLs
file_path = 'updated_opioid_26092023corpus.xlsx'
data = pd.read_excel(file_path)

# Check the columns in the DataFrame
print(data.columns)

# Use the correct column name for Wikidata URLs
wikidata_url_column = 'wikidata_url'  # Update this if the column name is different


# Function to fetch Wikidata properties
def fetch_wikidata_properties(wikidata_url):
    if pd.isna(wikidata_url):
        return {}, {}, {}

    entity_id = wikidata_url.split('/wiki/')[-1]
    url = f'https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json'
    response = requests.get(url)
    data = response.json()
    claims = data['entities'][entity_id]['claims']

    instance_of = claims.get('P31', [{}])[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id', '')
    part_of = claims.get('P361', [{}])[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id', '')
    subclass_of = claims.get('P279', [{}])[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id', '')

    return instance_of, part_of, subclass_of


# Fetch properties for each Wikidata item and add them to the DataFrame
data[['instance_of', 'part_of', 'subclass_of']] = data[wikidata_url_column].apply(
    lambda url: pd.Series(fetch_wikidata_properties(url)))

# Save the updated DataFrame to a new Excel file
output_file_path = 'updated_opioid_26092023corpus_with_properties.xlsx'
data.to_excel(output_file_path, index=False)

print(f"Updated DataFrame saved to {output_file_path}")

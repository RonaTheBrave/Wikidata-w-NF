import pandas as pd
import requests
import re
import time
from tqdm import tqdm

# Load the Excel file
file_path = 'updated_opioid_26092023corpus.xlsx'  # Change this to your file path
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Extract Wikidata IDs from the 'wikidata_url' column
df['wikidata_url'] = df['wikidata_url'].astype(str)
df['wikidata_id'] = df['wikidata_url'].apply(lambda x: re.search(r'Q\d+', x).group() if re.search(r'Q\d+', x) else None)

# Function to get the "part of" hierarchy for a given Wikidata item ID (iterative approach)
def get_part_of_hierarchy(item_id):
    hierarchy = []
    stack = [item_id]  # Using a stack for iterative depth-first search
    while stack:
        current_id = stack.pop()
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={current_id}&format=json&props=claims"
        response = requests.get(url).json()
        if 'entities' in response and current_id in response['entities']:
            claims = response['entities'][current_id].get('claims', {})
            if 'P361' in claims:  # P361 is "part of"
                part_of_ids = [claim['mainsnak'].get('datavalue', {}).get('value', {}).get('id') for claim in claims['P361'] if claim['mainsnak'].get('datavalue')]
                for part_of_id in part_of_ids:
                    if part_of_id not in hierarchy:
                        hierarchy.append(part_of_id)
                        stack.append(part_of_id)
    return hierarchy

# Function to get parent classes (using an iterative approach)
def get_parent_classes(item_id):
    parent_classes = []
    stack = [item_id]  # Using a stack for iterative depth-first search
    while stack:
        current_id = stack.pop()
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={current_id}&format=json&props=claims"
        response = requests.get(url).json()
        if 'entities' in response and current_id in response['entities']:
            claims = response['entities'][current_id].get('claims', {})
            if 'P279' in claims:  # P279 is "subclass of"
                for claim in claims['P279']:
                    if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                        parent_id = claim['mainsnak']['datavalue']['value']['id']
                        if parent_id not in parent_classes:
                            parent_classes.append(parent_id)
                            stack.append(parent_id)
    return parent_classes

# Get the "part of" hierarchy for each Wikidata item with progress bar and time estimation
start_time = time.time()
results = []

for i, wikidata_id in enumerate(tqdm(df['wikidata_id'], desc='Processing', unit='item')):
    if wikidata_id:
        hierarchy = get_part_of_hierarchy(wikidata_id)
    else:
        hierarchy = []
    results.append(hierarchy)

    # Calculate and display elapsed and estimated remaining time
    elapsed_time = time.time() - start_time
    avg_time_per_item = elapsed_time / (i + 1)
    remaining_items = len(df) - (i + 1)
    estimated_remaining_time = remaining_items * avg_time_per_item
    if (i + 1) % 10 == 0:  # Print progress every 10 items
        print(f"Processed {i + 1}/{len(df)} items. Estimated remaining time: {estimated_remaining_time:.2f} seconds")

# Add the results to the DataFrame
df['part_of_hierarchy'] = results

# Save the result to a new Excel file
output_file_path = 'all_part_of_hierarchy.xlsx'
df.to_excel(output_file_path, index=False)
print(f'Results saved to {output_file_path}')

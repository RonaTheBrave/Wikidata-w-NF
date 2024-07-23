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

# Function to get the "subclass of" hierarchy for a given Wikidata item ID (iterative approach)
def get_subclass_of_hierarchy(item_id):
    hierarchy = []
    stack = [item_id]  # Using a stack for iterative depth-first search
    while stack:
        current_id = stack.pop()
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={current_id}&format=json&props=claims"
        response = requests.get(url).json()
        if 'entities' in response and current_id in response['entities']:
            claims = response['entities'][current_id].get('claims', {})
            if 'P279' in claims:  # P279 is "subclass of"
                subclass_of_ids = [claim['mainsnak'].get('datavalue', {}).get('value', {}).get('id') for claim in claims['P279'] if claim['mainsnak'].get('datavalue')]
                for subclass_of_id in subclass_of_ids:
                    if subclass_of_id not in hierarchy:
                        hierarchy.append(subclass_of_id)
                        stack.append(subclass_of_id)
    return hierarchy

# Get the "subclass of" hierarchy for each Wikidata item with progress bar and time estimation
start_time = time.time()
results = []

for i, wikidata_id in enumerate(tqdm(df['wikidata_id'], desc='Processing', unit='item')):
    if wikidata_id:
        hierarchy = get_subclass_of_hierarchy(wikidata_id)
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
df['subclass_of_hierarchy'] = results

# Save the result to a new Excel file
output_file_path = 'all_subclass_of_hierarchy.xlsx'
df.to_excel(output_file_path, index=False)
print(f'Results saved to {output_file_path}')

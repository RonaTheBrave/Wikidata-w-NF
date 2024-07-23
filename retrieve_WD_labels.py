import pandas as pd
import requests

# Function to get label for a Wikidata ID
def get_wikidata_label(wikidata_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data['entities'][wikidata_id]['labels']['en']['value']
        except KeyError:
            return None
    else:
        return None

# Load the Excel file
file_path = 'all_part_of_hierarchy02.07.24.xlsx'
df = pd.read_excel(file_path)

# Define column names to process
columns_to_process = df.columns[4:241]  # Columns E to HN

# Extract unique Wikidata IDs from the selected columns
unique_wikidata_ids = pd.unique(df[columns_to_process].values.ravel('K')).tolist()
unique_wikidata_ids = [x for x in unique_wikidata_ids if pd.notna(x)]

# Get labels for all unique Wikidata IDs
wikidata_labels = {wid: get_wikidata_label(wid) for wid in unique_wikidata_ids}

# Replace Wikidata IDs with their labels in the selected columns
for column in columns_to_process:
    df[column] = df[column].apply(lambda wid: wikidata_labels.get(wid, wid))

# Save the updated dataframe to a new Excel file
output_file_path = 'labeled_all_part_of_hierarchy.xlsx'
df.to_excel(output_file_path, index=False)

print("Updated Excel file saved to:", output_file_path)

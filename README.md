# Wikidata (WD) statements collection for WP articles

HUJI DHHU project using Wikidata to qualify Wikipedia articles

We start with a corpus file (a list of WP articles by name)

1. ("wikidata adding.py")
First, we add WD IDs for each article 

2. ("DOB retrieving.py")
We then retrieve the DOBs for the WP articles, and the WD items

3. ("adding_wikidata_properties.py", "extracting all subclass of.py", "extracting instance of all way up.py", "extracting part of all the way up.py")
Then we scrape WD to find their statements and create
a) a df with the first level of each type of statement (instance of, subclass of, part of)
b) seperate files with dfs for each type, going into all levels
* total of 4 files
* we seperated this because often the levels can go very deep and it disrupts the presentation

4. ("retrieve_WD_labels.py")
Last we retrive the lables for manual inspection and visualizations




# Given name of directory + name of file to search for + file extension
# Recursively search directory for file and copy to new directory

from fuzzywuzzy import fuzz
import os

def search_files(directory, query, threshold=80):
    matches = []
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Get the file base name without extension
            base_name = os.path.splitext(filename)[0]
            ratio = fuzz.partial_ratio(query.lower(), base_name.lower())
            if ratio > threshold:
                matches.append(os.path.join(root, filename))
    
    return matches

# Example
directory_path = r''
query = 'Age of Empires'
matched_files = search_files(directory_path, query)
for file in matched_files:
    print(file)

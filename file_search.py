import os
import shutil
import logging
import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz

# Configure logging
logging.basicConfig(level=logging.INFO)

def search_files(directory, query, file_extension="", threshold=80):
    """Search for files based on a fuzzy match query."""
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # If a file extension is specified, filter files based on it
            if file_extension and not filename.lower().endswith(file_extension.lower()):
                continue

            base_name = os.path.splitext(filename)[0]
            ratio = fuzz.partial_ratio(query.lower(), base_name.lower())
            if ratio > threshold:
                matches.append(os.path.join(root, filename))
    return matches

def copy_file_avoiding_overwrite(source_path, destination_path):
    base, extension = os.path.splitext(destination_path)
    counter = 1
    while os.path.exists(destination_path):
        destination_path = f"{base}_{counter}{extension}"
        counter += 1
    try:
        shutil.copy2(source_path, destination_path)
        return True
    except Exception as e:
        logging.error(f"Error copying file: {e}")
        return False
    
def search_file_contents(directory, query, threshold=80):
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if not filename.lower().endswith(".dat"):
                continue
            filepath = os.path.join(root, filename)
            try:
                tree = ET.parse(filepath)
                # Search for 'machine' elements and get the 'name' attribute
                for machine in tree.findall(".//machine"):
                    machine_name = machine.get("name", "")
                    ratio = fuzz.partial_ratio(query.lower(), machine_name.lower())
                    if ratio > threshold:
                        matches.append(filepath)
                        logging.info(f"Match found in {filepath}: {machine_name}")
                        break
            except ET.ParseError:
                logging.warning(f"Failed to parse XML in {filepath}. Skipping.")
    return matches

def read_file_lines_to_list(filename):
    """Read the contents of a file and return each line as a list."""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def extract_machine_names_from_dat(filename):
    """Extract the name attributes from machine elements in a .dat file."""
    machine_names = []
    
    try:
        tree = ET.parse(filename)
        
        # Search for 'machine' elements and get the 'name' attribute
        for machine in tree.findall(".//machine"):
            name = machine.get("name")
            if name:  # Only add to the list if the name attribute exists
                machine_names.append(name)

    except ET.ParseError:
        logging.warning(f"Failed to parse XML in {filename}. Skipping.")
        
    return machine_names

def main():
    search_type = input("Choose search type: \n1. By file name \n2. By .dat file contents\nEnter choice (1 or 2): ")
    if search_type not in ['1', '2']:
        logging.error("Invalid choice. Exiting.")
        return

    search_file = input("Enter your search file path: ")
    search_dir = input("Enter the directory to search in: ")
    copy_dir = input("Enter the directory to copy files to: ")

    if search_type == '1':
        file_extension = input("Enter a file extension (e.g. '.txt') or leave blank for all extensions: ")
        search_queries = read_file_lines_to_list(search_file)
    else:  # If option 2, the file extension is implicitly .dat
        file_extension = '.dat'
        search_queries = extract_machine_names_from_dat(search_file)
    
    # Allow user to specify the threshold
    try:
        threshold = int(input("Enter a threshold (0-100, default is 80, lower is more lenient): "))
        if threshold < 0 or threshold > 100:
            logging.warning("Invalid threshold value. Using the default of 80.")
            threshold = 80
    except ValueError:
        logging.warning("Invalid threshold input. Using the default of 80.")
        threshold = 80

    # Ensure the copy directory exists
    if not os.path.exists(copy_dir):
        os.makedirs(copy_dir)

    for query in search_queries:
        if search_type == '1':
            matched_files = search_files(search_dir, query, file_extension, threshold)
        else:  # For .dat files and their XML content
            matched_files = search_file_contents(search_dir, query, threshold)
        
        if not matched_files:
            logging.info(f"No files matched the search query: {query}")
            continue

        # Copy files to the destination
        for file in matched_files:
            logging.info(f"Found file: {file} for query: {query}")
            dest_path = os.path.join(copy_dir, os.path.basename(file))
            if copy_file_avoiding_overwrite(file, dest_path):
                logging.info(f"Copied file to: {dest_path}")
            else:
                logging.error(f"Failed to copy: {file}")

    logging.info("File copying process completed.")

if __name__ == "__main__":
    main()

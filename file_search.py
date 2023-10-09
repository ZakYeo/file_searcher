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

def copy_file(source_path, destination_path):
    """Copy a file to a destination."""
    try:
        shutil.copy2(source_path, destination_path)
        return True
    except Exception as e:
        logging.error(f"Error copying file: {e}")
        return False

def search_file_contents(directory, query, threshold=80):
    """Search for .dat files based on a fuzzy match to their machine name contents."""
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Only consider .dat files
            if not filename.lower().endswith(".dat"):
                continue

            filepath = os.path.join(root, filename)
            try:
                tree = ET.parse(filepath)
                root_element = tree.getroot()

                for machine in root_element.findall('machine'):
                    machine_name = machine.get('name', '')
                    ratio = fuzz.partial_ratio(query.lower(), machine_name.lower())
                    if ratio > threshold:
                        matches.append(filepath)
                        break  # If one match is found in the file, no need to continue searching in it

            except Exception as e:
                logging.error(f"Error reading or parsing file {filepath}: {e}")
    return matches

def main():
    search_type = input("Choose search type: \n1. By file name \n2. By .dat file contents\nEnter choice (1 or 2): ")
    if search_type not in ['1', '2']:
        logging.error("Invalid choice. Exiting.")
        return

    query = input("Enter your search query: ")
    search_dir = input("Enter the directory to search in: ")
    copy_dir = input("Enter the directory to copy files to: ")

    if search_type == '1':
        file_extension = input("Enter a file extension (e.g. '.txt') or leave blank for all extensions: ")
    else:  # If option 2, the file extension is implicitly .dat
        file_extension = '.dat'
    # Allow user to specify the threshold
    try:
        threshold = int(input("Enter a threshold (0-100, default is 80, lower is more lenient): "))
        if threshold < 0 or threshold > 100:
            logging.warning("Invalid threshold value. Using the default of 80.")
            threshold = 80
    except ValueError:
        logging.warning("Invalid threshold input. Using the default of 80.")
        threshold = 80

    if search_type == '1':
        matched_files = search_files(search_dir, query, file_extension, threshold)
    else:  # For .dat files and their XML content
        matched_files = search_file_contents(search_dir, query, threshold)
    
    # Ensure the copy directory exists
    if not os.path.exists(copy_dir):
        os.makedirs(copy_dir)

    if not matched_files:
        logging.info("No files matched the search query.")
        return

    # Copy files to the destination
    for file in matched_files:
        logging.info(f"Found file: {file}")
        dest_path = os.path.join(copy_dir, os.path.basename(file))
        if copy_file(file, dest_path):
            logging.info(f"Copied file to: {dest_path}")
        else:
            logging.error(f"Failed to copy: {file}")

    logging.info("File copying process completed.")

if __name__ == "__main__":
    main()
import os
import shutil
import logging
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

def main():
    query = input("Enter your search query: ")
    search_dir = input("Enter the directory to search in: ")
    copy_dir = input("Enter the directory to copy files to: ")
    file_extension = input("Enter a file extension (e.g. '.txt') or leave blank for all extensions: ")

    # Ensure the copy directory exists
    if not os.path.exists(copy_dir):
        os.makedirs(copy_dir)

    # Search for files
    matched_files = search_files(search_dir, query, file_extension)
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

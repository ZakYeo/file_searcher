# Fuzzy File Search and Copy Tool

This Python script offers the ability to search for files in a specified directory and then copy them to another directory. The search is performed in two possible modes:

1. Fuzzy search by file name
2. Fuzzy search by `.dat` file contents (specifically looking for machine name attributes in XML format).

## Usage:

1. Run the script.
2. Choose your search type:
   - `1. By file name`: Allows you to specify any file extension, or search across all extensions.
   - `2. By .dat file contents`: Will only search within `.dat` files for matching XML content.
3. Enter your search query.
4. Specify the directory to search in.
5. Specify the directory to which matching files should be copied.
6. For search type 1, specify the desired file extension or leave blank to search all files.
7. Input a threshold for the search. Default is 80 (out of 100), where a lower value is more lenient. This determines the matching accuracy.

## Notes:

- The tool uses fuzzy matching, meaning it doesn't require an exact match to identify a file.
- For the `.dat` file content search, the script looks for machine name attributes in XML tags that resemble: `<machine name="...">`.

## Dependencies:

- `fuzzywuzzy`: For performing the fuzzy string matching.
  - Install with `pip install fuzzywuzzy`
- `python-Levenshtein`: (Optional) Speeds up the processing considerably for `fuzzywuzzy`.
  - Install with `pip install python-Levenshtein`
- `xml.etree.ElementTree`: For XML parsing in .dat files.
  - Should come pre-installed

Ensure you have the required modules installed via pip before using the script.

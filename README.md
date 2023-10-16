# README.md for `file_searcher`

## Introduction

`file_searcher` is a simple tool for searching files based on either their names or content of `.dat` files that have XML-like structures. The tool also has a copying feature which ensures that it won't overwrite existing files in the destination directory by appending a counter to the file name if a conflict occurs.

## Dependencies

To use `file_searcher`, you'll need to install the following Python modules:

- `fuzzywuzzy`

You can install them using `pip`:

`pip install fuzzywuzzy`

## Running Unit Tests

To run the unit tests, navigate to the project's root directory and execute the test script:

`python test_file_search.py`

Ensure that both the main script and the test script are in the same directory before running tests.

## Usage Instructions

1. **Search Type Selection**: The tool provides two search options:
   - Search by file name.
   - Search by the content of `.dat` files.

2. **Search File Path**: Input the path of your search file. This file should contain one search query per line. If you're searching by file name, these are string queries (e.g., "sample"). If you're searching by `.dat` file contents, this should be a `.dat` file with XML structures that contain machine elements with name attributes.

3. **Search Directory**: This is the directory where the tool will search for matches.

4. **Copy Directory**: After finding a match, the tool will copy the file to this directory. If the file already exists, the tool will append a counter to its name to avoid overwriting.

5. **File Extension (Optional)**: If you're searching by file name, you have the option to specify a file extension to further narrow down your search. If left blank, all extensions will be considered.

6. **Threshold**: This value (between 0-100) determines how lenient the fuzzy search should be. A lower value is more lenient, while a higher value is more strict. By default, the threshold is set to 80.

To start the program, navigate to the project's root directory and run:

```python file_searcher.py```

Then, follow the on-screen prompts to execute your search.

That's it! Feel free to explore the codebase and extend its functionalities as needed.

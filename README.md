# Fuzzy File Search and Copy Utility

This utility allows users to perform a fuzzy search for files within a specified directory based on a query. The found files can then be copied to a desired destination directory. An option is provided to filter the search based on a specific file extension.

## Usage

1. Run the utility from the command line.
2. Provide a search query when prompted.
3. Specify the directory where you want to search for files.
4. Provide the directory where the matched files should be copied to.
5. Optionally, specify a file extension to filter the search (e.g. `.txt`). Leave it blank if you wish to consider all file extensions.
6. Specify a threshold value (0-100). Default is 80. A lower threshold means a more lenient search, while a higher threshold makes the search stricter.

Example:

```shell
Enter your search query: Age of Empires
Enter the directory to search in: /path/to/search/directory
Enter the directory to copy files to: /path/to/destination/directory
Enter a file extension (e.g. '.txt') or leave blank for all extensions:
Enter a threshold (0-100, default is 80, lower is more lenient): 75
```

## Dependencies

- `fuzzywuzzy`: For performing the fuzzy string matching.
  - Install with `pip install fuzzywuzzy`
- `python-Levenshtein`: (Optional) Speeds up the processing considerably for `fuzzywuzzy`.
  - Install with `pip install python-Levenshtein`

## Logging

The utility uses logging to provide feedback about its actions to the console. You will be informed about the files that were found, those that are being copied, and any errors that might occur during the process.

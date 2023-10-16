import unittest
from unittest.mock import patch, mock_open
import os
import file_search

class TestSearcher(unittest.TestCase):

    def setUp(self):
        # Setting up necessary test data or configurations
        pass

    def test_search_files(self):
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                ('/test_dir', [], ['file1.txt', 'query_file2.txt', 'anotherfile.dat'])
            ]
            result = file_search.search_files('/test_dir', 'query_file')
            self.assertEqual(sorted(result), sorted(['/test_dir/file1.txt', '/test_dir/query_file2.txt']))


    def test_copy_file_avoiding_overwrite(self):
        # Mock the os.path.exists and shutil.copy2 methods
        with patch('os.path.exists') as mock_exists, patch('shutil.copy2') as mock_copy:
            mock_exists.return_value = False
            success = file_search.copy_file_avoiding_overwrite('/source/file.txt', '/dest/file.txt')
            self.assertTrue(success)
            mock_copy.assert_called_once_with('/source/file.txt', '/dest/file.txt')

    def test_extract_machine_names_from_dat(self):
        mock_data = """<?xml version="1.0"?>
        <root>
            <machine name="Machine1"></machine>
            <machine name="Machine2"></machine>
        </root>
        """
        with patch('builtins.open', mock_open(read_data=mock_data)):
            machine_names = file_search.extract_machine_names_from_dat('sample.dat')
            self.assertEqual(machine_names, ['Machine1', 'Machine2'])


    def test_read_file_lines_to_list(self):
        # Mock the file reading with sample data
        mock_data = "line1\nline2\nline3"
        with patch('builtins.open', mock_open(read_data=mock_data)):
            lines = file_search.read_file_lines_to_list('sample.txt')
            self.assertEqual(lines, ['line1', 'line2', 'line3'])

    # You can add more test methods for other functions and cases...

if __name__ == '__main__':
    unittest.main()

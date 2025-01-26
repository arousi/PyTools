import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

class TestPDF2TextScript(unittest.TestCase):

    @patch('builtins.input', side_effect=['test.pdf'])
    @patch('subprocess.run')
    def test_cli_mode(self, mock_subprocess_run, mock_input):
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Please place the PDF file to be converted in the script's directory.\n")
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'PDF2Text', 'PDF2Text.py'))
        result = subprocess.run([sys.executable, script_path, 'cli'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Please place the PDF file to be converted in the script's directory.", result.stdout)

    @patch('tkinter.filedialog.askopenfilename', return_value='test.pdf')
    @patch('subprocess.run')
    def test_gui_mode(self, mock_subprocess_run, mock_askopenfilename):
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Extraction complete. Text saved to 'exports/test.txt'\n")
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'PDF2Text', 'PDF2Text.py'))
        result = subprocess.run([sys.executable, script_path, 'gui'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Extraction complete. Text saved to 'exports/test.txt'", result.stdout)

if __name__ == '__main__':
    unittest.main()
import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

class TestMainScript(unittest.TestCase):

    @patch('builtins.input', side_effect=['cli', '2', 'test.pdf'])
    @patch('subprocess.run')
    def test_cli_mode(self, mock_subprocess_run, mock_input):
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Please place the file to be converted in the script's directory.\n")
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Please place the file to be converted in the script's directory.", result.stdout)

    @patch('tkinter.filedialog.askopenfilename', return_value='test.pdf')
    @patch('subprocess.run')
    def test_gui_mode(self, mock_subprocess_run, mock_askopenfilename):
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Select a Tool to Run\n")
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
        with patch('builtins.input', return_value='gui'):
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Select a Tool to Run", result.stdout)

if __name__ == '__main__':
    unittest.main()
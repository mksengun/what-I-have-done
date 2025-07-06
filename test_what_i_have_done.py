import unittest
from unittest.mock import patch, MagicMock
import os
import argparse
import requests
import subprocess

# Import the functions from the main script
# Assuming what-I-have-done.py is in the same directory
import what_I_have_done

class TestWhatIHaveDone(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args(self, mock_parse_args):
        # Test with API key provided
        mock_parse_args.return_value = argparse.Namespace(
            api_key='test_key', since='1.month', format='terminal', 
            template='developer', exclude_merges=False
        )
        args = what_I_have_done.parse_args()
        self.assertEqual(args.api_key, 'test_key')
        self.assertEqual(args.since, '1.month')
        self.assertEqual(args.format, 'terminal')
        self.assertEqual(args.template, 'developer')
        self.assertEqual(args.exclude_merges, False)

        # Test without API key
        mock_parse_args.return_value = argparse.Namespace(
            api_key=None, since='1.month', format='terminal', 
            template='developer', exclude_merges=False
        )
        args = what_I_have_done.parse_args()
        self.assertIsNone(args.api_key)
        self.assertEqual(args.since, '1.month')

    @patch('subprocess.run')
    def test_get_git_logs_success(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(
            stdout="log1\nlog2",
            stderr="",
            returncode=0
        )
        logs = what_I_have_done.get_git_logs("1.month", False)
        self.assertEqual(logs, "log1\nlog2")
        mock_subprocess_run.assert_called_once()

    @patch('subprocess.run')
    def test_get_git_logs_failure(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(
            stdout="",
            stderr="git error",
            returncode=1
        )
        with self.assertRaisesRegex(RuntimeError, "Git command failed: git error"):
            what_I_have_done.get_git_logs("1.month", False)
        mock_subprocess_run.assert_called_once()

    @patch('requests.post')
    def test_get_report_from_openai_success(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test Report'}}]
        }
        mock_requests_post.return_value = mock_response

        report = what_I_have_done.get_report_from_openai("git logs", "test_api_key", "developer", "terminal")
        self.assertEqual(report, "Test Report")
        mock_requests_post.assert_called_once()

    @patch('requests.post')
    def test_get_report_from_openai_failure(self, mock_requests_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_requests_post.return_value = mock_response

        with self.assertRaisesRegex(RuntimeError, "OpenAI API error: 400 Bad Request"):
            what_I_have_done.get_report_from_openai("git logs", "test_api_key", "developer", "terminal")
        mock_requests_post.assert_called_once()

    @patch('what_I_have_done.get_git_logs')
    @patch('what_I_have_done.get_report_from_openai')
    @patch('what_I_have_done.parse_args')
    @patch('os.getenv', return_value='env_api_key')
    @patch('builtins.print')
    def test_main_success_with_env_key(self, mock_print, mock_getenv, mock_parse_args, mock_get_report, mock_get_logs):
        mock_parse_args.return_value = argparse.Namespace(
            api_key=None, since='1.month', format='terminal', 
            template='developer', exclude_merges=False
        )
        mock_get_logs.return_value = "mock git logs"
        mock_get_report.return_value = "mock report"

        what_I_have_done.main()

        mock_getenv.assert_called_once_with('OPENAI_API_KEY')
        mock_parse_args.assert_called_once()
        mock_get_logs.assert_called_once_with('1.month', False)
        mock_get_report.assert_called_once()
        mock_print.assert_any_call('🔍 Fetching Git logs...')
        mock_print.assert_any_call('📡 Sending logs to OpenAI...')
        mock_print.assert_any_call("mock report")

    @patch('what_I_have_done.get_git_logs')
    @patch('what_I_have_done.get_report_from_openai')
    @patch('what_I_have_done.parse_args')
    @patch('os.getenv', return_value=None)
    @patch('builtins.print')
    def test_main_success_with_arg_key(self, mock_print, mock_getenv, mock_parse_args, mock_get_report, mock_get_logs):
        mock_parse_args.return_value = argparse.Namespace(
            api_key='arg_api_key', since='1.month', format='terminal', 
            template='developer', exclude_merges=False
        )
        mock_get_logs.return_value = "mock git logs"
        mock_get_report.return_value = "mock report"

        what_I_have_done.main()

        mock_getenv.assert_not_called()
        mock_parse_args.assert_called_once()
        mock_get_logs.assert_called_once_with('1.month', False)
        mock_get_report.assert_called_once()
        mock_print.assert_any_call('🔍 Fetching Git logs...')
        mock_print.assert_any_call('📡 Sending logs to OpenAI...')
        mock_print.assert_any_call("mock report")

    @patch('what_I_have_done.parse_args')
    @patch('os.getenv', return_value=None)
    def test_main_no_api_key(self, mock_getenv, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            api_key=None, since='1.month', format='terminal', 
            template='developer', exclude_merges=False
        )
        with self.assertRaisesRegex(RuntimeError, "OpenAI API key must be provided"):
            what_I_have_done.main()
        mock_getenv.assert_called_once_with('OPENAI_API_KEY')
        mock_parse_args.assert_called_once()

    def test_time_presets(self):
        """Test time period presets"""
        # Test that presets are properly converted
        with patch('subprocess.run') as mock_subprocess_run:
            mock_subprocess_run.return_value = MagicMock(
                stdout="test logs", stderr="", returncode=0
            )
            
            # Test preset conversion
            what_I_have_done.get_git_logs("yesterday", False)
            call_args = mock_subprocess_run.call_args[0][0]
            self.assertIn('--since="1.day"', call_args)
            
            what_I_have_done.get_git_logs("this-week", False)
            call_args = mock_subprocess_run.call_args[0][0]
            self.assertIn('--since="1.week"', call_args)

    def test_exclude_merges_option(self):
        """Test exclude merges functionality"""
        with patch('subprocess.run') as mock_subprocess_run:
            mock_subprocess_run.return_value = MagicMock(
                stdout="test logs", stderr="", returncode=0
            )
            
            # Test with exclude_merges=True
            what_I_have_done.get_git_logs("1.month", True)
            call_args = mock_subprocess_run.call_args[0][0]
            self.assertIn('--no-merges', call_args)
            
            # Test with exclude_merges=False
            what_I_have_done.get_git_logs("1.month", False)
            call_args = mock_subprocess_run.call_args[0][0]
            self.assertNotIn('--no-merges', call_args)

    def test_generate_prompt_templates(self):
        """Test different prompt templates"""
        test_logs = "2024-01-01 10:00:00|Test commit|abc123"
        
        # Test developer template
        prompt = what_I_have_done.generate_prompt(test_logs, 'developer', 'terminal')
        self.assertIn('technical aspects', prompt)
        self.assertIn('ASCII box-drawing characters', prompt)
        
        # Test manager template  
        prompt = what_I_have_done.generate_prompt(test_logs, 'manager', 'terminal')
        self.assertIn('management-focused', prompt)
        self.assertIn('deliverables', prompt)
        
        # Test markdown format
        prompt = what_I_have_done.generate_prompt(test_logs, 'developer', 'markdown')
        self.assertIn('Markdown', prompt)
        self.assertIn('headers', prompt)
        
        # Test JSON format
        prompt = what_I_have_done.generate_prompt(test_logs, 'developer', 'json')
        self.assertIn('JSON', prompt)
        self.assertIn('structured data', prompt)

    def test_analyze_git_logs(self):
        """Test git log analysis"""
        # Test with valid logs
        test_logs = "2024-01-01 10:00:00|First commit|abc123\n2024-01-02 15:30:00|Second commit|def456"
        analysis = what_I_have_done.analyze_git_logs(test_logs)
        
        self.assertEqual(analysis['total_commits'], 2)
        self.assertEqual(analysis['date_range']['start'], '2024-01-02 15:30:00')
        self.assertEqual(analysis['date_range']['end'], '2024-01-01 10:00:00')
        self.assertEqual(len(analysis['commit_messages']), 2)
        
        # Test with empty logs
        analysis = what_I_have_done.analyze_git_logs("")
        self.assertEqual(analysis, {})

if __name__ == '__main__':
    unittest.main()

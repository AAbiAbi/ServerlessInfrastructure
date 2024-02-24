import json
import unittest
from unittest.mock import MagicMock, patch
from slack_request.handler import handle as handle_request
from slack_interactive.handler import handle as handle_interactive

class IntegrationTest(unittest.TestCase):
    @patch('slack_request.handler.requests.post')
    def test_slack_request_to_slack_interactive_integration(self, mock_post):
        # Configure the mock to return a specific response when called
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.text = json.dumps({"response": ["My name is ChatBot."]})
        # Test "name" request
        user_input_name = "What is your name?"
        
        response_name = handle_request(user_input_name)
        self.assertIn("My name is ChatBot.", response_name)

        # Prepare slack-interactive to handle "name" request type
        request_output_name = json.dumps({
            "request_type": "name",
            "original_request": user_input_name
        })
        interactive_response_name = handle_interactive(request_output_name)
        self.assertIn("My name is ChatBot.", interactive_response_name)

        # Mock subprocess for "figlet" request
        with patch('slack_interactive.handler.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(stdout="Figlet Text")
            request_output_figlet = json.dumps({
                "request_type": "figlet",
                "original_request": "Generate a figlet for Hello World"
            })
            interactive_response_figlet = handle_interactive(request_output_figlet)
            
            self.assertIn("Figlet Text", interactive_response_figlet)

if __name__ == "__main__":
    unittest.main()
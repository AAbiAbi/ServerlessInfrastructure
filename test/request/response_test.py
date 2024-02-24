import json
import unittest


# Adjust the import based on your actual file structure
from unittest.mock import MagicMock, patch
# Import the handler function from wherever your OpenFaaS function is defined
from slack_request.handler import handle

class TestChatbotFunction(unittest.TestCase):
    
    @patch('slack_request.handler.requests.post')  # Add this line to mock requests.post
    def test_name_response(self, mock_post):
        
        # Mock the response from the slack-interactive function
        mock_response = MagicMock()
        mock_response.text = "My name is ChatBot"
        mock_post.return_value = mock_response

         # Now call the handle function which will use the mocked requests.post
        response = handle("What is your name")
        self.assertIn("My name is ChatBot", response)

        # If you want to test a different name response, set up a new mock response
        mock_response.text = "I'm called ChatBot"
        mock_post.return_value = mock_response
        response = handle("name?")
        self.assertIn("I'm called ChatBot", response)

    @patch('slack_request.handler.requests.post')  # Add this line to mock requests.post
    def test_time_response(self, mock_post):
        # Mock the response from the slack-interactive function
        mock_response = MagicMock()
        mock_response.text = json.dumps({"response": "The current time is 12:00 PM."})
        mock_post.return_value = mock_response

        # Invoke the handler with a time-related question
        response = handle("what is the current time?")
        self.assertIn("The current time is", response)

    @patch('slack_request.handler.requests.post')  # This line is already correct
    def test_figlet_generation(self, mock_post):
        # Mock the response from the figlet invocation
        mock_response = MagicMock()
        mock_response.text = "Figlet Text"
        mock_post.return_value = mock_response

        response = handle("Generate a figlet for Hello World")
        self.assertEqual("Figlet Text", response)


if __name__ == '__main__':
    unittest.main()


import datetime
import json
import unittest
from unittest.mock import MagicMock, patch, Mock
from slack_interactive.handler import handle  # Adjust the import based on your actual file structure

class TestInteractiveHandle(unittest.TestCase):

    @patch('datetime.datetime')
    def test_handle_time(self, mock_datetime):
        # Create a mock datetime object
        mock_now = Mock()
        
        # Setup the mock to return specific strings for strftime
        def mock_strftime(fmt):
            if fmt == '%H:%M:%S':
                return "12:00:00"
            elif fmt == '%Y-%m-%d %H:%M:%S':
                return "2021-01-01 12:00:00"
            elif fmt == '%Y-%m-%d':
                return "2021-01-01"
            return ""
        
        mock_now.strftime.side_effect = mock_strftime        
        # Set the return value of datetime.datetime.now() to the mock object
        mock_datetime.now.return_value = mock_now
        
        # Construct a request payload
        request_payload = json.dumps({
            "request_type": "time",
            "original_request": "what is the current time?"
        })
        

        # Call the handle function
        response = handle(request_payload)
        response_data = json.loads(response)
        response_texts = response_data.get("response", [])

        self.assertIn("Current time is 12:00:00.", response)
        self.assertIn("It's now 2021-01-01 12:00:00.", response)
        self.assertIn("The date today is 2021-01-01.", response)

    @patch('slack_interactive.handler.requests.post')
    def test_handle_figlet(self, mock_requests_post):
        # Setup the mock to return a successful requests.post result
        mock_response = MagicMock()
        mock_response.text = "Figlet Text"
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response

        # Construct a request payload
        request_payload = json.dumps({
            "request_type": "figlet",
            "original_request": "generate a figlet for Hello World"
        })

        # Call the handle function
        response = handle(request_payload)
        # Additionally, verify that requests.post was called as expected
        mock_requests_post.assert_called_once_with(
            'http://gateway:8080/function/figlet',  # URL used in your function
            data="Hello World",  # Data passed to requests.post in your function
           
        )

    def test_handle_name(self):
        # Construct a request payload
        request_payload = json.dumps({
            "request_type": "name",
            "original_request": "What is your name?"
        })

        # Call the handle function
        response = handle(request_payload)
        self.assertIn("My name is ChatBot.", response)
        self.assertIn("I'm called ChatBot.", response)
        self.assertIn("You can call me ChatBot.", response)

    def test_handle_unknown(self):
        # Construct a request payload for an unknown request
        request_payload = json.dumps({
            "request_type": "unknown",
            "original_request": "How do you do?"
        })

        # Call the handle function
        response = handle(request_payload)
        self.assertEqual("Sorry, I didn't understand that.", response)

if __name__ == '__main__':
    unittest.main()

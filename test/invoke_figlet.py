import requests

def invoke_figlet(text):
    url = 'http://127.0.0.1:8080/function/figlet'
    headers = {'Content-Type': 'text/plain'}
    response = requests.post(url, data=text, headers=headers)
    return response

# Replace 'Hello World' with the text you want to convert to ASCII art
text_to_convert = 'Hello World'
figlet_response = invoke_figlet(text_to_convert)
print("Response from figlet:", figlet_response.text)
print("Status code:", figlet_response.status_code)
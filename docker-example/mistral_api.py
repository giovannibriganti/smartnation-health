import requests
import json

def make_api_call():
    url = 'http://127.0.0.1:11434/api/generate'
    payload = {
        "model": "mistral",
        "prompt": "Give an another name for mistral"
    }
    headers = {
        'Content-Type': 'application/json',
    }
    print("Call made")
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("API call successful!")
        print("Response:", response.json())
    else:
        print("API call failed. Status code:", response.status_code)

if __name__ == "__main__":
    make_api_call()


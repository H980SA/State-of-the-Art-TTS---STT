import os
from time import sleep
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def make_request(url, headers, method="GET", data=None, files=None):
    if method == "POST":
        response = requests.post(url, headers=headers, json=data, files=files)
    else:
        response = requests.get(url, headers=headers)
    return response.json()


def get_api_key():
    # Try to get API key from environment variable
    api_key = os.getenv("GLADIA_API_KEY")
    
    # If not found, try to load from config file
    if not api_key:
        config_path = os.path.join(os.path.dirname(__file__))
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    api_key = config.get("GLADIA_API_KEY")
                    print("- API key loaded from config file")
            except Exception as e:
                print(f"- Error loading config file: {e}")

    # If still not found, prompt the user
    if not api_key:
        print("- No API key found in environment or config file")
        api_key = input("Please enter your Gladia API key: ").strip()
        
    return api_key


print(os.getcwd())
file_path = r"C:\php-Course\State-of-the-Art TTS & STT\stt\cloud\audio.mp3"  # Change with your file path

if os.path.exists(file_path):  # This is here to check if the file exists
    print("- File exists")
else:
    print("- File does not exist")
    exit(0)


file_name, file_extension = os.path.splitext(
    file_path
)  # Get your audio file name + extension

with open(file_path, "rb") as f:  # Open the file
    file_content = f.read()  # Read the content of the file

# Get the API key using our new function
api_key = get_api_key()
if not api_key:
    print("- Error: No API key provided. Cannot proceed.")
    exit(1)

headers = {
    "x-gladia-key": api_key,
    "accept": "application/json",
}

files = [("audio", (file_path, file_content, "audio/" + file_extension[1:]))]

print("- Uploading file to Gladia...")
upload_response = make_request(
    "https://api.gladia.io/v2/upload/", headers, "POST", files=files
)
print("Upload response with File ID:", upload_response)

# Check if error occurred
if "statusCode" in upload_response and upload_response.get("statusCode") != 200:
    print(f"- Error uploading file: {upload_response.get('message')}")
    exit(1)

audio_url = upload_response.get("audio_url")

data = {
    "audio_url": audio_url,
    "diarization": True,
}
# You can also send an URL directly without uploading it. Make sure it's the direct link and publicly accessible.
# For any parameters, please see: https://docs.gladia.io/api-reference/pre-recorded-flow

headers["Content-Type"] = "application/json"

print("- Sending request to Gladia API...")
post_response = make_request(
    "https://api.gladia.io/v2/transcription/", headers, "POST", data=data
)

print("Post response with Transcription ID:", post_response)
result_url = post_response.get("result_url")

if result_url:
    while True:
        print("Polling for results...")
        poll_response = make_request(result_url, headers)

        if poll_response.get("status") == "done":
            print("- Transcription done: \n")
            print(poll_response.get("result"))
            break
        elif poll_response.get("status") == "error":
            print("- Transcription failed")
            print(poll_response)
        else:
            print("Transcription status:", poll_response.get("status"))
        sleep(1)

print("- End of work")
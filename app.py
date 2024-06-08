import os
import requests
import playsound
from langchain.llms import OpenAI

# OpenAI setup
llm = OpenAI(api_key="", temperature=0.8)
user_input = input("Enter your question: ")
output_text = llm.predict(user_input)

# Save the output to a text file
with open("input.txt", "w") as file:
    file.write(output_text)

print("Output has been saved to input.txt")

# Deepgram API key
DEEPGRAM_API_KEY = ""

def text_to_speech(input_filename, output_filename):
    try:
        with open(input_filename, "r") as file:
            text = file.read()

        # Construct the request payload
        payload = {
            "text": text
        }

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }

        # Send the request to Deepgram's text-to-speech API
        response = requests.post(
            "https://api.deepgram.com/v1/speak?model=aura-asteria-en",
            headers=headers,
            json=payload,
            stream=True
        )

        if response.status_code == 200:
            with open(output_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Audio content written to {output_filename}")

            # Play the audio file
            playsound.playsound(output_filename)
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    input_filename = "input.txt"
    output_filename = "output.mp3"
    text_to_speech(input_filename, output_filename)

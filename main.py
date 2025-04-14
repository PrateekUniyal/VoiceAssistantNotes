import requests
import sounddevice as sd
import numpy as np
import tempfile
import os
from scipy.io.wavfile import write
import json

# Configuration
GROQ_API_KEY = 'grok key'  
TRANSCRIPTION_API_URL = 'https://api.groq.com/openai/v1/audio/transcriptions'
CHAT_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
TRANSCRIPTION_MODEL = 'whisper-large-v3-turbo'
EXTRACTION_MODEL = 'llama-3.3-70b-versatile'
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 8  # seconds
  
def record_audio_chunk(duration, sample_rate, channels):
    """Record audio for a specified duration."""
    print(f"Recording for {duration} seconds... Please speak now.")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return audio_data

def save_wav_file(filename, data, sample_rate):
    """Save audio data to a WAV file."""
    write(filename, sample_rate, data)

def transcribe_audio(file_path):
    """Transcribe audio file using Groq's Whisper model."""
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }
    with open(file_path, 'rb') as audio_file:
        files = {
            'file': (file_path, audio_file, 'audio/wav')
        }
        data = {
            'model': TRANSCRIPTION_MODEL,
            'language': 'en'  # Directly request English transcription
        }
        response = requests.post(TRANSCRIPTION_API_URL, headers=headers, files=files, data=data)
        if response.status_code == 200:
            return response.json().get('text', '')
        else:
            print(f"Transcription Error: {response.status_code}, {response.text}")
            return None

def extract_information(text):
    """Extract material, grade, quantity, and delivery time from text using Groq's LLM."""
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    prompt = (
        "You are an assistant tasked with extracting specific information from text. "
        "Given the following text, extract the following fields: material, grade, quantity, and delivery time. "
        "Return the result as a JSON object. If any field is not found, set its value to null. "
        "Ensure the output is valid JSON.\n\n"
        f"Text: {text}\n\n"
        "Example output:\n"
        "{\n"
        '  "material": "steel",\n'
        '  "grade": "A36",\n'
        '  "quantity": "500 kg",\n'
        '  "delivery_time": "2 weeks"\n'
        "}\n"
    )
    payload = {
        'model': EXTRACTION_MODEL,
        'messages': [
            {
                'role': 'system',
                'content': prompt
            },
            {
                'role': 'user',
                'content': 'Extract the information from the provided text.'
            }
        ],
        'response_format': {'type': 'json_object'},
        'temperature': 0.2,  # Low temperature for deterministic output
        'max_tokens': 200
    }
    response = requests.post(CHAT_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content']
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing extraction response: {e}")
            return None
    else:
        print(f"Extraction Error: {response.status_code}, {response.text}")
        return None

def main():
    try:
        # Record one audio chunk
        audio_chunk = record_audio_chunk(CHUNK_DURATION, SAMPLE_RATE, CHANNELS)

        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
            temp_path = tmpfile.name
        save_wav_file(temp_path, audio_chunk, SAMPLE_RATE)

        # Transcribe audio
        transcription = transcribe_audio(temp_path)
        if transcription:
            print(f"Transcribed in English: {transcription}")

            # Extract information
            extracted_info = extract_information(transcription)
            if extracted_info:
                try:
                    # Parse JSON string to dictionary
                    info_dict = json.loads(extracted_info)
                    print("Extracted Information:")
                    print(f"Material: {info_dict.get('material', 'Not found')}")
                    print(f"Grade: {info_dict.get('grade', 'Not found')}")
                    print(f"Quantity: {info_dict.get('quantity', 'Not found')}")
                    print(f"Delivery Time: {info_dict.get('delivery_time', 'Not found')}")
                except json.JSONDecodeError as e:
                    print(f"Error parsing extracted info: {e}")
            else:
                print("Failed to extract information.")
        else:
            print("No transcription available.")

        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except OSError as e:
            print(f"Error deleting temp file: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
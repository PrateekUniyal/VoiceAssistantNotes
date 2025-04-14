This feature takes as input the user speech(maybe in some other language medium than English) and transcribes it . Once the speech is transcribed , some key information points are extracted.

This can be accomplished by the use of [[Whisper AI]] , [[Azure_Speech]] and [[Llama]].
## Libraries used are:

| Library          | Purpose                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| requests         | Handle http requests to groq APIs to send audio over API and recieve JSON response                         |
| soundevice       | Used to capture audio through microphone  works well with numpy to work with audio data.                   |
| numpy            | save the audio data as arrays.                                                                             |
| tempfile         | Create temporary files(.wav file) for storing audio to send via API to Groqs [[Whisper AI]] to transcribe. |
| os               | Used to work with file system operations mainly deleting temporary files,                                  |
| scipy.io.wavfile | Converts NumPy array having raw audio data to .wav file for sending to model.                              |
| json             | Take JSON response from Groq API and convert to python dictionary for easier working.                      |
## Function Structure:

| Function              | Purpose                                                                             | Parameters                      | Return                  |
| --------------------- | ----------------------------------------------------------------------------------- | ------------------------------- | ----------------------- |
| record_audio_chunk()  | record audio for taking in order                                                    | duration, sample_rate, channels | audio_data(NumPy array) |
| save_wav_file()       | Save audio array to a WAV file                                                      | filename, data, sample_rate     |                         |
| transcribe_audio()    | Sends the audio file for transcription and save the response in a python dictionary | filepath                        | None                    |
| extract_information() | Extract the required information from the transcribed text.                         | text                            | None                    |
| main()                | Control the flow of tasks                                                           |                                 |                         |


## API Billing(metrics based on free tier):
### Whisper large V3 turbo 
* requests per minute = 20
* requests per day = 2000
* Audio seconds per hour = 7200
* Audio seconds per day = 28800

### Llama-3.3-70b-versatile
* requests per minute = 30
* requests per day = 1000
* tokens per minute = 6000
*  tokens per day = 100000


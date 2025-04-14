This is a state of art, open source speech recognition system designed for robust and multilingual transcription and translation tasks. Whisper uses the encoder-decoder transformer architecture.

# Working
- Audio pre processing
- Encoder
- Decoder

## Audio pre-processing:
The input audio is resampled to 16kHz and converted into an 80-channel log magnitude Mel spectrogram.

## Encoder:
The spectrogram is passed through convolutional layers, followed by series of transformer encoder blocks with pre-activation residual connections. Sinusoidal positional  embeddings  are added to capture temporal information.

## Decoder:
The decoder has the similar width and block structure, processes the encoded representation. It utilizes learned positional embeddings and a byte pair encoding tokenizer. Special tokens are used to guide tasks such as language identification and timestamp generation.

---

# Capabilities
* Supports transcription in 99 languages, English having the highest accuracy.
* Can translate non English text to English text.
* As result of being trained on a diverse dataset, is quite robust when it comes to background noise or handling different accents.
* Timestamp generation helps in alignment of text to audio.
* Provide near real-time transcription making it suitable for live applications.

---
## Limitations
* Whisper can sometimes generate text which were not spoken, especially during silences or unclear audio segments.
* Can show variance in accuracy depending on the language.
* Not capable of differentiating between different speakers.
* Mostly real time but can vary depending on the hardware and model variant being used.

---

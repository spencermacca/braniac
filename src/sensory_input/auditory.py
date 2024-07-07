import numpy as np
import speech_recognition as sr
import logging
from textblob import TextBlob
from neural_networks.sound_recognition import SoundRecognitionNN
import pyaudio

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

class AuditoryProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sound_recognition_nn = SoundRecognitionNN()

    def process_auditory_input(self, auditory_data):
        try:
            audio = sr.AudioData(auditory_data.tobytes(), RATE, 2)
            text = self.recognizer.recognize_google(audio)
            logging.info(f"Recognized audio: {text}")
            processed_data = self.sound_recognition_nn.process_sound(text)
            sentiment = TextBlob(text).sentiment.polarity
            return processed_data, sentiment
        except sr.UnknownValueError:
            logging.error("Could not understand audio")
            return "Could not understand audio", None
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            return f"Could not request results from Google Speech Recognition service; {e}", None

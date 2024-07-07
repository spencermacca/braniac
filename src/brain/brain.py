import cv2
import numpy as np
import threading
import time
import logging
import speech_recognition as sr
from textblob import TextBlob
from neural_networks.language_processing import LanguageProcessingNN
from neural_networks.memory_management import MemoryManagementNN
from neural_networks.decision_making import DecisionMakingNN
from neural_networks.sound_recognition import SoundRecognitionNN
from neural_networks.texture_recognition import TextureRecognitionNN
from brain.emotion import Emotion
from brain.learning_algorithms import LearningAlgorithms
from brain.motor_control import MotorControl
import pyaudio

# Configure logging
logging.basicConfig(level=logging.INFO)

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

class Brain:
    def __init__(self):
        self.neural_networks = {
            'language_processing': LanguageProcessingNN(),
            'memory_management': MemoryManagementNN(),
            'decision_making': DecisionMakingNN(),
            'sound_recognition': SoundRecognitionNN(),
            'texture_recognition': TextureRecognitionNN(),
        }
        self.sensory_inputs = {}
        self.emotion = Emotion()
        self.learning = LearningAlgorithms()
        self.motor_control = MotorControl()
        self.running = False
        self.latest_frame = None
        self.latest_decision = None
        self.latest_emotion = None
        self.latest_audio = None
        self.recognizer = sr.Recognizer()
        self.audio_thread = None

    def process_visual_input(self, visual_data):
        gray_image = cv2.cvtColor(visual_data, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        average_brightness = np.mean(gray_image)
        return edges, average_brightness

    def process_input(self, input_data):
        sensory_type, sensory_data = input_data
        if sensory_type == 'visual':
            edges, brightness = self.process_visual_input(sensory_data)
            self.sensory_inputs['visual'] = edges
            self.sensory_inputs['visual_brightness'] = brightness
        elif sensory_type == 'auditory':
            self.sensory_inputs['auditory'] = self.process_auditory_input(sensory_data)
        elif sensory_type == 'tactile':
            self.sensory_inputs['tactile'] = self.process_tactile_input(sensory_data)
        else:
            raise ValueError(f"Unsupported sensory type: {sensory_type}")

    def process_auditory_input(self, auditory_data):
        try:
            audio = sr.AudioData(auditory_data.tobytes(), RATE, 2)
            text = self.recognizer.recognize_google(audio)
            logging.info(f"Recognized audio: {text}")
            self.latest_audio = text
            processed_data = self.neural_networks['sound_recognition'].process_sound(text)
            self.analyze_emotion_from_audio(text)
        except sr.UnknownValueError:
            logging.info("Could not understand audio")
            processed_data = "Could not understand audio"
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            processed_data = f"Could not request results from Google Speech Recognition service; {e}"
        return processed_data

    def analyze_emotion_from_audio(self, text):
        sentiment = TextBlob(text).sentiment.polarity
        if sentiment > 0:
            self.process_emotion("Happy")
        elif sentiment < 0:
            self.process_emotion("Sad")
        else:
            self.process_emotion("Neutral")

    def process_tactile_input(self, tactile_data):
        processed_data = self.neural_networks['texture_recognition'].classify_texture(tactile_data)
        return processed_data

    def make_decision(self):
        decisions = []
        if 'visual_brightness' in self.sensory_inputs:
            average_brightness = self.sensory_inputs['visual_brightness']
            decision = "Visual analysis: Bright image" if average_brightness > 127 else "Visual analysis: Dark image"
            decisions.append(decision)
        if self.latest_audio:
            decisions.append(f"Auditory analysis: {self.latest_audio}")
        decision_output = " | ".join(decisions)
        self.neural_networks['memory_management'].store_memory('latest_decision', decision_output)
        self.latest_decision = decision_output
        return decision_output

    def generate_output(self):
        decision_output = self.neural_networks['memory_management'].retrieve_last_memory('latest_decision')
        if decision_output:
            output = self.neural_networks['language_processing'].generate_output(decision_output)
        else:
            output = "No recent decision available to generate output."
        return output

    def process_emotion(self, emotion_data):
        self.emotion.process_emotion(emotion_data)
        self.latest_emotion = self.emotion.generate_response()
        logging.info(f"Processed emotion: {emotion_data} | Response: {self.latest_emotion}")

    def generate_emotional_response(self):
        return self.emotion.generate_response()

    def capture_audio(self):
        while self.running:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    logging.info("Listening for audio...")
                    audio = self.recognizer.listen(source)
                    audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                    self.process_input(('auditory', audio_data))
            except Exception as e:
                logging.error(f"Error capturing audio: {e}")
            time.sleep(0.1)  # Adjust the delay as needed

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height
        if not cap.isOpened():
            logging.error("Error: Could not open video device.")
            return
        # Start audio capture in a separate thread
        self.audio_thread = threading.Thread(target=self.capture_audio)
        self.audio_thread.start()
        while self.running:
            ret, frame = cap.read()
            if ret:
                edges, brightness = self.process_visual_input(frame)
                self.latest_frame = edges
                self.process_input(('visual', frame))

            # Placeholder for tactile inputs
            tactile_input_data = ('tactile', 0.7)
            self.process_input(tactile_input_data)

            self.make_decision()
            time.sleep(0.1)  # Reduced delay to improve framerate

        cap.release()
        self.audio_thread.join()

    def stop(self):
        self.running = False

brain = Brain()

def start_brain():
    brain_thread = threading.Thread(target=brain.run)
    brain_thread.start()
    return brain_thread

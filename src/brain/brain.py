import cv2
import numpy as np
import threading
import time
import speech_recognition as sr
import pyaudio
import logging
from brain.emotion import Emotion
from brain.learning_algorithms import LearningAlgorithms
from brain.motor_control import MotorControl
from neural_networks.language_processing import LanguageProcessingNN
from neural_networks.memory_management import MemoryManagementNN
from neural_networks.decision_making import DecisionMakingNN
from sensory_input import AuditoryProcessor, VisualProcessor, TactileProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)

class Brain:
    def __init__(self):
        self.neural_networks = {
            'language_processing': LanguageProcessingNN(),
            'memory_management': MemoryManagementNN(),
            'decision_making': DecisionMakingNN(),
        }
        self.sensory_inputs = {}
        self.emotion = Emotion()
        self.learning = LearningAlgorithms()
        self.motor_control = MotorControl()
        self.auditory_processor = AuditoryProcessor()
        self.visual_processor = VisualProcessor()
        self.tactile_processor = TactileProcessor()
        self.recognizer = sr.Recognizer()
        self.running = False
        self.latest_frame = None
        self.latest_decision = None
        self.latest_emotion = "The system has no strong emotional response."
        self.latest_audio = None
        self.audio_thread = None

    def process_input(self, input_data):
        sensory_type, sensory_data = input_data
        if sensory_type == 'visual':
            edges, brightness = self.visual_processor.process_visual_input(sensory_data)
            self.sensory_inputs['visual'] = edges
            self.sensory_inputs['visual_brightness'] = brightness
            self.analyze_emotion_from_visual(brightness)
        elif sensory_type == 'auditory':
            processed_data, sentiment = self.auditory_processor.process_auditory_input(sensory_data)
            self.sensory_inputs['auditory'] = processed_data
            self.latest_audio = processed_data
            self.analyze_emotion_from_audio(sentiment)
        elif sensory_type == 'tactile':
            self.sensory_inputs['tactile'] = self.tactile_processor.process_tactile_input(sensory_data)
        else:
            raise ValueError(f"Unsupported sensory type: {sensory_type}")

    def analyze_emotion_from_visual(self, brightness):
        if brightness > 127:
            self.process_emotion("Bright")
        else:
            self.process_emotion("Dark")

    def analyze_emotion_from_audio(self, sentiment):
        logging.info(f"Audio sentiment polarity: {sentiment}")
        if sentiment is not None:
            if sentiment > 0.2:
                self.process_emotion("Happy")
            elif sentiment < -0.2:
                self.process_emotion("Sad")
            else:
                self.process_emotion("Neutral")

    def process_emotion(self, emotion_data):
        self.emotion.process_emotion(emotion_data)
        self.latest_emotion = self.emotion.generate_response()
        logging.info(f"Processed emotion: {emotion_data} | Response: {self.latest_emotion}")

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
            except sr.UnknownValueError:
                logging.error("Could not understand audio")
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech Recognition service; {e}")
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
                edges, brightness = self.visual_processor.process_visual_input(frame)
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

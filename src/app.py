from flask import Flask, render_template, Response, request, jsonify
import cv2
import pyaudio
import numpy as np
import threading
import time
from brain.brain import brain, start_brain

app = Flask(__name__)

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Initialize Emotion
emotion = brain.emotion

audio_buffer = []

def generate_frames():
    while True:
        if brain.latest_frame is not None:
            frame = brain.latest_frame
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

def audio_callback(in_data, frame_count, time_info, status):
    global audio_buffer
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    audio_buffer = audio_data.tolist()
    return (in_data, pyaudio.paContinue)

@app.route('/audio_feed')
def audio_feed():
    def generate():
        while True:
            global audio_buffer
            yield f"data: {audio_buffer}\n\n"
            time.sleep(0.1)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_params', methods=['POST'])
def update_params():
    min_val = int(request.form['minVal'])
    max_val = int(request.form['maxVal'])
    return '', 204

@app.route('/process_emotion', methods=['POST'])
def process_emotion():
    emotion_data = request.form['emotion']
    brain.process_emotion(emotion_data)
    response = brain.latest_emotion
    return jsonify({'response': response})

@app.route('/latest_decision', methods=['GET'])
def latest_decision():
    decision = brain.latest_decision
    return jsonify({'decision': decision})

@app.route('/start_brain', methods=['POST'])
def start_brain_route():
    brain_thread = start_brain()
    return '', 204

@app.route('/stop_brain', methods=['POST'])
def stop_brain_route():
    brain.stop()
    return '', 204

if __name__ == '__main__':
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=audio_callback)
    stream.start_stream()
    
    app.run(debug=True, threaded=True)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

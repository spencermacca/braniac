class Emotion:
    def __init__(self):
        self.current_emotion = None
        self.emotion_history = []

    def process_emotion(self, emotion_data):
        """
        Process the input emotion data and update the current emotional state.
        :param emotion_data: A string representing the detected emotion (e.g., "Happy", "Sad").
        """
        self.current_emotion = emotion_data
        self.emotion_history.append(emotion_data)
        print(f"Processed emotion: {emotion_data}")

    def generate_response(self):
        """
        Generate a response based on the current emotional state.
        :return: A string representing the response.
        """
        if self.current_emotion == "Happy":
            return "The system is feeling happy!"
        elif self.current_emotion == "Sad":
            return "The system is feeling sad."
        elif self.current_emotion == "Angry":
            return "The system is feeling angry."
        elif self.current_emotion == "Surprised":
            return "The system is feeling surprised."
        else:
            return "The system has no strong emotional response."

    def get_emotion_history(self):
        """
        Retrieve the history of processed emotions.
        :return: A list of processed emotions.
        """
        return self.emotion_history

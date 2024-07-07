import unittest
from brain.emotion import Emotion

class TestEmotion(unittest.TestCase):

    def setUp(self):
        self.emotion = Emotion()

    def test_process_emotion(self):
        self.emotion.process_emotion("Happy")
        response = self.emotion.generate_response()
        self.assertEqual(response, "The system is feeling happy!")

if __name__ == '__main__':
    unittest.main()

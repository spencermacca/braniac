import unittest
import numpy as np
from brain.brain import Brain

class TestBrain(unittest.TestCase):

    def setUp(self):
        self.brain = Brain()

    def test_process_visual_input(self):
        visual_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        edges, brightness = self.brain.process_visual_input(visual_data)
        self.assertIsNotNone(edges)
        self.assertIsInstance(brightness, float)

    def test_process_auditory_input(self):
        auditory_data = np.random.randint(0, 256, 44100, dtype=np.int16)
        processed_data = self.brain.process_auditory_input(auditory_data)
        self.assertIsNotNone(processed_data)

    def test_make_decision(self):
        visual_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        self.brain.process_input(('visual', visual_data))
        decision = self.brain.make_decision()
        self.assertIn("Visual analysis", decision)

if __name__ == '__main__':
    unittest.main()

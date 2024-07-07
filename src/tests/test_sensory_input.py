import unittest

import numpy as np
from sensory_input.auditory import AuditoryProcessor
from sensory_input.visual import VisualProcessor

class TestSensoryInput(unittest.TestCase):

    def setUp(self):
        self.auditory_processor = AuditoryProcessor()
        self.visual_processor = VisualProcessor()

    def test_auditory_input(self):
        auditory_data = np.random.rand(1000).astype(np.float32)
        processed_data = self.auditory_processor.process_auditory_input(auditory_data)
        self.assertIsNotNone(processed_data)

    def test_visual_input(self):
        visual_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        edges, brightness = self.visual_processor.process_visual_input(visual_data)
        self.assertIsNotNone(edges)
        self.assertIsInstance(brightness, float)

if __name__ == '__main__':
    unittest.main()

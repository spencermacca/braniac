import unittest
import numpy as np
from neural_networks.language_processing import LanguageProcessingNN
from neural_networks.memory_management import MemoryManagementNN
from neural_networks.decision_making import DecisionMakingNN

class TestNeuralNetworks(unittest.TestCase):

    def setUp(self):
        self.language_processing = LanguageProcessingNN()
        self.memory_management = MemoryManagementNN()
        self.decision_making = DecisionMakingNN()

    def test_language_processing(self):
        output = self.language_processing.generate_output("Test input")
        self.assertIsNotNone(output)

    def test_memory_management(self):
        self.memory_management.store_memory('test_key', 'test_value')
        value = self.memory_management.retrieve_last_memory('test_key')
        self.assertEqual(value, 'test_value')

    def test_decision_making(self):
        visual_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        decision = self.decision_making.make_decision({'visual': visual_data})
        self.assertIsNotNone(decision)

if __name__ == '__main__':
    unittest.main()

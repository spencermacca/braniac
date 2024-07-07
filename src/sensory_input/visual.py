import cv2
import numpy as np

class VisualProcessor:
    def process_visual_input(self, visual_data):
        average_brightness = np.mean(cv2.cvtColor(visual_data, cv2.COLOR_BGR2GRAY))
        gray_image = cv2.cvtColor(visual_data, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        return edges, average_brightness

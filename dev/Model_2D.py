from Model import Model
import numpy as np

class Model2D(Model):
    """
    Model class for 2 dimensional model structures.
    """


    def __init__(self, image_name, quantization_numbers):
        """
        """
        self.image_name = image_name
        self.quantization_numbers = quantization_numbers
        self.compressed_images = []

    def gaussian_analysis(self):
        """
        Gaussian Analysis for post compression effect.
        """
        pass
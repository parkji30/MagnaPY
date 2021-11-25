import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from astropy.io import fits

class ArrayND:
    def __init__(self, name, data):
        """
        """
        self.name = name
        self.original_data = data
        self.compressed_data = {}

    def add_compressed_data(self, data, alg):
        self.compressed_data[alg] = data

    def update_compressed_data_dictionary(self, new_compressed_dictionary):
        self.compressed_data = new_compressed_dictionary


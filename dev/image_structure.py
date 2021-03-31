import os
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import math

class ImageStructure:
    """
    The DataStructure class object is used to represent an abstract image or datafile

    """
    def __init__(self, image, compressor):
        """
        @type self: DataStructure compression object
        @type image_name: String
            (Name of data structure object)
        @rtype: None
        """
        self.image_fits = image
        self.compressor = compressor
        self.original_data = self.image_fits[0].data
        self.compressed_data = self.compress_data()
        # self.image_info = self.get_info(image)
        
    def compress_data(self, raw=True):
        """
        @type self:
        """
        if raw:
            self.compressed_data = self.compressor.compress()
        else:
            self.compressed_data = self.compressor.uncompress()

    # def load_data(self):
    #     """
    #     Currently this method is designed to handle numpy, fits, and
    #     text file objects only.
    #
    #     Future versions may handle .dat, .csv, .dir and other file types.
    #
    #     @type self: ImageStructure
    #     @rtype:
    #     """
    #     return None

    def get_info(self, data):
        """
        """
        return None

    def get_image_name(self):
        """
        """
        return "Random Name"

    def get_original_data(self):
        """
        """
        return self.original_data

    def get_compressed_data(self):
        """
        """
        return self.compressed_data



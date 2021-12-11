import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from astropy.io import fits

class ImageArrayND:
    def __init__(self, original_data, compressed_data):
        """
        Data input must be np arrays, 2D or 1D are both fine.

        """
        self.original_data = original_data
        self.compressed_data = compressed_data

    def __repr__(self):
        """
        Representation of this python object when called upon.

        @type self: Balco
        @rtype: String
            When this object is called, it will be represented
            by it's compressed name.
        """
        return self.image_name

    def __str__(self):
        """
        Representation of this python object when used as a string.

        """
        return self.get_name(version="compressed")

    def get_data(self, version):
        """
        Returns the image data of the desired version.

        @type self: Image

        @type version: String
            1) Original obtains the original image. 
            2) Compressed obtains the compressed image.
            3) Difference obtains original subtracted by the compressed image.

        @rtype: String
            Returns the data of the selected version.
        """
        if version.lower() == 'original':
            return self.original_data
        elif version.lower() == 'compressed':
            return self.compressed_data
        elif version.lower() == 'residual':
            return self.original_data - self.compressed_data
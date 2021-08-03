import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from astropy.io import fits

class ArrayND:
    def __init__(self, original_image, compressed_image_path):
        """
        """
        # Original array data.
        self.original_data = fits.getdata(original_image)
        self.compressed_data = fits.getdata(compressed_image_path)

        # Compressed Image Name
        self.image_name = compressed_image_path.split('/')[-1]
        self.compression_factor = self.original_data.nbytes / self.compressed_data.nbytes

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

        @type self: Balco
        @rtype: String
            When this object is used as a string, it will be
            represented by it's compressed name.
        """
        return self.get_name(version="compressed")

    def return_compression_factor():
        return self.compression_factor

    def get_mms(self, version='original'):
        """
        Returns the mean, median, standard deviation of the input image.

        @type self: Model

        @type version: String
            1) Original returns the original image. 
            2) Compressed returns the compressed image.
            3) Difference returns original subtracted by the compressed image.

        @rtype: String
            Returns the mean, median and standard deviation of the selected
            version.
        """
        original = self.original_data
        compressed = self.compressed_data

        if version.lower()=='original':
            return [np.mean(original), np.median(original), np.std(original)]
        elif version.lower()=='compressed':
            return [np.mean(compressed), np.median(compressed), np.std(compressed)]
        elif version.lower()=='residual':
            return [np.mean(original - compressed), \
                    np.median(original - compressed), \
                    np.std(original - compressed)]

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

    def get_psd_data(self, version):
        """
        Returns the image PSD data of the desired version.

        @type self: Image

        @type version: String
            1) Original obtains the original image. 
            2) Compressed obtains the compressed image.
            3) Difference obtains original subtracted by the compressed image.

        @rtype: String
            Returns the data of the selected version.
        """
        if version.lower() == 'original':
            return self.original_psd
        elif version.lower() == 'compressed':
            return self.compressed_psd
        elif version.lower() == 'residual':
            return self.original_psd - self.compressed_psd

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from astropy.io import fits

class Visualizer:
    """
    The modelling class which will be used to compare the original
    image to it's compressed image.

    Various features are implemented such as:
        (1) Compression factor vs. Image Quality
        (2) Power Spectrum Analysis
        (3) Image Reduction
    """

    def __init__(self, image_object):
        """

        @type self: Model
        @type image_structure: ImageStructure Object
                As defined in the code within the file.
        """
        self.image_structure = image_object
        self.image_info = self.get_image_info()

    def get_image_info(self):
        """
        """
        return {'name': self.image_structure.get_image_name(),
            'original': self.image_structure.get_original_data(),
            'compressed': self.image_structure.get_compressed_data()}

    def Im_show(self):
        """
        Displays the image using matplotlib.pyplot

        @type self: Model
        """
        plt.figure(figsize=(10, 10))
        plt.title("Original Image")
        plt.imshow(self.image_info['original'])
        plt.colorbar()
        plt.show()

    def Im_show_compressed(self):
        """
        Displays the image using matplotlib.pyplot

        @type self: Model
        """
        compressed = self.image_info['compressed']
        plt.figure(figsize=(10, 10))
        plt.title("Compressed Image")
        plt.imshow(compressed.data)
        plt.colorbar()
        plt.show()
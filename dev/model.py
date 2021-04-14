import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from astropy.io import fits

class Model:
    """
    The modelling class which will be used to compare the original
    image to it's compressed image.

    Various features are implemented such as:
        (1) Compression factor vs. Image Quality
        (2) Power Spectrum Analysis
        (3) Image Reduction
    """
    def __init__(self, data, compressed_data, title=''):
        """
        @type self: Model
        @type image_structure: ImageStructure Object
                As defined in the code within the file.
        """
        self.data = data
        self.compressed_data = compressed_data
        self.title = title

    def Im_show_original(self):
        """
        Displays the original Image

        @type self: Model
        """
        plt.figure(figsize=(10, 10))
        plt.title("Original " + self.title)
        plt.imshow(self.data)
        plt.colorbar()
        plt.show()

    def Im_show_compressed(self):
        """
        Displays the compressed Image

        @type self: Model
        """
        plt.figure(figsize=(10, 10))
        plt.title("Compressed " + self.title)
        plt.imshow(self.compressed_data)
        plt.colorbar()
        plt.show()

    def Im_show_difference(self):
        """
        Displays the residual between the original and compressed image.
        """
        plt.figure(figsize=(10, 10))
        plt.title("Residual " + self.title)
        plt.imshow(self.data - self.compressed_data)
        plt.colorbar()
        plt.show()

    def print_statistics(self, original_view=True):
        """
        Returns basic statistics about the compressed and original image.
        """
        original = self.data
        compressed = self.compressed_data

        if original_view:
            return("\nOriginal Image" + \
                    "\n----------------------" + \
                    "\nMean: "+ str(np.mean(original)) + \
                    "\nMedian: "+ str(np.median(original)) + \
                    "\nStandard Deviation: " + str(np.std(original)) + '\n')
        else:
            print("\nCompressed Image" + \
                    "\n----------------------" + \
                    "\nMean: "+ str(np.mean(compressed)) +
                    "\nMedian: "+ str(np.median(compressed)) +
                    "\nStandard Deviation: "+ str(np.std(compressed)) + '\n')

    def get_mms(self, original_view=True):
        """
        Returns the mean, median, standard deviation of the input image.

        @type self: Model
        @type original_view: Boolean (Display the original or compressed Image)
        """
        original = self.data
        compressed = self.compressed_data

        if original_view:
            return [np.mean(original), np.median(original), np.std(original)]
        else:
            return [np.mean(compressed), np.median(compressed), np.std(compressed)]

    def return_difference(self):
        """
        Returns the difference of the mean, median, standard deviation of the
        original and compressed image.

        @type self: Model
        @rtype:  Tuple[ mean, median, standard deviation ]
            (Original - compressed)
        """
        original = self.data
        compressed = self.compressed_data

        return (np.mean(original) - np.mean(compressed),
                np.median(original) - np.median(compressed),
                np.std(original) - np.std(compressed))


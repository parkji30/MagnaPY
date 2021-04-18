import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from scipy import signal

class Model:
    """
    The modelling class which will be used to compare the original
    image to it's compressed image.

    Various features are implemented such as:
        (1) Compression factor vs. Image Quality
        (2) Power Spectrum Analysis
        (3) Image Reduction
    """
    def __init__(self, image_name):
        """
        @type self: Model
        @type image_structure: ImageStructure Object
                As defined in the code within the file.
        """
        self.original_image_name = image_name
        self.compressed_images = []
        
    def print_statistics(self, version='original'):
        """
        Returns basic statistics about the compressed and original image.
        """
        original = self.data
        compressed = self.compressed_data

        if version.lower()=='original':
            print("\nOriginal Image" + \
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

    def get_image_name(self):
        """
        Returns the name of the original image (not compressed)

        @type self: Model
        @rtype: String
            Name of original image.
        """
        return "The Model is based of the Image: " + self.original_image_name

    def current_compressed_images(self):
        """

        """
        for i in range(len(self.compressed_images)):
            print(str(i) + ') ' + self.compressed_images[i])
        return self.compressed_images

    def update_compressed_list(self, Image):
        """
        Updates the compressed list of image objects but appending a new 
        compressed Image Object to the list of compressed images.

        @type self: Model Object
        @type Image: Image Object
        @rtype: None
        """
        self.compressed_images.append(Image)

    def get_compressed_list(self):
        """
        Returns a list of all compressed Image objects.

        @type self: Model Object
        @rtype: List[Images]
            returns the list of all compressed Images that this Model is analysing.
        """
        return self.compressed_images

    def run_analysis(self, cutoff=2):
        """
        Finds the optimally compressed image to compressed factor based off the list of images.

        @type self: Model 
            Model object used to run the analysis of the compressed images.
        @type cutoff: Float
            percentage value used to indicate residual cutoff.
        @rtype: None
        """
        residual_values = {}
        for compressed_image in self.compressed_images:
            residual_values[compressed_image.get_name()] \
                 = np.mean(np.abs(compressed_image.get_data(version='original') - compressed_image.get_data(version='compressed')))

        # updated_residual_values = {}
        # for value in residual_values:
        #     if residual_values[value] > cutoff/10000:
        #         updated_residual_values[value] = residual_values[value]

        return residual_values
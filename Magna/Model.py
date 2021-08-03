import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from scipy import signal

class LossModel:
    """
    The modelling class which will be used to compare the original
    image to it's compressed image.

    Various features are implemented such as:
        (1) Compression factor vs. Image Quality
        (2) Power Spectrum Analysis
        (3) Image Reduction
    """
    def __init__(self, text_report):
        """
        """
        self.text_file = text_report
        self.image_arrays = []

    def write_info(self, image_array):
        """
        """
        file = open(self.text_file, 'a')
        file.write('\n' + image_array.image_name + "\t " + str(image_array.compression_factor) \
                                          + "\t " + str(np.min(image_array.original_data)) \
                                          + "\t " + str(np.max(image_array.original_data)) \
                                          + "\t " + str(np.mean(image_array.original_data)) \
                                          + "\t " + str(np.std(image_array.original_data)) \
                                          + "\t " + str(np.min(image_array.compressed_data)) \
                                          + "\t " + str(np.max(image_array.compressed_data)) \
                                          + "\t " + str(np.mean(image_array.compressed_data)) \
                                          + "\t " + str(np.std(image_array.compressed_data)))
        file.close()

    def update_array_list(self, array):
        """
        Updates the compressed list of image objects but appending a new 
        compressed Image Object to the list of compressed images.

        @type self: Model Object
        @type Image: Image Object
        @rtype: None
        """
        self.image_arrays.append(array)

    def run_gaussian_analysis(self, cutoff=0.05, cfactor=2):
        """
        Investigates the quality of the image based off the compression factor.

        @type self: Model 
            Model object used to run the analysis of the compressed images.
        @type cutoff: Float
            percentage value used to indicate residual cutoff.
        @rtype: None
        """
        pass

    def show_residual_PSD_vs_compression_factor(self):
        """
        Shows the relationship between the residual (PSD) of the images vs.
        it's compression factor.

        @type self: Model
        @rtype: None
            Displays an interactive Matplotlib figure.
        """
        max_residuals = [np.max(np.abs(image.get_psd_data(version='residual'))) for image in self.compressed_images]
        min_residuals = [np.min(np.abs(image.get_psd_data(version='residual'))) for image in self.compressed_images]
        factors = self.get_compressed_factors()

        plt.figure(figsize=(9, 6))
        plt.title("PSD Residual (Max & Min values) vs. Compression Factor")
        plt.plot(factors, max_residuals, label="Max", linestyle="None", marker='x')
        plt.plot(factors, min_residuals, label='Min', linestyle="None", marker='+')
        plt.xlabel("Compression Factor")
        plt.ylabel("Frequency [Hz]")
        plt.legend()
        plt.show()

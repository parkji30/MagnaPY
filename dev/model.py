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
    def __init__(self, image_name, compression_factors):
        """
        @type self: Model
        @type image_structure: ImageStructure Object
                As defined in the code within the file.
        """
        self.original_image_name = image_name
        self.compressed_images = []
        self.compression_factors = compression_factors

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

    def get_compressed_factors(self):
        """
        Returns a list of the compression factors of the images.

        @type self: Model Object
        @rtype: List[Floats]
            returns the list of all compression factors.
        """
        return [img.get_compressed_factor() for img in self.compressed_images]

    def run_analysis(self, cutoff = 0.5):
        """
        Investigates the quality of the image based off the compression factor.

        @type self: Model 
            Model object used to run the analysis of the compressed images.
        @type cutoff: Float
            percentage value used to indicate residual cutoff.
        @rtype: None
        """
        percentile_difference = {}
        for compressed_image in self.compressed_images:
            percentile_difference[compressed_image.get_name(version='compressed')] \
                = compressed_image.get_data(version='original') - compressed_image.get_data(version='compressed')
        
        updated_percentile_value = {}
        for percentile in percentile_difference:
            if np.all(np.abs(percentile_difference[percentile]) < cutoff):
                updated_percentile_value[percentile] = percentile_difference[percentile]
                print("Passes the Threshold!")
            # To do
            # Show where the code failed.

        # Also to look at. Regions where maximal difference is lower than the cutoff, but 
        # investigate overall difference around the image.

        # Return regions where differences are more than a certain percentage higher but still
        # lower than the cutoff.          
        # Code ---->
        # To do....

        # Look into the PSD of the images.

        return updated_percentile_value

    def show_residual_vs_compression_factor(self):
        """
        Shows the relationship between the residual of the images vs.
        it's compression factor.

        @type self: Model
        @rtype: None
            Displays an interactive Matplotlib figure.
        """
        max_residuals = [np.max(np.abs(image.get_data(version='residual'))) for image in self.compressed_images]
        min_residuals = [np.min(np.abs(image.get_data(version='residual'))) for image in self.compressed_images]
        factors = self.compression_factors
        
        plt.figure(figsize=(9, 6))
        plt.title("Residual (Max & Min Values) vs. Compression Factor")
        plt.plot(factors, max_residuals, label="Max", linestyle="None", marker='.')
        plt.plot(factors, min_residuals, label='Min', linestyle="None", marker='+')
        plt.xlabel("Compression Factor")
        plt.ylabel("Residual")
        plt.legend()
        plt.show()

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
        factors = self.compression_factors

        plt.figure(figsize=(9, 6))
        plt.title("PSD Residual (Max & Min values) vs. Compression Factor")
        plt.plot(factors, max_residuals, label="Max", linestyle="None", marker='x')
        plt.plot(factors, min_residuals, label='Min', linestyle="None", marker='+')
        plt.xlabel("Compression Factor")
        plt.ylabel("Frequency [Hz]")
        plt.legend()
        plt.show()

   
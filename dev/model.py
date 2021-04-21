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
    def __init__(self, image_name, quantization_numbers):
        """
        @type self: Model
        @type image_structure: ImageStructure Object
                As defined in the code within the file.
        """
        self.original_image_name = image_name
        self.compressed_images = []
        self.quantization_numbers = quantization_numbers

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

    def get_quantization_numbers(self):
        """
        Returns a list of the compression factors of the images.

        @type self: Model Object
        @rtype: List[Floats]
            returns the list of all compression factors.
        """
        return self.quantization_numbers

    def run_analysis(self, cutoff=0.05, cfactor=2):
        """
        Investigates the quality of the image based off the compression factor.

        @type self: Model 
            Model object used to run the analysis of the compressed images.
        @type cutoff: Float
            percentage value used to indicate residual cutoff.
        @rtype: None
        """
        valid_cfactors = {}
        for compressed_image in self.compressed_images:
            if np.all(np.abs(compressed_image.get_data(version='residual')) < cutoff) \
                and compressed_image.get_compressed_factor() >= cfactor:
                valid_cfactors[compressed_image] = compressed_image.get_compressed_factor()

        print("Balco has found a total of", str(len(valid_cfactors)), "acceptable images.")
        
        number = 1
        for image in valid_cfactors:
            print(str(number) + ") " + image.get_name(version='compressed') + ": " + str(valid_cfactors[image]))
            number += 1

        print("\n Read this as:")
        print(" Algorithm -- Quantization Number -- Image Name: Compression Factor ")

        # Also to look at. Regions where maximal difference is lower than the cutoff, but 
        # investigate overall difference around the image.
        # Return regions where differences are more than a certain percentage higher but still
        # lower than the cutoff.          
        # Code ---->
        # To do....
        # Look into the PSD of the images.
        return valid_cfactors

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
        factors = self.get_compressed_factors()
        
        plt.figure(figsize=(9, 6))
        plt.title("Residual (Max & Min Values) vs. Compression Factor")
        plt.plot(factors, max_residuals, label="Max", linestyle="None", marker='.')
        plt.plot(factors, min_residuals, label='Min', linestyle="None", marker='+')
        plt.xlabel("Compression Factor")
        plt.ylabel("Residual")
        plt.legend()
        plt.show()

    def show_residual_vs_quantization_number(self):
        """
        Shows the relationship between the residual of the images vs.
        the quantization number used.

        @type self: Model
        @rtype: None
            Displays an interactive Matplotlib figure.
        """
        max_residuals = [np.max(np.abs(image.get_data(version='residual'))) for image in self.compressed_images]
        min_residuals = [np.min(np.abs(image.get_data(version='residual'))) for image in self.compressed_images]
        factors = self.get_quantization_numbers()
        
        plt.figure(figsize=(9, 6))
        plt.title("Residual (Max & Min Values) vs. Quantization Number")
        plt.plot(factors, max_residuals, label="Max", linestyle="None", marker='.')
        plt.plot(factors, min_residuals, label='Min', linestyle="None", marker='+')
        plt.xlabel("Quantization Number")
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
        factors = self.get_compressed_factors()

        plt.figure(figsize=(9, 6))
        plt.title("PSD Residual (Max & Min values) vs. Compression Factor")
        plt.plot(factors, max_residuals, label="Max", linestyle="None", marker='x')
        plt.plot(factors, min_residuals, label='Min', linestyle="None", marker='+')
        plt.xlabel("Compression Factor")
        plt.ylabel("Frequency [Hz]")
        plt.legend()
        plt.show()

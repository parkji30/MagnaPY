import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from astropy.io import fits

class ArrayND:
    def __init__(self, data, compressed_data, image_name, comp_image_name, cfactor=0, info=''):
        """
        @type self: Image
        
        @type data: Numpy Array (2D) 
            Image represented by its 2D pixel values

        @type compressed_data: Numpy Array (2D) 
            Compressed Image represented by its 2D pixel values

        @type image_name: String
            The name of the original image.

        @type comp_image_name: String
            The name of the compressed image.

        @type cfactor: Float
            The compression factor of the compressed image from 
            it's original image.

        @type info:
            Information of the image containing it's header.
        """
        self.original_data = data
        self.data_modified = np.copy(self.original_data)
        self.compressed_data = compressed_data
        self.compressed_factor = round(cfactor, 4)

        self.image_name = image_name
        self.comp_image_name = comp_image_name
        self.info = info
    
    def __repr__(self):
        """
        Representation of this python object when called upon.

        @type self: Balco
        @rtype: String
            When this object is called, it will be represented
            by it's compressed name.
        """
        return self.get_name(version="compressed")

    def __str__(self):
        """
        Representation of this python object when used as a string.

        @type self: Balco
        @rtype: String
            When this object is used as a string, it will be
            represented by it's compressed name.
        """
        return self.get_name(version="compressed")

    def median_reduction(self):
        """
        Median reduction of the original image. 

        Typically used in situations where a major portion of the image
        is dark empty space.
            e.g. Super/Giga BIT images.

        @type self: Image
        @rtype: Numpy Array(2d) 
            Image represented by its 2D pixel values
        """
        self.data_modified = self.original_data - np.median(self.original_data)

    def flat_field_reduction(self):
        """
        Flat field reduction of image to account for faulty light measurement
        across camera

        @type self: Image
        @rtype: Numpy Array(2d) 
            Image represented by its 2D pixel values
        """
        pass
    
    def get_compressed_factor(self):
        """
        Returns the compression factor of the compressed Image.

        @type self: Float
            Returns the compression factor 
        """
        return self.compressed_factor

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

    def get_name(self, version='original'):
        """
        Returns the Image name of the desired version.

        @type self: Image
        
        @type version: String
            1) Original displays the original image. 
            2) Compressed displays the compressed image.

        @rtype: String
            Returns the name of the version of the image.
        """
        if version.lower() == 'original':
            return self.image_name
        elif version.lower() == 'compressed':
            return self.comp_image_name

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

    def save_image(self, directory):
        """
        Saves the compressed image in the specified directory.

        @type self: Image 

        @type directory: String
            Directory to save this image.

        @rtype: None
            Saves this image to designated directory.
        """
        fits.writeto(directory + self.comp_image_name, self.compressed_data, overwrite=True)
        
    def Im_show(self, version="original"):
        """
        Displays a matplotlib image.

        @type self: Model

        @type version: String
            1) Original obtains the original image. 
            2) Compressed obtains the compressed image.
            3) Difference obtains original subtracted by the compressed image.

        @rtype: None
            Displays the version of the selected image as a matplotlib object.
        """
        plt.figure(figsize=(7, 7))
        if version.lower() == "original":
            plt.title("Original " + self.image_name)
            plt.imshow(self.original_data)
        elif version.lower() == 'compressed':
            plt.title("Compressed " + self.image_name)
            plt.imshow(self.compressed_data)
        elif version.lower() == 'residual':
            plt.title("Residual (Max & Min Value) " + self.image_name)
            plt.imshow(np.max(self.original_data) - np.max(self.compressed_data), label='Max Value Residual')
            plt.imshow(np.min(self.original_data) - np.min(self.compressed_data), label='Min Value Residual')
        plt.colorbar()
        plt.show()

    def Im_show_psd(self):
        """
        Power Spectrum Analysis of array.

        To be implemented in child classes.

        @type self: Array
        @rtype: None
            Displays the PSD of the array.
        """
        pass
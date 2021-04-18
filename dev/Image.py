import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class Image:
    def __init__(self, data, compressed_data, image_name, comp_image_name, info=''):
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

        @type info:
            Information of the image containing it's header.
        """
        self.original_data = data
        self.data_modified = np.copy(self.original_data)
        self.compressed_data = compressed_data

        self.image_name = image_name
        self.comp_image_name = comp_image_name
        self.info = info

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

    def get_mms(self, version='original'):
        """
        Returns the mean, median, standard deviation of the input image.

        @type self: Model
        @type original_view: Boolean (Display the original or compressed Image)
        """
        original = self.original_data
        compressed = self.compressed_data

        if version.lower()=='original':
            return [np.mean(original), np.median(original), np.std(original)]
        else:
            return [np.mean(compressed), np.median(compressed), np.std(compressed)]

    def get_name(self, version='original'):
        """
        Returns the image name of the desired version.

        @type self: Image
        @type version: String
            Version of the image name to be returned.
        @rtype: None
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
            Version of the image data to be returned.
        @rtype: None
        """
        if version.lower() == 'original':
            return self.original_data
        elif version.lower() == 'compressed':
            return self.compressed_data

    def save_image(self, directory):
        """
        Saves the image in a specified directory.

        @type self: Image 
        @type directory: String
            New pathing to save this image object.
        """
        pass

    def Im_show(self, version="original"):
        """
        Displays the image. 3 Options to choose from.

            1) original
            2) compressed
            3) difference

        @type self: Model
        @rtype: None
        """
        plt.figure(figsize=(7, 7))
        if version.lower() == "original":
            plt.title("Original " + self.image_name)
            plt.imshow(self.original_data)
        elif version.lower() == 'compressed':
            plt.title("Compressed " + self.image_name)
            plt.imshow(self.compressed_data)
        elif version.lower() == 'difference':
            plt.title("Residual " + self.image_name)
            plt.imshow(self.original_data - self.compressed_data)
        plt.colorbar()
        plt.show()

    def Im_show_psd_1D(self, version='original', freq_scale=1):
        """
        Displays the 1D power spectrum density of this image.

        @type self: Image
        @rtype: None
            Shows PSD figure of the image (1D).
        """
        original = self.original_data
        compressed = self.compressed_data

        # Assume 1D
        try:
            plt.figure(figsize=(7, 7))
            plt.title("Power Spectral Density " + version)
            if version.lower() == 'original':
                freqs, psd = signal.welch(original)
                plt.semilogx(freqs * freq_scale, psd)
            elif version.lower() =='compressed':
                freqs, psd = signal.welch(compressed)
                plt.semilogx(freqs * freq_scale, psd)
            elif version.lower() == 'difference':
                freqs, psd = signal.welch(original - compressed)
                plt.semilogx(freqs * freq_scale, psd)
            plt.colorbar()
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Power [Units]")
            plt.show()
        except:
            print("1D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")
    
    def Im_show_psd_2D(self, version='original', freq_scale=1):
        """
        Displays the 2D power spectrum density of this image.

        @type self: Image
        @rtype: None
            Shows PSD figure of the image (2D).
        """
        original = self.original_data
        compressed = self.compressed_data

        # Assume 2D
        try:
            plt.figure(figsize=(7, 7))
            plt.title("Power Spectral Density " + version)
            if version.lower() == 'original':
                fft = np.fft.fft2(original)
                p2d = np.power(np.abs(fft) * freq_scale, 2) 
                plt.imshow(np.fft.fftshift(np.log10(p2d)))
            elif version.lower() =='compressed':
                fft = np.fft.fft2(compressed)
                p2d = np.power(np.abs(fft) * freq_scale, 2)
                plt.imshow(np.fft.fftshift(np.log10(p2d)))
            elif version.lower() == 'difference':
                fft = np.fft.fft2(original-compressed)
                p2d = np.power(np.abs(fft) * freq_scale, 2)
                plt.imshow(np.fft.fftshift(np.log10(p2d)))
            plt.colorbar()
            plt.show()
        except:
            print("2D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")

   
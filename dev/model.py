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
    def __init__(self, data, compressed_data, title=''):
        """
        @type self: Model
        @type image_structure: ImageStructure Object
                As defined in the code within the file.
        """
        self.original_images = []
        self.compressed_images = []
        
        self.data = data
        self.compressed_data = compressed_data
        self.title = title

    def Im_show(self, version="original"):
        """
        Displays the original Image

        @type self: Model
        """
        
        plt.figure(figsize=(7, 7))
        if version.lower() == "original":
            plt.title("Original " + self.title)
            plt.imshow(self.data)
        elif version.lower() == 'compressed':
            plt.title("Compressed " + self.title)
            plt.imshow(self.compressed_data)
        elif version.lower() == 'difference':
            plt.title("Residual " + self.title)
            plt.imshow(self.data - self.compressed_data)
        plt.colorbar()
        plt.show()

    def Im_show_psd_1D(self, version='original', freq_scale=1):
        """
        Displays the 1D power spectrum density of the given image.

        @type self: Model
        @rtype: None
            Shows PSD figure of the image (1D).
        """
        original = self.data
        compressed = self.compressed_data

        # Assume 1D
        try:
            plt.figure(figsize=(7, 7))
            plt.title("Power Spectral Density " + version)
            if version.lower() == 'original':
                freqs, psd = signal.welch(original)
                plt.semilogx(freqs*freq_scale, psd)
            elif version.lower() =='compressed':
                freqs, psd = signal.welch(compressed)
                plt.semilogx(freqs*freq_scale, psd)
            elif version.lower() == 'difference':
                freqs, psd = signal.welch(original - compressed)
                plt.semilogx(freqs*freq_scale, psd)
            plt.colorbar()
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Power [Units]")
            plt.show()
        except:
            print("1D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")
    
    def Im_show_psd_2D(self, version='original', freq_scale=1):
        """
        Displays the 2D power spectrum density of the given image.

        @type self: Model
        @rtype: None
            Shows PSD figure of the image (2D).
        """
        original = self.data
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
            print("1D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")
            

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

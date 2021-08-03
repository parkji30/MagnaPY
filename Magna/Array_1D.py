from Array import ArrayND
from scipy import signal

class Array1D(ArrayND):
    def __init__(self, data, compressed_data, image_name, comp_image_name, cfactor=0, info=''):
        super(Array1D, self).__init__(data, compressed_data, image_name, comp_image_name, cfactor, info)

        self.original_psd, self.original_freqs = signal.welch(data)
        self.compressed_psd, self.compressed_freqs = signal.welch(compressed_data)

    def Im_show_psd(self, version='original', freq_scale=1):
        """
        Displays the 1D power spectrum density of this image.

        @type self: Image
        @rtype: None
            Shows PSD figure of the image (1D).
        """
        try:
            plt.figure(figsize=(7, 7))
            plt.title("Power Spectral Density " + version)
            if version.lower() == 'original':
                plt.semilogx(self.original_freqs * freq_scale, self.original_psd)
            elif version.lower() =='compressed':
                plt.semilogx(self.compressed_freqs * freq_scale, self.compressed_psd)
            elif version.lower() == 'residual':
                plt.semilogx(self.original_freqs-self.compressed_freqs, self.original_psd - self.compressed_psd)
            plt.colorbar()
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Power [Units]")
            plt.show()
        except:
            print("1D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")
    
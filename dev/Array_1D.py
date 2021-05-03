class Array_1D(Array):
    
    def __init__(self, data, compressed_data, image_name, comp_image_name, cfactor=0, info=''):
        Array.__init__(data, compressed_data, image_name, comp_image_name, cfactor, info)

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
            elif version.lower() == 'residual':
                freqs, psd = signal.welch(original - compressed)
                plt.semilogx(freqs * freq_scale, psd)
            plt.colorbar()
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Power [Units]")
            plt.show()
        except:
            print("1D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")
    
class Array_2D(Array):
    """
    Child class of the general Array class.

    This class object is used to handle 2 dimensional Array data.
    """
        
    def __init__(self, data, compressed_data, image_name, comp_image_name, cfactor=0, info=''):
        Array.__init__(data, compressed_data, image_name, comp_image_name, cfactor, info)

    def Im_show_psd_2D(self, version='original', freq_scale=1):
        """
        Displays the 2D power spectrum density of this image.

        @type self: Image

        @type version: String
            1) Original obtains the original image. 
            2) Compressed obtains the compressed image.
            3) Difference obtains original subtracted by the compressed image.

        @type freq_scale: Float
            Number to scale the frequency values by.

        @rtype: None
            Displays the version of the selected image as a matplotlib object.
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
            elif version.lower() == 'residual':
                fft = np.fft.fft2(original-compressed)
                p2d = np.power(np.abs(fft) * freq_scale, 2)
                plt.imshow(np.fft.fftshift(np.log10(p2d)))
            plt.colorbar()
            plt.show()
        except:
            print("2D PSD failed... probably dimensional error. Your image has " + str(original.ndim) + " dimensions")
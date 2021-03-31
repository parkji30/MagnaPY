from astropy.io import fits

class Compression:
    """
    The compression object class that determines what compression 
    algorithm will be used.
    """

    def __init__(self, compression_type, data=None, factor=2):
        """
        @type self: Compression Object

        @type compresson_type: String 
            Compression Algorithm to be used)

        @type image_structure: ImageStructure Object

        @type factor: Integer 
            desired compression factor, particularily used with 
            HCompression or used as a quantization factor.

        Acceptable parameters of compression_type:
            1) Hcomp
            2) Gzip
            3) Rice
            4) BitShave
        """
        self.compression_algorithm = compression_type
        self.data = data[0].data
        self.scale_factor = factor

    def compress(self):
        """
        The compress method which compresses the image file based on the 
        algorithm specified.
        
        @type self: Compression Object
        """     
        algorithm_dict = {
            'hcomp': "HCOMPRESS_1",
            'gzip': "GZIP_1",
            'rice': "RICE_1"
        } 
        
        # selected_algorithm = algorithm_dict[self.compression_algorithm]
        try:
            selected_algorithm = algorithm_dict[self.compression_algorithm]
        except:
            return("Could not find Algorithm. Check your spelling?")

        # print(self.data)
        # Specific Case of H Compression
        dt = fits.CompImageHDU(data=self.data, compression_type = "RICE_1")
        return dt
        
        # if selected_algorithm == 'HCOMPRESS_1':
        #     return fits.CompImageHDU(data=self.data, compression_type = "HCOMPRESS_1", \
        #     hcomp_scale=self.scale_factor, hcomp_smooth = 1)
        # # Specific Case of Bit Shaving
        # elif selected_algorithm == 'Bitshave':
        #     pass
        # else:
        #     return fits.CompImageHDU(data=self.data, compression_type = selected_algorithm) 

         
    def uncompress(self):
        """
        Uncompresses the astropy fits object.
        
        @type self: Compression
        @rtype: Numpy array (2D)
            The uncompressed image.
        """
        dt = fits.CompImageHDU(data=self.data, compression_type = "RICE_1")
        return dt
        
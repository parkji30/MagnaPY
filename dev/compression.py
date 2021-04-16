from astropy.io import fits
import numpy as np
from Model import Model
import os

class Compression:
    """
    The compression object class that determines what compression
    algorithm will be used.
    """

    def __init__(self, data=None, factor=2, compressed_name='comp.fits'):
        """
        @type self: Compression Object

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
        self.data = data
        self.quantize_factor = factor
        self.compressed_name = compressed_name

    def valid_extension(self):
        """
        Checks to see if the image extension is compressible with current
        Implementation of Balco.

        @type self: Compression
        @type image: Numpy Array (2d)
        @rtype: Boolean
            Returns true if image is compressible. False otherwise.
        """

        name, extension = os.path.splitext(self.compressed_name)
        KNOWN_EXTENSIONS = ['.jpg', '.png', '.fits', '.jpeg']

        if extension in KNOWN_EXTENSIONS:
            return True
        else:
            return False

    def compress(self, algorithm):
        """
        Compressed data packet using the H Transformation method and saves it
        into a fits file.

        Compression List -> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']

        @type self: Compression
        @rtype: None
        """
        if self.valid_extension():
            if algorithm =="HCOMPRESS_1":
                fits.CompImageHDU(self.data, compression_type = algorithm, \
                hcomp_scale=self.quantize_factor).writeto(algorithm + "_" + self.compressed_name, overwrite=True)
                print("Hcompress!")

            else:
                fits.CompImageHDU(self.data, compression_type = algorithm, \
                quantize_level=self.quantize_factor).writeto(algorithm + "_" + self.compressed_name, overwrite=True)
                print(algorithm + " Compress!")

    def optimize(self):
        """
        Selects the most optimal compression algorithm to be used for given
        science image.

        TODO- implement libpolycomp for fitting compression.

        @type self: Compression
        @rtype: None
        """
        model_list = []
        if self.valid_extension():
            try:
                self.compress(algorithm='HCOMPRESS_1')
                compressed_image = fits.getdata(self.compressed_name)
                model_1 = Model(self.data, compressed_image, title=self.compressed_name)
                model_list.append(model_1.return_difference())
            except:
                return("The H-Compression Failed...")

            try:
                self.compress(algorithm='RICE_1')
                compressed_image = fits.getdata(self.compressed_name)
                model_2 = Model(self.data, compressed_image, title=self.compressed_name)
                model_list.append(model_2.return_difference())
            except:
                return("The RICE Compression Failed...")

            try:
                self.compress(algorithm='PLIO_1')
                compressed_image = fits.getdata(self.compressed_name)
                model_3 = Model(self.data, compressed_image, title=self.compressed_name)
                model_list.append(model_3.return_difference())
            except:
                return("The PLIO Compression Failed...")

            try:
                self.compress(algorithm='GZIP_1')
                compressed_image = fits.getdata(self.compressed_name)
                model_4 = Model(self.data, compressed_image, title=self.compressed_name)
                model_list.append(model_4.return_difference())
            except:
                return("The GZIP Compression Failed...")





from astropy.io import fits
from astropy.io.fits.hdu import compressed
import numpy as np
import os, shutil

class Compression:
    """
    The compression object class that determines what compression
    algorithm will be used.
    """
    def __init__(self, path, textfile='default.txt'):
        """
        """
        self.directory_path
        self.info_textfile = textfile

    def compress(self, data, algorithm='HCOMPRESS_1', file_name='default', qf=1):
        """
        """
        compressed_name = algorithm+'_' + str(qf)+'_' + file_name
        fits.CompImageHDU(data, compression_type=algorithm, \
                hcomp_scale=qf).writeto(self.compressed_directory_path+compressed_name, overwrite=True)

        return compressed_name


    def multi_compress(self, image):
        """
        runs multiple compression algorithms on one data set and returns an array to compare the reults
        """

        algorithms = ['HCOMPRESS_1', 'RICE_1']

        for alg in algorithms:
            fits.CompImageHDU(data, compression_type=alg).writeto(self.compressed_directory_path \
            + compressed_name, overwrite=True)

        # get data


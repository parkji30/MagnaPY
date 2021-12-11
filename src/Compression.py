from astropy.io import fits
from astropy.io.fits.hdu import compressed
from real_time_writer import RealTimeWriter
import numpy as np
import os, shutil

ALGORITHMS = ['HCOMPRESS_1', 'RICE_1']

class Compression:
    """
    The compression object class that determines what compression
    algorithm will be used.
    """
    def __init__(self, path, textfile='default.txt'):
        """
        """
        self.directory_path = path
        self.info_textfile = textfile


    def update_compression_path(self, new_path):
        """
        Updates the directory pathing for new files to be compressed.
        """
        self.directory_path = new_path


    def compress(self, data, algorithm='HCOMPRESS_1', file_name='default', qf=1):
        """
        """
        compressed_name = algorithm+'_' + str(qf)+'_' + file_name
        fits.CompImageHDU(data, compression_type=algorithm, \
                hcomp_scale=qf).writeto(self.compressed_directory_path+compressed_name, overwrite=True)

        return compressed_name


    def multi_compress(self, image_name):
        """
        runs multiple compression algorithms on one data set and returns an array to compare the reults
        """

        data = fits.getdata(image_name)[0].data

        for alg in ALGORITHMS:
            results = []
            fits.CompImageHDU(data, compression_type=alg)
                .writeto(self.compressed_directory_path + image_name + alg, overwrite=True)



        # get data


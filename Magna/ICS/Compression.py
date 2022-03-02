from astropy.io import fits
from astropy.io.fits.hdu import compressed
# from real_time_writer import RealTimeWriter
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
                hcomp_scale=qf).writeto(self.directory_path + compressed_name, overwrite=True)

        return compressed_name


    def multi_compress(self, image_name, image_data):
        """
        runs multiple compression algorithms on one data set and returns an array to compare the reults
        """

        # data = fits.getdata(image_name)[0].data

        # Compress the files
        for alg in ALGORITHMS:
            results = []
            fits.CompImageHDU(image_data, compression_type=alg) \
                .writeto(self.directory_path + alg + '_' + image_name, overwrite=True)

        # Get compressed information and write into text file.
        compressed_images = os.listdir(self.directory_path)
        for compressed_image in compressed_images:
            if compressed_image.lower() == ".ds_store":
                pass
            else:
            # print('your comp images'+compressed_image)
                print(compressed_image)
                print(fits.getdata(self.directory_path+compressed_image))




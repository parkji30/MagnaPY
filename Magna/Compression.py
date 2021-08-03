from astropy.io import fits
import numpy as np
from Array_1D import Array1D
from Array_2D import Array2D  
import os, shutil

class Compression:
    """
    The compression object class that determines what compression
    algorithm will be used.
    """
    def __init__(self, comp_dir_path, textfile='default.txt'):
        """
        """
        self.compressed_directory_path = comp_dir_path
        self.text_file = textfile
        
    def update_save_directory(self, new_directory):
        """
        Updates the new save directory.
        
        @type self: Compression
        @type new_directory: Strong
            Pathing to the new directory for saving the compressed images.
        @rtype: None
        """
        self.save_directory = new_directory

    def clean_save_directory(self):
        """
        Empties the save directory.

        @type self: Compression
        @rtype: None
        """
        folder = self.save_directory
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    def valid_extension(self,file):
        """
        Checks to see if the image extension is compressible with current
        Implementation of Balco.

        @type self: Compression
        @type image: Numpy Array (2d)
        @rtype: Boolean
            Returns true if image is compressible. False otherwise.
        """
        name, extension = os.path.splitext(file)
        KNOWN_EXTENSIONS = ['.jpg', '.png', '.fits', '.jpeg']

        if extension in KNOWN_EXTENSIONS:
            return True
        else:
            return False

    def compress(self, file, algorithm='HCOMPRESS_1', qf=1):
        """
        """
        original_data = fits.getdata(file)
        if original_data.ndim < 2 and algorithm=='HCOMPRESS':
            print("Incompatible Dimensions")
            return 0
        
        if self.valid_extension(file):
            compressed_name = algorithm+'_'+str(qf)+'_'+file
            fits.CompImageHDU(original_data, compression_type=algorithm, \
                hcomp_scale=qf).writeto(self.compressed_directory_path+compressed_name, overwrite=True)

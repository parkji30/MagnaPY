from astropy.io import fits
import numpy as np
from Model import Model
from Image import Image
import os, shutil

class Compression:
    """
    The compression object class that determines what compression
    algorithm will be used.
    """
    def __init__(self, data, image_name, file_size):
        """
        Initializes a new compression object from 4 differnt algorithms 
        to choose from.

        Valid algorithms to choose from are:
            Compression List -> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
        All of which can be used by the optimize() and compress() methods.

        @type data: Numpy Array (2D)
            Pixel values of the image.
        
        @type image_name: String
            Image name that will be compressed.

        @type self: Compression Object
        """
        self.original_data = data
        self.image_name = image_name
        self.original_size = file_size

        self.compressed_directory = []
        self.save_directory = '../comp_images'

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
    
    def valid_extension(self):
        """
        Checks to see if the image extension is compressible with current
        Implementation of Balco.

        @type self: Compression
        @type image: Numpy Array (2d)
        @rtype: Boolean
            Returns true if image is compressible. False otherwise.
        """
        name, extension = os.path.splitext(self.image_name)
        KNOWN_EXTENSIONS = ['.jpg', '.png', '.fits', '.jpeg']

        if extension in KNOWN_EXTENSIONS:
            return True
        else:
            return False

    def compress(self, algorithm, quantize_factor=2):
        """
        Compressed data packet using the H Transformation method and saves it
        into a fits file.

        @type self: Compression
            Compression List ---> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
        @type factor: Integer
            desired compression factor, particularily used with
            HCompression or used as a quantization factor.
        @rtype: None
        """
        compressed_name = algorithm + "_" + str(round(quantize_factor, 3)) +  "_" + self.image_name

        if self.valid_extension():
            if algorithm =="HCOMPRESS_1":
                fits.CompImageHDU(self.original_data, compression_type=algorithm, \
                hcomp_scale=quantize_factor).writeto(self.save_directory + compressed_name, overwrite=True)
                self.image_compressed_name = compressed_name
            else:
                fits.CompImageHDU(self.original_data, compression_type = algorithm, \
                quantize_level=quantize_factor).writeto(self.save_directory + compressed_name, overwrite=True)
                self.image_compressed_name = compressed_name

    def optimize(self, algorithm='HCOMPRESS_1', compression_range=(1, 2), iterations=4):
        """
        Selects the most optimal compression algorithm to be used for given
        science image.

        TODO- implement libpolycomp for fitting compression.

        @type self: Compression
        @type algorithm: String
            The desired compression algorithm to be used.
            Compression List ----> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
        @type compression_range: Tuple(Float, Float)
            Range of compression factors from min to max 
        @type iterations:
            compression factor forward steps.
        @rtype: None
        """
        factors = np.linspace(compression_range[0], compression_range[1], iterations)
        if self.valid_extension():
            for factor in factors:
                self.compress(algorithm=algorithm, quantize_factor=factor)
            
            #Figure out a way to get a list of all the compressed images.
            compressed_images = os.listdir(self.save_directory)
            compressed_images.sort()
            self.compressed_directory = compressed_images
            model = Model(image_name = self.image_name, quantization_numbers=factors)

            for comp_image in self.compressed_directory:
                comp_file_size = os.path.getsize(self.save_directory + comp_image)
                compressed_image_data = fits.getdata(self.save_directory + comp_image)
                model.update_compressed_list(Image(data = self.original_data,
                                                    compressed_data = compressed_image_data,
                                                    image_name = self.image_name,
                                                    comp_image_name = comp_image,
                                                    cfactor = self.original_size/comp_file_size))

            # Have the model run it's analysis for its compressed images...
            compression_images = model.run_analysis()

            model.show_residual_vs_compression_factor()
            model.show_residual_PSD_vs_compression_factor() 
            model.show_residual_vs_quantization_number()
            
            # finalize = int(input("Enter option number: "))
            selected_image = compression_images[-1]
            print("Your selected image is: ", selected_image)
            print("The compression factor is: ", str(selected_image.get_compressed_factor()), '\n')

            # Removes all other images, but the best version.
            return selected_image
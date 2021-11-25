import os
from Compression import Compression
from Array import Array
from astropy.io import fits

# 1) Load directory full of images
dir = '/Users/a16472/Desktop/MagnaPY/TestImages'

os.chdir(dir)
images = os.listdir()

# 2) Run several Compression methods on each image
compressor = Compression(dir)

image_analysis_list = []

for image_name in images:
    image_data = fits.load(image_name)[0].data
    compression_results = Compression.multi_compress(image_data)
    image_array = Array(image_name, image_data)
    image_array.update_compressed_data_dictionary(compression_results)
    image_analysis_list.append(image_array)


# 3) Return a text file that has information regarding the compression




# 4)
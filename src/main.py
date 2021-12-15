import os
from Compression import Compression
# from Array import Array
from astropy.io import fits

## Loading Directory
# 1) Load directory full of images

import os

dir = '/Users/a16472/Desktop/MagnaPY/TestImages/'
compression_directory = '/Users/a16472/Desktop/MagnaPY/compressed/'

os.chdir(dir)
images = os.listdir()
print(images)


## Running Compression

# 2) Run several Compression methods on each image
compressor = Compression(path=compression_directory)
image_analysis_list = []

for name in images:
    image_data = fits.open(name)[0].data
    compressor.multi_compress(image_name=name, image_data=image_data)
    # image_array = Array(image_name, image_data)
    # image_array.update_compressed_data_dictionary(compression_results)
    # image_analysis_list.append(image_array)


## Update text file for compression

# 3) Return a text file that has information regarding the compression



## Finalize compression information.

# 4)
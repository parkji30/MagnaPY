import os

os.chdir("/Users/a16472/desktop/temp_balco")

## Load Packages
from Compression import Compression
from Model import Model
from astropy.io import fits

original_images = './images/'
comp_images = './comp_images/'

original_image = fits.open('/Users/a16472/Desktop/temp_balco/original_images/L1M10_0.fits')[0].data

## Compress
# Compression List -> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
algorithm = 'HCOMPRESS_1'
compressor = Compression(data=original_image, image_name="L1M10.fits")
compressor.update_save_directory("/Users/a16472/desktop/temp_balco/comp_images/")

compressor.optimize(algorithm="HCOMPRESS_1", compression_range=(0, 10), iterations=20)
compressed_image = fits.getdata(compressor.save_directory + compressor.get_compressed_name())

## Model
model = Model(original_image, compressed_image, title="L1M10_0")

model.Im_show(version='original')
model.Im_show(version='compressed')
# model.Im_show(version='compressed')
# model.Im_show(version="difference")

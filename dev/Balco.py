import os

os.chdir("/Users/a16472/desktop/temp_balco")

## Load Packages
from Compression import Compression
from Model import Model
from astropy.io import fits

original_images = './images/'
comp_images = './comp_images/'

original_image = fits.open('/Users/a16472/Desktop/temp_balco/images/L1M10_0.fits')[0].data

## Compress
# Compression List -> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
algorithm = 'GZIP_2'
compressor = Compression(original_image, factor=100, compressed_name="L1M10.fits")
compressor.compress(algorithm)
compressed_image = fits.getdata(algorithm + "_" + "L1M10.fits")

## Model
model = Model(original_image, compressed_image, title="L1M10_0")

model.Im_show_original()
model.Im_show_compressed()
model.Im_show_difference()
print(model.get_mms())
print(model.get_mms(False))
print(model.return_difference())


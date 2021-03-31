import os

os.chdir("/Users/a16472/desktop/balco/dev/")

from image_structure import ImageStructure
from compression import Compression
from model import Visualizer

from astropy.io import fits

images_path = './images/'

# def main():
# Load images here

# image_fits = input("Input Image Name: ")
image_fits = fits.open('/Users/a16472/Desktop/Balco/src/VelaC_500_intermediate_regrid_30as_pix_var_ang.fits')
# algorithm = input("Desired Compression Algorithm?: ")
algorithm = 'hcomp'

compressor = Compression(algorithm, image_fits)
image_object = ImageStructure(image_fits, compressor)
image_object.compress_data()

vis = Visualizer(image_object = image_object)

vis.Im_show()
vis.Im_show_compressed()

# main()

import os

os.chdir("/Users/a16472/desktop/balco/dev/")

from image_structure import ImageStructure
from compression import Compression
from model import Model

from astropy.io import fits

images_path = './images/'

def main():
    # Load images here

    # image_fits = input("Input Image Name: ")
    image_fits = fits.open('/Users/a16472/Desktop/Balco/src/VelaC_500_intermediate_regrid_30as_pix_var_ang.fits')
    # algorithm = input("Desired Compression Algorithm?: ")
    algorithm = 'hcomp'

    compressor = Compression(algorithm)
    image_object = ImageStructure(image_fits, compressor)
    image_object.compress_data()

    model = Model(image_object = image_object)

    model.Im_show()

main()

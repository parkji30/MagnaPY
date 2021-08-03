## Load Packages
import os, shutil
from Compression import Compression
from astropy.io import fits
import sys
import time

main_path = "/Users/a16472/Desktop/Balco 2/Magna/"
og_image_path = "/Users/a16472/Desktop/Balco 2/Magna/Original/"
comp_image_path = "/Users/a16472/Desktop/Balco 2/Magna/Compressed/"

compression_algorithm = 'HCOMPRESS_1'

try:
    while True:
        time.sleep(1)
        print("Magna is Running...")
        os.chdir(og_image_path)
        file_names = os.listdir(og_image_path)

        for name in file_names:
            compressor = Compression(comp_dir_path=comp_image_path)
            compressor.compress(file=name, algorithm=compression_algorithm)
except Exception as err:
    exception_type = type(err).__name__
    print(exception_type)
    print("Magna is now Exiting.")


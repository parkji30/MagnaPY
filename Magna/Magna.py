## Load Packages
import os, shutil
from Compression import Compression
from Model import LossModel
from Array import ArrayND
from astropy.io import fits
import sys
import time

main_path = "/Users/a16472/Desktop/Balco 2/Magna/"
orig_image_path = "/Users/a16472/Desktop/Balco 2/Magna/Original/"
comp_image_path = "/Users/a16472/Desktop/Balco 2/Magna/Compressed/"

compression_algorithm = 'HCOMPRESS_1'

loss_model = LossModel(main_path+'default.txt')
try:
    while True:
        time.sleep(1)
        print("Magna is Running...")
        os.chdir(orig_image_path)
        file_names = os.listdir(orig_image_path)
        print(file_names)
        for name in file_names:
            compressor = Compression(comp_dir_path = comp_image_path)
            compressed_file = compressor.compress(file = name, algorithm = compression_algorithm)
            temp_array = ArrayND(original_image = name, compressed_image_path = comp_image_path + compressed_file)
            loss_model.update_array_list(temp_array)
            loss_model.write_info(temp_array)
      
except Exception as err:
    exception_type = type(err).__name__
    print(err)
    print("Magna is now Exiting.")

print(loss_model.image_arrays)
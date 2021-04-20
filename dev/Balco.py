import os, shutil

## Delete the compression folder each time we run.
os.chdir("/Users/a16472/desktop/temp_balco")
folder = "/Users/a16472/desktop/temp_balco/comp_images"
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

## Load Packages
from Compression import Compression
from Model import Model
from astropy.io import fits

original_images = './images/'
comp_images = './comp_images/'

# c_list = ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
# try:
#     algorithm = sys.argv[-2]
#     q_factor = float(sys.argv[-1])
# except:
#     print("Something went wrong...")
#     exit()

# if not algorithm in c_list:
#     print("Could not comprehend command, system exiting...")
#     exit()

original_image = fits.open('/Users/a16472/Desktop/temp_balco/original_images/L1M10_0.fits')[0].data

## Compress
# Compression List -> ['RICE_1', 'GZIP_1', 'GZIP_2', 'PLIO_1', 'HCOMPRESS_1']
algorithm = 'RICE_1'
compressor = Compression(data=original_image, image_name="L1M10.fits")
compressor.update_save_directory("/Users/a16472/desktop/temp_balco/comp_images/")
# compressor.compress(algorithm='RICE_1')
compressor.optimize(algorithm="HCOMPRESS_1", compression_range=(0, 10), iterations=20)

## Model
# model = Model(original_image, compressed_image, title="L1M10_0")
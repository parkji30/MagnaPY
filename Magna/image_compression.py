import os
import fitsio
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import math


OG_SOURCE = "/home/james/Desktop/sbit_compress_py/original"
COMP_SOURCE = "/home/james/Desktop/sbit_compress_py/compressed"
DS9 = "/home/james/Desktop/sbit_compress_py/ds9"
MAIN = "/home/james/Desktop/sbit_compress_py/"

class ImageCompression:
    """
    SuperBit_Compression is a class object that compresses an image using 
    bit shaving or the H-Transformation. Both compression algorithm can be 
    either lossless or lossy depending on the quantization factor.

    """
    def __init__(self, image_file, cat="", crop=False):
        """
        A SuperBit compression object which is used to compress an fits image 
        file. NOTE- the image must be a fits file in order for this program to
        properly run.

        Given that the borders of SuperBIT's images are somewhat useless, it is 
        safe to crop this region out. Hence, if crop is True, then the edges of 
        the image is trimmed off (APPROXIMATELY 50 PIXELS PER SIDE).
        
        Bit_reduction is how many bits we want to shave off the bottom of our image.
        image_file refers to the self.image_name of the fits image. The default 
        setting is set as 4, but this value can be set using the bit_shaving 
        method.
        
        H-Transformation is a 2D Wavelett transformation compression algorithm
        that can be both lossless or lossy. For most astronomical images, it was
        found that this algorithm is the optimal choice, yielding the greatest
        preservation of data to compression factor.
        
        The cat parameter takes the name of the test.cat file provided by 
        SExtractor. This test.cat file should contain the following 10 parameters:
                
        ###################################################################################################
        ##   1 FLUX_AUTO              Flux within a Kron-like elliptical aperture                [count] ##
        ##   2 X_IMAGE                Object position along x                                    [pixel] ## 
        ##   3 Y_IMAGE                Object position along y                                    [pixel] ##
        ##   4 A_IMAGE                Profile RMS along major axis                               [pixel] ##
        ##   5 B_IMAGE                Profile RMS along minor axis                               [pixel] ##
        ##   6 FLUX_RADIUS            Fraction-of-light radii                                    [pixel] ##
        ##   7 ELLIPTICITY            1 - B_IMAGE/A_IMAGE                                                ##
        ##   8 ELONGATION             A_IMAGE/B_IMAGE                                                    ##
        ##   9 ALPHA_J2000            Right ascension of barycenter (J2000)                      [deg]   ##
        ##  10 DELTA_J2000            Declination of barycenter (J2000)                          [deg]   ##
        ###################################################################################################
    
        If the parameters are not set as such, this program will fail to run.
    
        @type self: SuperBit_compression object
        @type image_file: String (Name of fits image)
        @type cat: String (Name of test.cat file from SExtractor)
        @rtype: None
        """
        self.bit_reduction = 4 # 4 is set to default unless specified otherwise
        self.hdu_list = fits.open(image_file)
        self.image_name = image_file
        self.original_image = np.round(self.hdu_list[0].data) #convert image to int values.
        
        if crop: # crop the edges of image
            self.original_image = self.crop()
        
        # Create a dictionary for header
        self.header = self.hdu_list[0].header
        keys = list(self.header.keys())
        dict = {}
        for key in keys:
            dict[key] = self.header[key]
        self.header = dict
        
        self.flags = []
        self.cookies = None
        
        # Median of the original image
        self.median = np.median(self.original_image)
        
        # Text Files contraing Sextractor Info On different Images
        self.SExtract_data = np.loadtxt(cat, comments="#")
        
        # Compressed Image
        self.compressed_image = self.original_image.copy()
        # H-Compress Image
        self.h_compress = self.original_image.copy()
        # Masked Image
        self.masked_image  = self.original_image.copy()
        
        # Number of sources for Big, Medium, Small size.
        self.c1 = self.c2 = self.c3 = 0

    def flag_stars(self):
        """
        Locates all the position of pixel values of that take up 2 bytes of memory
        and obtains their coordinates.
        
        @type self: SuperBIT_compression
        @rtype: None
        """
        pos = np.where(self.original_image > 255)
        flags = []
        for i in range(len(pos[0])):
            flags.append((self.original_image[pos[0][i]][pos[1][i]], pos[0][i], pos[1][i]))
        self.flags = flags
        
    def restore_flags(self, image):
        """
        Takes the stored coordinates of every 2 byte value pixel from the original
        image and restores these values back into the given image.
        
        @type self: SuperBit_Compression
        @rtype: None
        """
        for flag in self.flags:
            image[flag[1]][flag[2]]=flag[0]
        return image
        
    def crop(self):
        """
        Crops the image by shaving a width of 50 pixels from each side.
        
        @type matrix: Numpy Matrix
        @rtype: Numpy Matrix
        """
        return self.original_image[50:self.original_image.shape[0]-50, \
        50:self.original_image.shape[1]-50]
        
    def shown_region(self, x, y):
        """
        Displays a region of the image centred around the given x, y coordinate.
        
        @type self: SuperBit_Compression
        @type x_pos: Int
        @type y_pos: Int
        @rtype: None
        """
        a_size = b_size = 20
        left_x, right_x, up_y, down_y = self.square_cookie(a_size, b_size, int(x) , int(y))
        region = self.original_image[up_y:down_y, left_x:right_x]
        plt.figure(str(x) + ", " + str(y))
        plt.title(str(x) + ", " + str(y))
        max = np.mean(region) + np.std(region) * 1
        min = np.mean(region) - np.std(region) * 1
        plt.imshow(region, vmax=max, vmin=min)
        plt.colorbar()
        plt.show()
        
    def locate_wrappers(self):
        """
        There may be incidents where the image displays some arbitrarily large
        negative values. This is most likely due to a wrapping issue.
        
        This method is designed to locate each one and set those values to 0.
        
        @type self: SuperBit_Compression
        @rtype: None
        """
        x_pos, y_pos = np.where(self.compressed_image < 0)
        for i in range(len(x_pos)):
            self.compressed_image[x_pos[i]][y_pos[i]] = 0
    
    def square_cookie(self, a_size, b_size, x, y, masking=False):
        """
        A helper function used to cut a square cookie based on major and minor
        axis size of the respective source.
        
        @type self: SuperBit_Compression
        @type a_size: int
        @type b_size: int
        @type x: int
        @type y: int
        masking: Boolean
        @rtype: Tuple of ints
        """
        y_max = self.original_image.shape[0]
        x_max = self.original_image.shape[1]
        # square_size = (a_size + b_size) * 4
        
        # SMALL SOURCE #
        if a_size <= 1.2 and b_size <= 0.950:
            self.c1 +=1
            square_size = 3 # change this to 4
        # MEDIUM SOURCE #
        elif a_size > 10:
            #change this later
            square_size = 65
            self.c2 += 1
        # BIG SOURCE #
        else:
            #change this later
            square_size = 10
            self.c3 += 1
        left_x = right_x = 0
        up_y = down_y = 0
        
        if x - square_size < 0:
            left_x = 0
            right_x = int(x + square_size - (x - square_size))
        elif x + square_size > x_max: 
            left_x =  int(np.floor(x - (square_size) - (x + square_size - x_max))) 
            right_x = x_max 
        else:
            left_x = int(round(x - square_size))
            right_x = int(round(x + square_size))
            
        if y - square_size < 0:
            up_y = 0
            down_y = int(y + square_size - (y - square_size))
        elif y + square_size > y_max:
            up_y = int(np.floor(y - (square_size) - (y + square_size - y_max)))
            down_y = y_max 
        else:
            up_y = int(round(y - square_size))
            down_y = int(round(y + square_size))
        return(left_x, right_x, up_y, down_y)
        
    def cc_stars(self):
        """
        Locates the star position and cuts a square region around it, 
        maintaining all of its ORIGINAL pixels values.
        
        @type self: SuperBit_Compression
        @rtype: Numpy Array 
        """
        y_max = self.original_image.shape[0]
        x_max = self.original_image.shape[1]
        sext_data = self.SExtract_data
        regions = []
        
        if len(sext_data) == 10:
            star = sext_data
            flux = star[0]
            x = star[1]
            y = star[2]
            a_size = star[3]
            b_size = star[4]
            left_x, right_x, up_y, down_y = self.square_cookie(a_size, b_size, x, y)
            region = self.original_image[up_y:down_y, left_x:right_x]
            regions.append((region, x, y, a_size, b_size))
            self.cookies = regions
        else:
            for star in sext_data:
                flux = star[0]
                x = star[1]
                y = star[2]
                a_size = star[3]
                b_size = star[4]
                left_x, right_x, up_y, down_y = self.square_cookie(a_size, b_size, x , y)
                region = self.original_image[up_y:down_y, left_x:right_x]
                regions.append((region, x, y, a_size, b_size))
                self.cookies = regions
        
    def cc_restore_stars(self, algorithm):
        """
        Restores the cookie cut regions back to the compressed image with the
        ORIGINAL pixel values. 
        
        @type self: SuperBit_Compression
        @type image: Numpy Array
        @rtype: None
        """
        regions = []
        index = 0
        y_max = self.original_image.shape[0]
        x_max = self.original_image.shape[1]
        for star in self.cookies:
            cookie = star[0]
            x = star[1]
            y = star[2]
            a_size = star[3]
            b_size = star[4]
            
            left_x, right_x, up_y, down_y = self.square_cookie(a_size, b_size, x ,y)
            
            if algorithm.lower() == "hcomp":
                self.h_compress[up_y:down_y, left_x:right_x] = cookie
            elif algorithm.lower() == "bs":
                self.compressed_image[up_y:down_y, left_x:right_x] = cookie
            index += 1
            
        if algorithm.lower() == "hcomp":
            fitsio.write("hcomp_" + self.image_name, self.h_compress, \
            header=self.header, clobber=True)
        elif algorithm.lower() == "bs":
            fitsio.write("bs_" + self.image_name, self.compressed_image, \
            header=self.header, clobber=True)
        
    def H_Compression(self, scale_value):
        """
        Uses Astropy package's H-Transform Algorithm to lossfully (or losslessly) 
        compress the background noise of the image.
        
        @type self: SuperBit_Compression
        @type scale_value: Int (Lossy Compression Factor)
        @rtype: Numpy Matrix
        """
        self.flag_stars()
        os.chdir(COMP_SOURCE)
        fits.CompImageHDU(self.h_compress, compression_type='HCOMPRESS_1', \
        hcomp_scale=scale_value, hcomp_smooth=1).writeto("HCOMPRESS.fits", overwrite=True)  
        fits.CompImageHDU(self.h_compress, compression_type='HCOMPRESS_1', \
        hcomp_scale=scale_value, hcomp_smooth=1).writeto("hcomp_" + self.image_name, overwrite=True)
        self.h_compress = fits.getdata("hcomp_" + self.image_name)
        fitsio.write("hcomp_" + self.image_name, self.h_compress, \
        header=self.header, clobber=True)

    def masking(self, c_factor):
        """
        Masking Algorithm which will be used to flag and preserve pixel values.
        by cutting these regions out and sending them as a seperate file. The 
        region of these sources will be set to 0 and remaining portion of the 
        image will be compressed using a H Transformation.
        
        @type self: SuperBit Compression
        @type c_factor: Integer (Lossy Compression Factor)
        @rtype: Numpy Matrix
        """
        masked_image = self.original_image.copy()
        
        for star in self.SExtract_data:
            x = star[1]
            y = star[2]
            a_size = star[3]
            b_size = star[4]
            left_x, right_x, up_y, down_y = self.square_cookie(a_size, b_size, \
            x, y, masking = True)
            masked_image[up_y:down_y, left_x:right_x] = 0        
        
        diff = self.original_image - masked_image
        x_pos, y_pos = np.where(diff != 0)
        sources = []
        values = []
        
        for i in range(len(x_pos)):
            sources.append((x_pos[i], y_pos[i], diff[x_pos[i]][y_pos[i]]))
            values.append(diff[x_pos[i]][y_pos[i]])
        sources = np.array(sources)
        
        self.H_Compression(c_factor)
        
        for source in sources:
            self.h_compress[int(source[0])][int(source[1])] = source[2]
        fitsio.write("hcomp_" + self.image_name, self.h_compress, \
        header=self.header, clobber=True)        
        
    def bit_shaving(self, bits=4):
        """
        The bit shaving algorithm to reduce the size of an image.
        
            ALGORITHM IMPLEMENTATION
        -------------------------------
        1) Subtract the Median of the image pixel values.
        2) Add the negative of the minimum value.
        3) Find all source (pixel value > 255)
        4) Shave off bottom 1/2/3/4 bits of the image (divide by 2/4/8/16)
        5) Round each number to the nearest integer, but mark any source with 254.
        
        @type image: Numpy Matrix
        @type bits: Integer (Number of bits dropped)
        @rtype: None
        """
        self.bit_reduction = np.floor(bits)
        
        # Lossless (Source position acquistion)
        self.flag_stars()
        
        # Set Negatives to 0
        # Uncomment below to make this run.
        # self.locate_wrappers()
        
        # Lossless (Value subtractions)
        median = np.median(self.compressed_image)
        self.compressed_image = self.compressed_image - median
        min = np.min(self.compressed_image) 
        self.compressed_image += -min 
            
        if self.bit_reduction <= 0 or self.bit_reduction > 5:
            print("Incomprehensible Bit shave")
            exit()
        elif self.bit_reduction == 5: # 5 Bit Drop
            self.compressed_image = self.compressed_image / 32
            flag = np.where(self.compressed_image ==   7.9375)
            for i in range(len(flag[0])):
                self.compressed_image[flag[0][i]][flag[1][i]] = 8
            self.compressed_image = np.round(self.compressed_image)
            self.compressed_image = self.compressed_image * 32
        elif self.bit_reduction == 4: # 4 Bit Drop
            self.compressed_image = self.compressed_image / 16
            flag = np.where(self.compressed_image == 15.875)
            for i in range(len(flag[0])):
                self.compressed_image[flag[0][i]][flag[1][i]] = 16
            self.compressed_image = np.round(self.compressed_image)
            self.compressed_image = self.compressed_image * 16
        elif self.bit_reduction == 3: # 3 Bit Drop
            self.compressed_image = self.compressed_image / 8
            flag = np.where(self.compressed_image == 31.75)
            for i in range(len(flag[0])):
                self.compressed_image[flag[0][i]][flag[1][i]] = 32
            self.compressed_image = np.round(self.compressed_image)
            self.compressed_image = self.compressed_image * 8
        elif self.bit_reduction == 2: # 2 Bit drop
            self.compressed_image = self.compressed_image / 4
            flag = np.where(self.compressed_image == 63.75)
            for i in range(len(flag[0])):
                self.compressed_image[flag[0][i]][flag[1][i]] = 64
            self.compressed_image = np.round(self.compressed_image)
            self.compressed_image = self.compressed_image * 4
        elif self.bit_reduction == 1: # 1 Bit drop
            self.compressed_image = self.compressed_image / 2
            flag = np.where(self.compressed_image == 127.75)
            for i in range(len(flag[0])):
                self.compressed_image[flag[0][i]][flag[1][i]] = 127
            self.compressed_image = np.round(self.compressed_image)
            self.compressed_image = self.compressed_image * 2
        
        # Restore original pixel values to the compressed image.
        # Uncomment below to let this run.
        # self.compressed_image = self.restore_flags(self.compressed_image)
        
        # Adding back Median and Min
        self.compressed_image += min
        self.compressed_image += median
        
        os.chdir(COMP_SOURCE)    
        fitsio.write("bs_" + self.image_name, self.compressed_image, \
        header=self.header, clobber=True)
       
    def compress_cc(self, algorithm, c_factor=0, cc=False):
        """
        Runs the desired algorithm alongside a cookie cut of the source regions.
        
        algorithm
        ---------
            1) hcomp ->    for H-Transformation
            2) bs    ->    for Bit-Shaving
        
        @type self: SBit_Compression
        @type algorithm: String (algorithm type)
        @type c_factor: Int (Lossy factor)
        @type cc: Boolean (Indicate whether you want to use Region Snipping)
        @rtype: None
        """
        if algorithm == "hcomp":
            self.cc_stars()
            self.H_Compression(c_factor)
            if cc:
                self.cc_restore_stars("hcomp")
        elif algorithm == "masking":
            self.masking(c_factor)
        elif algorithm == "bs":
            self.cc_stars()
            self.bit_shaving(c_factor)
            if cc:
                self.cc_restore_stars("bs")
    
    def show_image(self, version="original", scaling=False):
        """
        Shows our image as a figure using matplotlib. 
        
        If version = "original", shows the original image.
        If version = "bs", shows the bit shaved image.
        If version = "hcomp" shows the H Transformed image.
        
        NOTE- if either H Transformation or bit shaving was not used and if 
        the respective algorithm was called, the original image will be shown
        instead.
        
        If scaling = True, shows a clearer image with visible sources.
        
        @type self: SuperBit_Compression
        @type version: String 
        @type scaling: Boolean (normalize the image to see sources clearer)
        @rtype: None
        """
        if not scaling:
            if version.lower() == "original":
                plt.figure("Original")  
                plt.title("Original")
                plt.imshow(self.original_image)
                plt.show()
            elif version.lower() == "bs":
                plt.figure("Bit Shaved")
                plt.title("Bit Shaved")
                plt.imshow(self.compressed_image)
                plt.show()
            elif version.lower() == "hcomp":
                plt.figure("H Transform")
                plt.title("H Transform")
                plt.imshow(self.h_compress)
                plt.show()
        else: 
            if version.lower() == "original":
                plt.figure("Original Scaled")
                plt.title("Original Scaled")
                max = np.mean(self.original_image) + np.std(self.original_image) * 1
                min = np.mean(self.original_image) - np.std(self.original_image) * 1
                plt.imshow(self.original_image, vmax=max, vmin=min)
                plt.colorbar()
                plt.show()
            elif version.lower() == "bs":
                plt.figure("Bit Shaved")
                plt.title("Bit Shaved")
                max = np.mean(self.compressed_image) + np.std(self.compressed_image) * 1
                min = np.mean(self.compressed_image) - np.std(self.compressed_image) * 1
                plt.imshow(self.compressed_image, vmax=max, vmin=min)
                plt.colorbar()                
                plt.show()
            elif version.lower() == "hcomp":
                plt.figure("H Transform")
                plt.title("H Transform")
                max = np.mean(self.h_compress) + np.std(self.h_compress) * 1
                min = np.mean(self.h_compress) - np.std(self.h_compress) * 1
                plt.imshow(self.h_compress, vmax=max, vmin=min)
                plt.colorbar()
                plt.show()
    
    def show_cuts(self, algorithm):
        """
        Shows the regions where the cookie cuts occur on the image. 
        
        For people with trypophobia, this might be somewhat unsetlling.
        
        algorithm
        ---------
            1) hcomp ->    for H-Transformation
            2) bs    ->    for Bit-Shaving
        
        @type self: SuperBit_Compression
        @type algorithm: String (Algorithm Type)
        @type rtype: None
        """
        if algorithm == "bs":
            diff = self.original_image - self.compressed_image
            plt.figure("DIFF")
            plt.title("DIFF")
            max = np.mean(diff) + np.std(diff) * 1
            min = np.mean(diff) - np.std(diff) * 1
            plt.imshow(diff, vmax=max, vmin=min)
            plt.colorbar()
            plt.show()
        elif algorithm =="hcomp":
            diff = self.original_image - self.h_compress
            plt.figure("DIFF")
            plt.title("DIFF")
            max = np.mean(diff) + np.std(diff) * 1
            min = np.mean(diff) - np.std(diff) * 1
            plt.imshow(diff, vmax=max, vmin=min)
            plt.colorbar()
            plt.show()
        
    def run_statistics(self, algorithm):
        """
        Displays basic statistics, comparing the orginal image to the 
        compressed image. 
        
        Shows the histogram of the pixel value distribution in the image.
        
        THIS METHOD SHOULD NOT BE USED FOR AN IMAGE WITH ONLY 1 SOURCE.
        
        algorithm refers to bs for bit shave and hcomp for H Transformation.
        
        algorithm
        ---------
            1) hcomp ->    for H-Transformation
            2) bs    ->    for Bit-Shaving
        
        @type self: SuperBit_Compression
        @type algorithm: String (Type of Compression)
        @rtype: string
        """
        os.chdir("/home/james/Desktop/sbit_compress_py/experiment/data")
        
        def plothist(img, title="", bins=10000, sig=1, nfig=True, label="", report=True):
            """
            HELPER FUNCTION
            
            Plot a numpy histogram and statistics of different images.
            
            This function was created by Shaabam.
            
            @type img: Numpy Array (The data set)
            @type title: String (Title of image)
            @type bins: Int (Number of Histogram bins)
            @type sig: float (Sigma)
            @type nfig: Boolean (Figure)
            @type label: String (Label of figure)
            @type report: Boolean (Return mean and median of image)
            @rtype: None
            """
            m = np.mean(img)
            s = np.std(img)
            hist, edge = np.histogram(img, bins=bins)
            if nfig:
                plt.figure(figsize=(14, 8))
            plt.plot(edge[1:], hist,label=label)
            plt.xlim([m-(sig * s), m + (sig * s)]);
            plt.title(title);
            plt.legend();
            temp = sorted(hist, key= lambda x:abs(x - np.max(hist) / 2))
            print("\nPeak =", np.max(hist),"FWHM = ", \
            np.abs(edge[np.where(hist == temp[0])] - edge[np.where(hist == temp[1])])[0])
            if report:
                print("Mean after "+label, m)
                print("Median after "+label, np.median(img))
            if not nfig:
                plt.show()
        if algorithm == "bs":
            plothist(self.original_image, title="Pixel Value Distribution", \
            bins=10000, label="original")
            plothist(self.compressed_image, title="Pixel Value Distribution", \
            bins=10000, nfig=False, label="Bit Shave")
        elif algorithm == "hcomp":
            plothist(self.original_image, title="Pixel Value Distribution", \
            bins=50000, label="original")
            plothist(self.h_compress, title="Pixel Value Distribution", \
            bins=50000, nfig=False, label="H Compress")

if __name__ == "__main__":              
    #
    os.chdir(OG_SOURCE)
    sbit = ImageCompression(image_file='new-image.fits', cat="test.cat", crop=False)
    sbit.show_image(version="original", scaling=True)
    sbit.compress_cc(algorithm='hcomp', c_factor=2, cc=False)
    # sbit.run_statistics(True, 'hcomp')
    sbit.show_cuts('hcomp')
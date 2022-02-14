import os
import numpy as np
import shutil
import matplotlib.pyplot as plt

SRC = "../src"
os.chdir(SRC)
from image_compression import *
from fake_stars import *

OG_SOURCE = "../original"
COMP_SOURCE = "../compressed"
DS9 = "../ds9"
MAIN = "/home/james/Desktop/sbit_compress_py/"

class SE_Comparison:
    """
    A class module designed to help run analysis for compressed and original
    images using SExtractor.
    
    This class module is capable of RUNNING SIMULATIONS for a set number of 
    SOURCES and obtain data between the compressed and original versions.
    
    This class module is also capable of also running simulations for real
    SuperBIT images and obtaining the data between the compressed and original
    version.
    
    -------------------------
        NOTE (READ BELOW)
    -------------------------
    
    In order for this class to run, Source Extractor must be properly install 
    along with any necessary python packages. The directory of the files above
    must also be changed to the necessary location.
    """
    def __init__(self, factor, comp_type):
        """
        Initializes a new SE_Comparison object which will be used to run 
        comparisons between compressed and original images.
        
        NOTE: Only masking and hcomp compress type are capable of taking float 
        compresison factor values. For any other compression type, the value
        will be rounded off.
                
        comp_type is the compression algorithm you with to use. The options are
        between "hcomp" for H Transformation, and "bs" for bit shaving.
        ---------
            hcomp- H-Transformation using Astropy's HTransform method.
            
            bs- Bit Shaving by dropping the lowest bits.
            
            masking- H- Transformation using a smarter way to locate source 
            positions.
                        
        @type self: SE_Comparison
        @type factor: Int (Compression factor)
        @type comp_type: String
        @rtype: None
        """
        self.comp_f = factor
        self.compression = comp_type
        
        # For Generated Fake Stars
        self.og_sources = []
        self.comp_sources = []
        
        # For Actual Image
        self.im_og_sources = []
        self.im_cp_sources = []
        
        self.og_dict = {}
        self.comp_dict = {}
        self.id_to_label = {1:"Flux Auto",\
                        2: "X Position",
                        3: "Y Position",
                        4: "A Image",
                        5: "B Image",
                        6: "Flux Radius",
                        7: "Ellipticity",
                        8: "Elongation",
                        9: "THETA ANGLE",
                        10: "NUMBER"}
        
    def run_ss_experiment(self, sources, sd=29, cut=False, rp=False, bt=[200, 5, 5], sz=100):
        """
        This method runs a quick simulation for the desired number of generated
        single sources and compresses the image using the desired algorithm.
        
        The cut parameter determines whether or not you would want your sources
        to be cookie cut.
        
        The rp parameter determines whether or not you would the centre of the 
        source to be randomized. If true, this acts like a pseudo monte-carlo 
        simulation.
        
        The bt parameter represents (in order): brightness, x_sigma, y_sigma 
        of the source in that order.
        
        Sz is the dimension (height and width) of the fake image. By default, 
        the generated source will be in a 100 by 100 image grid.
        
        @type self: SE_Comparison
        @type sources: Integer (Number of desired sources)
        @type sd: Int (Standard deviation of noise)
        @type rp: Boolean (Random Position)
        @type cut: Boolean 
        @type bt: List[ints] (Source Parameters)
        @type sz: Dimension of the image (Height and Width)
        @rtype: None
        """
        alg = self.compression
        c_fact = self.comp_f
        for i in range(sources):
            os.chdir(OG_SOURCE)
            fs = FakeStars("fakestar1", 4400, 6650)
            fs.create_single_source(bt=bt[0], std=sd, xf=bt[1], yf=bt[2], rand_pos=rp, sz=sz)
            fs.create_fits_image()
            os.system("sextractor fakestar1.fits -c default.sex")
            sbit = ImageCompression(image_file='fakestar1.fits', cat="test.cat")   
            sbit.compress_cc(algorithm=alg, c_factor=c_fact, cc=cut)
            os.chdir(COMP_SOURCE)
            if alg =='hcomp':
                os.system("sextractor hcomp_fakestar1.fits -c default.sex")
            elif alg == 'bs':
                os.system("sextractor bs_fakestar1.fits -c default.sex")
            og, cs = self.cat_reader([i for i in range(1, 11)]) 
            self.og_sources.append(og)
            self.comp_sources.append(cs)
        self.get_parameter()
        
    def cat_reader(self, index):
        """
        This method returns the parameters obtained in SExtractor verbatim. 
        
        Below are the different parameters that SExtractor will find.
        
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
        
        @type self: SE_comparison
        @type index: List[indexes]
        @rtype: List
        """    
        os.chdir(COMP_SOURCE)
        csdata1 = np.loadtxt("test.cat").T
    
        os.chdir(OG_SOURCE)
        osdata1 = np.loadtxt("test.cat").T
        
        return [osdata1[i-1] for i in index], [csdata1[i-1] for i in index]
        
    def get_parameter(self):
        """
        After compressing the image, SExtractor will often find more sources than
        there actually are. This method is used to find and compare about 90-95%
        sources from the original image to the compressed image.
        
        This method will exclude any generated sources found after the compression.
        
        @type self: SE_comparison
        @rtype: None
        """
        def get_true_source():
            """
            THIS IS USED FOR SINGLE SOURCE SIMULATIONS ONLY!!! NOT FOR IMAGES!!
            
            Due to the noise, source extractor sometimes finds and extra source
            in the compressed and original image. 
            
            Given that we know there exists only one source and that it has the 
            highest FLUX out of all "sources" (fake sources included), this 
            function will return the parameters for the true source.
            
            This is a HELPER FUNCTION.
            
            @rtype: List[List, List]
            """
            f1 = []
            f2 = []
            for source in self.og_sources:
                if isinstance(source[0], float):
                    f1.append(0) # position of the source is at first index.
                else:
                    # Get the index of the source with the highest flux value.
                    f1.append((np.argmax(source[0])))
                
            for source in self.comp_sources:
                if isinstance(source[0], float):
                    f2.append(0) # position of the source is at first index.
                else:
                    # Get the index of the source with the highest flux value.
                    f2.append((np.argmax(source[0])))
            return f1, f2
            
        for index in range(10):
            o_i, c_i = get_true_source()
            index = round(index-1)
            f1 = []
            f2 = []
            for source in self.og_sources:
                if isinstance(source[index], float):
                    f1.append(source[index])
                    o_i.pop(0)
                else:
                    f1.append((source[index][o_i[0]]))
                    o_i.pop(0)
                
            for source in self.comp_sources:
                if isinstance(source[index], float):
                    f2.append(source[index])
                    c_i.pop(0)
                else:                
                    f2.append((source[index][c_i[0]]))
                    c_i.pop(0)
            index += 1
            self.og_dict[index] = f1
            self.comp_dict[index] = f2
    
    def run_im_experiment(self, im_name, cut=False):
        """
        This method runs a simulation and returns a statistical comparison
        between the original image and compressed image.
        
        The cut parameter allows sources found in the image to be cropped out 
        which preservces their original values. 
        
        @type self: SE_comparison
        @type im_name: String (Name of the image)
        @type cut: Boolean (Cookie Cutting enabled/disabled)
        @rtype: None
        """
        alg = self.compression
        c_fact = self.comp_f
        os.chdir(OG_SOURCE)
        os.system("sextractor cp_new-image.fits -c default.sex")
        sbit = ImageCompression(image_file='cp_new-image.fits', cat="test.cat")   
        sbit.compress_cc(algorithm=alg, c_factor=c_fact, cc=cut)
        os.chdir(COMP_SOURCE)
        if alg =='hcomp':
            os.system("sextractor hcomp_cp_new-image.fits -c default.sex")
        elif alg == 'bs':
            os.system("sextractor bs_cp_new-image.fits -c default.sex")
            
    def image_comparison(self):
        """
        This method is used to compare sources from  the original image to the 
        sources in the compressed version.
        
        @type self: SE_comparison
        @rtype: None
        """
        og, cs = self.cat_reader([2,3])
        og = np.round(og)
        cs = np.round(cs)        
        
        og_co = []
        for i in range(len(og[0])):
            og_co.append((og[0][i], og[1][i]))     
               
        cs_co = []
        for i in range(len(cs[0])):
            cs_co.append((cs[0][i], cs[1][i]))
      
        og_idx = []
        cs_idx = []
        for coord in og_co:
            for j in range(-1, 1):
                x = coord[0] + j
                for k in range(-1, 1):
                    y = coord[1] + k
                    if (x, y) in cs_co:
                        og_idx.append(og_co.index(coord))
                        cs_idx.append(cs_co.index((x, y)))
        
        os.chdir(OG_SOURCE)
        osdata1 = np.loadtxt("test.cat")
        z1 = []
        
        os.chdir(COMP_SOURCE)
        csdata1 = np.loadtxt("test.cat")
        z2 = []
        os.chdir(MAIN)

        # Updates z1, z2 to refer to the same sources.
        for i in og_idx:
            z1.append(osdata1[i])
        
        for i in cs_idx:
            z2.append(csdata1[i])

        # Returns desired parameter from test.cat file
        self.im_og_sources = np.array(z1).T
        self.im_cp_sources = np.array(z2).T
                    
    def signal_to_noise(self, fwhm_lim, bt_lim, rp=False, cut=False):
        """
        THIS IS ONLY FOR A SINGLE SOURCE SIMULATION. THIS METHOD WILL FAIL WHEN
        USED FOR AN IMAGE WITH MULTIPLE SOURCES!!!!!!
        
        Runs a simulation to determine where source extractor fails based on
        the signal to noise ratio of the source and the fwhm of its x and y
        sigma.
        
        If rp = true, the source will be centred around a square of values.
        If cut = true, then cookie cutting will be used in the compression
        algorithm.
        
        Brightness determines what the highest count of a source will be.
        Fwhm_lim determines the pixel width of a source.
        
        If the return value is 1 it means it succeeded.
        if the return value is 0 it means it failed.
        
        @type self: SE_comparison
        @type fwhm_x: Float
        @type fwhm_x: Float
        @type brightness: Float
        @rtype: Integer
        """
        def sim(fwhm_x, fwhm_y, brightness):
            """
            Helper function to run a simulation.
            """
            try:
                self.run_ss_experiment(sources=50, rp=False, cut=False, \
                bt=[brightness, fwhm_x, fwhm_y])
                return(1)
            except:
                return(0)
                
        success_x = []
        success_y = []
        
        failed_x = []
        failed_y = []
        
        for i in range(1,fwhm_lim):
            for j in range(8, bt_lim):
                j = j * 10
                run = sim(fwhm_x=i/2, fwhm_y=i/2, brightness = j)
                if run == 1:
                    success_x.append(i/2)
                    success_y.append(j)
                elif run == 0:
                    failed_x.append(i/2)
                    failed_y.append(j)
            
        plt.figure("Signal To Noise (29 Noise)")
        plt.title("Signal To Noise (29 Noise)")
        suc = plt.plot(success_x, success_y, label='success', marker='o', linestyle='None', alpha=0.6)
        fail = plt.plot(failed_x, failed_y, label='failed', marker='x', linestyle='None', alpha=0.6)
        plt.xlabel("FWHM (in pixels)")
        plt.ylabel("Brightness")
        plt.ylim(70, (bt_lim+1)*10)
        plt.legend(loc='upper left', numpoints = 1)
        plt.show()
  
    def mean_std(self, index, image):
        """
        Returns the mean and standard deviation of the desired parameters found
        by SExtractor.
        
        Index refers to the desired parameter value.
        
        Image is a boolean value indicating whether this statistics is for an 
        image fits file or a single source file.
        
        @type self: SE_comparison
        @type index: Int
        @type image: Boolean
        @rtype: String
        """
        if image:
            og = self.im_og_sources[index-1]
            cs = self.im_cp_sources[index-1]
            if index == "distance":
                og = np.sqrt((mp-np.array(self.im_og_sources[2]))**2 + \
                (mp-np.array(self.im_og_sources[3]))**2)
                cs = np.sqrt((mp-np.array(self.im_cp_sources[2]))**2 + \
                (mp-np.array(self.im_cp_sources[3]))**2)
                print("\nOriginal MEAN: ", np.mean(og))
                print("Original STD: ", np.std(og))
                print("Compressed MEAN: ", np.mean(cs))
                print("Compressed STD: ", np.std(cs))
            else:
                print("\nOriginal MEAN: ", np.mean(self.im_og_sources[index]))
                print("Original STD: ", np.std(self.im_og_sources[index]))
                print("Compressed MEAN: ", np.mean(self.im_cp_sources[index]))
                print("Compressed STD: ", np.std(self.im_cp_sources[index]))
        else:
            if index == "distance":
                og = np.sqrt((mp-np.array(self.og_dict[2]))**2 + (mp-np.array(self.og_dict[3]))**2)
                cs = np.sqrt((mp-np.array(self.comp_dict[2]))**2 + (mp-np.array(self.comp_dict[3]))**2)
                print("\nOriginal MEAN: ", np.mean(og))
                print("Original STD: ", np.std(og))
                print("Compressed MEAN: ", np.mean(cs))
                print("Compressed STD: ", np.std(cs))
            else:
                print("\nOriginal MEAN: ", np.mean(self.og_dict[index]))
                print("Original STD: ", np.std(self.og_dict[index]))
                print("Compressed MEAN: ", np.mean(self.comp_dict[index]))
                print("Compressed STD: ", np.std(self.comp_dict[index]))
            
    def numpy_hist(self, img, title="", bins=10000, sig=1, report=True, label=''):
        """
        This method is used to display the histogram of a data set.
        
        @type self: SE_comparison
        @type img: Numpy Array
        @type title: String
        @type bins: Int
        @type sig: Int
        @type report: Boolean
        @type label: String
        @rtype: None
        """
        m = np.mean(img)
        s = np.std(img)
        hist, edge = np.histogram(img, bins=bins, density=1) # <-- Density Plot #
        plt.plot(edge[1:], hist, label=label)
        
        # Uncomment this to set x-limit. #
        # plt.xlim([m-(sig*s),m+(sig*s)]) #
        
        plt.xlabel(title)
        plt.ylabel("Frequency Count")
        plt.title(title + " (Density Plot)")
        plt.legend()
        temp = sorted(hist, key= lambda x:abs(x - np.max(hist) / 2))
        print("P\neak =", np.max(hist),"FWHM = ", \
        np.abs(edge[np.where(hist == temp[0])] - edge[np.where(hist == temp[1])])[0])
        if report:
            print("Mean after "+label, m)
            print("Median after "+label, np.median(img))
        plt.show()
        
    def plot_hist(self, index, image, bins=200, alg='H Compress'):
        """
        Plots the histogram for the original and compressed image for the
        desired parameter.
        
        alg is the specified compression type
            1) H Compress - H Compression algorithm
            2) Bit shave - Bit Shave algorithm
        
        @type: SE_Experiment
        @type index: Integer (Desired Parameter value) 
        @type image: Numpy Array
        @type bins: Int
        @type alg: String ("Compression type")
        @rtype: None
        """
        lb = self.id_to_label[index]
        og = self.og_dict[index]
        cs = self.comp_dict[index]
        
        if image:
            og = self.im_og_sources[index-1]
            cs = self.im_cp_sources[index-1]
            x = np.linspace(1, len(og), len(og)) 
            self.numpy_hist(og-cs, title=lb + " Difference", bins=bins, label="Difference")
        else:
            if alg == "bs":
                self.numpy_hist(og, title=lb, bins=bins, label="Original")
                self.numpy_hist(cs, title=lb, bins=bins, label="Bit Shave")
            elif alg == "hcomp":
                self.numpy_hist(og, title=lb, bins=bins, label="Original")
                self.numpy_hist(cs, title=lb, bins=bins, label="H Compress")
                            
if __name__ == "__main__":
    # Run Statistics (Example)
    bs1 = SE_Comparison(2, 'H_COMPRESS')
    id = 'distance'
    bs1.plot_hist(index=id, lb=id, bins=300)
    bs1.mean_std(index=id)

    ## Get Parameter
    id = 7
    label="HCOMP 2 " + bs1.id_to_label[id]
    print(label)
    bs1.plot_hist(index=id, lb=label, bins=1000)
    bs1.mean_std(index=id)

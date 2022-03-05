import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.utils.data import download_file
import os
import random

class FakeStars():
    """
    A class object that generates fake sources or fake images.
    
    NOTE- The generate sources are generated using statistical information from
    existing data but are completely pseudo and do not represent a real 
    science image.
    
    In order for this class to run, you need to necessary Python modules installed.
    
    It is recommended you run this on LINUX, I've tried making it compatible with
    windows but I encounter some errors.
    """
    
    def __init__(self, image_name, x_len, y_len):
        """
        Initializes a new FakeStar object which represents either a fake space 
        image or a fake singular point source.
        
        @type self: FakeStars
        @type image_name: String (The name of the image)
        @type x_len: Int (Width of Image)
        @type y_len: Int (Height of Image)
        @rtype: None
        """
        self.name = image_name
        self.width = x_len
        self.height = y_len
        self._image_array = np.zeros((x_len, y_len))
        self.noise = np.zeros((x_len, y_len))
          
    def generate_white_noise(self, std=29, mean=0):
        """
        Generates a 1D array of random gaussian white noise. The default
        setting for the average noise is 29. (This is estimated to be SuperBIT's
        estimated noise)
        
        The length of the array is width * height of the image.
        
        @type self: FakeStars
        @rtype: Numpy Array
        """
        num_samples = self.width * self.height
        white_noise = np.round(np.random.normal(mean, std, size=num_samples))
        white_noise = white_noise.reshape(self.width, self.height)
        return white_noise

    def generate_background(self, mean=1250, std=0):
        """
        Generates a fake background representing the dark sky of the image.
        The background has a median value of 1250.
        
        All this does is simply add the value 1250 to each individual pixel in 
        the image. 
        
        @type self: FakeStars
        @rtype: Numpy Array
        """
        num_samples = self.width * self.height
        background = np.round(np.random.normal(mean, std, size = num_samples))
        return background
                        
 
    def create_2d_gaussian(self, size, xfwhm=2, yfwhm=2, center=None, btness=400):
        """ Make a square gaussian kernel
    
        Size is the length of a side of the square
        fwhm is full-width-half-maximum, which
        can be thought of as an effective radius.
        
        @type self: FakeStars
        @type size: Int 
        @type xfwhm: Int
        @type yfwhm: Int  
        @type center: Tuple (Coordinates of center of star)
        @type btness: Int (Brightest point of star)
        """
        x = np.arange(0, size, 1, float)
        y = x[:,np.newaxis]
    
        if center is None:
            x0 = y0 = size // 2
        else:
            x0 = center[0]
            y0 = center[1]
        return btness * np.exp(-4*np.log(2) * ((x-x0)**2 / xfwhm**2 + \
                                               (y-y0)**2 / yfwhm**2))
                                               
    def create_point_stars(self, num_stars):
        """
        Creates a fake single pixel to represent a hot pixel on a SuperBIT
        image.
        
        The star will simply be a dot on the image with a high intensity 
        brightness.
        
        @type self: FakeStars
        @type num_stars: Integer
        @rtype: Numpy Array
        """
        for i in range(num_stars):
            point_star = random.randint(6000, 60000)
            x_pos = random.randint(0, self.width-1) 
            y_pos = random.randint(0, self.height-1)  
            self._image_array[x_pos][y_pos] += point_star
        
    def create_stars(self, generator=100, sz=20, xf=10, yf=10, amp=200):
        """
        Creates a certain number of fake star based on different parameters 
        based on the generator value. 
        
        @type self: FakeStars
        @type generator: Int (Number of Iterations)
        @type sz: used to randomly step away from the designated point.
        @type xf: Int (FWHM in x direction)
        @type yf: Int (FWHM in y direction)
        @type amp: Int (The Amplitude of the gaussian- how bright a star is)
        @rtype: None
        """
        while generator != 0:
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            source = self.create_2d_gaussian(size=sz, xfwhm=xf, yfwhm=yf, btness=amp)
            self._image_array[x:x+sz, y:y+sz] += source
            generator -= 1
        
    def create_cosmic_rays(self, amount):
        """
        Creates a streak of cosmic ray streak that will be randomly placed 
        in the image.
        
        @type self: FakeStars
        @type amount: Int (Number of sources)
        @rtype: None
        """
        while amount != 0:
            size = 40
            chance = random.randint(0,1)
            rotation = random.randint(0, 2)
            x_pos = random.randint(0, self.width - 1) 
            y_pos = random.randint(0, self.height - 1)  
            brightness = 8000
            while size != 0:
                if rotation == 0:
                    if x_pos >= 4400 or y_pos >= 6650:
                        break
                    self._image_array[x_pos][y_pos] += brightness
                    x_pos += 1
                    y_pos -= 1
                elif rotation == 1:
                    if x_pos >= 4400 or y_pos >= 6650:
                        break
                    self._image_array[x_pos][y_pos] += brightness
                    x_pos += 1
                    y_pos += 1
                else:
                    if x_pos >= 4400 or y_pos >= 6650:
                        break
                    self._image_array[x_pos][y_pos] += brightness
                    x_pos += 1
                size -=1
                brightness -= 8000/500
            amount -= 1
            
    def create_single_source(self, bt=250, xf=10, yf=10, rand_pos=False, std=29, sz=100):
        """
        Creates a single fake source with different noise realizations.
        
        Brightness increases the signal of the source value.
        
        @type self: FakeStars
    
        @type bt: Int (Brightest point in the star)
        @type xf: Int (FWHM in x direction)
        @type yf: Int (FWHM in y direction)
        @type rand_pos: Boolean (Randomly places star)
        @type std: Int (Standard Deviation)
        @type sz: Size of Image (height by width)
        @rtype: None
        """
        x = y = sz // 2
        if rand_pos:
            x += random.uniform(-0.5, 0.5)
            y += random.uniform(-0.5, 0.5)
        star = self.create_2d_gaussian(size=sz, xfwhm=xf, yfwhm=yf, center=(x, y), btness=bt)
        num_samples = sz*sz
        white_noise = np.round(np.random.normal(29, std, size=num_samples))
        white_noise = np.reshape(white_noise, (sz, sz))
        self.noise = white_noise
        self._image_array = star + white_noise
        
    def create_image(self, signal=1, btness= 400):
        """
        Creates a fake map with different sources and galaxies.
        
        Signal is an integer value. Which determines how many fake sources 
        of different forms (Point stars, large sources, galaxies, cosmic rays)
        will be created.
        
        @type self: Fake_Star 
        @type signal: Int 
        @type btness: Int (Brightest point of a source)
        @rtype: None
        """
        self.noise = self.generate_white_noise()
        self.create_point_stars(signal*100)
        if type(btness) == list:
            for amp in btness:
                if random.randint(0, 25) == 1:
                    self.create_stars(generator=signal * 5, sz=50*2, xf=5, yf=2, amp=amp)
                else:
                    self.create_stars(generator=signal * 5, sz=50*2, xf=amp/40, yf=amp/40, amp=amp)
        else:
            self.create_stars(generator=signal*5, sz=30, xf=amp/40, yf=amp/40, bt=btness)
        self.create_cosmic_rays(signal*3)
        self._image_array += self.noise
        
    def new_noise(self):
        """
        Creates a new generated white noise background with the same sources
        in the same position.
        
        @type self: Fake_stars
        @rytpe: None
        """
        self._image_array -= self.noise
        self.noise = self.generate_white_noise()
        self._image_array += self.noise
        
    def cap_pixel_value(self, bit_limit=64):
        """
        Limits the maximal pixal value to be below a 16 bit number
        
        @type self: Fake_Stars
        @rtype: None
        """
        x, y = np.where(self._image_array > 65535)
        if type(x) == np.ndarray and len(x) > 0:
            for i in range(len(x)):
                self._image_array[x[i]][y[i]] = 65535
        
    def show_image(self, together=True):
        """
        Displays the scaled and original version of the source.
        
        The together parameter puts both sources into the one figure.
        
        @type self: FakeStars
        @type together: Boolean 
        @rtype: None
        """
        if together:
            fig=plt.figure(figsize=(10, 10))
            columns = 2
            rows = 1
            max = np.mean(self._image_array) + np.std(self._image_array) *3
            min = np.mean(self._image_array) - np.std(self._image_array) *3
            fig.add_subplot(rows, columns, 1)
            plt.title("Normalized")        
            plt.imshow(self._image_array, vmax=max, vmin=min)
            plt.colorbar()
            fig.add_subplot(rows, columns, 2)
            plt.title("Original")
            plt.imshow(self._image_array)
            plt.colorbar()
            plt.show()
        else:
            plt.figure("Scaled")
            plt.title("Scaled")
            max = np.mean(self._image_array) + np.std(self._image_array) *1
            min = np.mean(self._image_array) - np.std(self._image_array) *1
            plt.imshow(self._image_array, vmax=max, vmin=min)
            plt.colorbar()
            plt.figure("Original")
            plt.title("Original")
            plt.imshow(self._image_array)
            plt.colorbar()
        plt.show()

    def create_fits_image(self):
        """
        Creates a fake fits image and saves it onto the current working directory.
        
        Use os.chdir() to change to the desired save location
        
        clobber: bool, optional- if True, overwrite any existing file.
        
        @type self: FakeStars
        @rtype: None
        """
        hdu = fits.PrimaryHDU(data=self._image_array)
        hdu.writeto(self.name + "large.fits", overwrite=True)
        
    def show_statistics(self):
        """
        Runs basic statistics on the fake image and prints the values.
        
        @type self: FakeStars
        @rtype: None
        """
        # Basic Statistics
        self.median = np.median(self._image_array)
        self.mean = np.mean(self._image_array)
        self.min = np.min(self._image_array)
        self.std = np.std(self._image_array)
        
        print("Mean: ", self.mean, "\n")
        print("Min: ", self.min, "\n")
        print("Median: ", self.median, "\n")
        print("Standard Deviation: ", self.std, "\n") 
        
    def return_image(self):
        """
        Returns the image array data.
        
        @type self: Fakestars
        @rtype: Numpy Array
        """
        return self._image_array
           
## (Example)

if __name__ == '__main__':
    os.chdir("/Users/a16472/desktop/")

    fakestar1 = FakeStars("fakestar1", 4400, 6650)
    fakestar1.create_image(signal = 150, btness=[1200, 1000, 800, 200])
    
    # fakestar1 = FakeStars("fakestar1", 100, 100)
    # fakestar1.create_single_source(bt=250, xf=2, yf=2, sz=100)

    fakestar1.cap_pixel_value()
    fakestar1.create_fits_image()
    fakestar1.show_image(together=False)

    fakestar1.new_noise()
    fakestar1.show_image(together=False)
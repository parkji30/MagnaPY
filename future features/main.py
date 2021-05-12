import os

SRC = "/home/james/Desktop/sbit_compress_py/src"
OG_SOURCE = "/home/james/Desktop/sbit_compress_py/original"
COMP_SOURCE = "/home/james/Desktop/sbit_compress_py/compressed"
DS9 = "/home/james/Desktop/sbit_compress_py/ds9"
MAIN = "/home/james/Desktop/sbit_compress_py/"
os.chdir(SRC)

from Sbit_Compression import *
from fake_stars import *
from se_experiment import *


## UPDATE PARAMETERS HERE
# ------------------
# COMPRESSION_TYPE 
# ------------------
#
# This parameter indicates the type of algorithm you wish to test.
# It can either be: 
# --------------------------------
# "bs" for           Bit-Shaving
# "hcomp" for        H-Transfomation
# ---------------------------------
#
# ----------------------------------------------------------------------------
COMPRESSION_TYPE = 'bs'

# ----------
# C_FACTOR
# ----------
#
# This parameter is for the lossy compression factor.
#
# Please note, if you run a bit shaving simulation, you SHOULD ONLY USE 
# INTEGERS between the values of 1 and 4 for your C_FACTOR
#
# If you run H transformation simulation, you can use any value greater 
# than 0 for your C_FACTOR value.
#
# ----------------------------------------------------------------------------
COMPRESSION_VALUE = 4

# --------
# SOURCES 
# --------
# This parameter indicates the number of sources you wish to simulate and test
# varying algorithms (with different compression factors).
#
# ----------------------------------------------------------------------------
SOURCES = 1000


# -----
# SIZE 
# -----
# This parameter indicates how big the image will be in the simulation.
# For example, SIZE = 100 will create an image of 100 by 100 size.
#
# ---------------------------------------------------------------------------
SIZE = 100 


# -----------
# BRIGHTNESS
# -----------
# This parameter indicates the brightness and size of the sources. 
# first value is the brightest point 
# second value is the xfwhm
# third value is the yfwhm
#
# ---------------------------------------------------------------------------
BRIGHTNESS = [250, 2, 2]


# ----------
# REGION_CUT
# ----------
# This parameter determines whether or not you would like the sources to the 
# preserved by taking a region cut aronud it.
#
# It has been noted that region cutting has resulted in better results after
# compression.
#
# ----------------------------------------------------------------------------
REGION_CUT = False


## SIMULATION
simulation = SE_Comparison(factor=COMPRESSION_VALUE, comp_type=COMPRESSION_TYPE)
simulation.run_ss_experiment(sources=SOURCES, cut=REGION_CUT, bt=BRIGHTNESS, sz=SIZE)


## STATISTICS and PLOTS
"""
SExtractor test.cat parameters 

NOTE, you must set the default.param to return the below parameters in 
SExtractor. 

These are the parameters that are returned when SExtractor is used on an 
astronomical image.

1 FLUX_AUTO              Flux within a Kron-like elliptical aperture                [count] 
2 X_IMAGE                Object position along x                                    [pixel] 
3 Y_IMAGE                Object position along y                                    [pixel] 
4 A_IMAGE                Profile RMS along major axis                               [pixel] 
5 B_IMAGE                Profile RMS along minor axis                               [pixel] 
6 FLUX_RADIUS            Fraction-of-light radii                                    [pixel] 
7 ELLIPTICITY            1 - B_IMAGE/A_IMAGE                                                
8 ELONGATION             A_IMAGE/B_IMAGE                                                    
9 ALPHA_J2000            Right ascension of barycenter (J2000)                      [deg]   
10 DELTA_J2000            Declination of barycenter (J2000)                          [deg]   
"""
simulation.plot_hist(index=8, image=False, alg=COMPRESSION_TYPE, bins=150)
simulation.mean_std(index=8, image=False)


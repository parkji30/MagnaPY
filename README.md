# SuperBIT_Compression
A compression algorithm and source simulator the the ballon borne telescope, Super/Giga BIT

NOTE
----

In order for this program to run, you must have SExtractor installed. A good description of how to get SExtractor 
set up can be found here- https://sextractor.readthedocs.io/en/latest/Installing.html.

You should also have the necessary packages from python installed- numpy, matplotlib, scipy, astropy, fitsio, etc. 


HOW TO RUN THE PROGRAM
----------------------
This program is best run using linux, but can be modified to run on windows. Windows prevents the user from installing 
fitsio which is critical for this simulation to work.

1) Open the <b>main.py file</b>, the entire program is run here, but it is encouraged to read the other files and their 
methods to get a detailed explanation.

2) Description of each parameter is found in the main.py file, but most important, the directories labelled <b>MUST</b> be changed according to where you save this program.

  SRC = "/home/james/Desktop/sbit_compress_py/src"
  
  OG_SOURCE = "/home/james/Desktop/sbit_compress_py/original"
  
  COMP_SOURCE = "/home/james/Desktop/sbit_compress_py/compressed"
  
  DS9 = "/home/james/Desktop/sbit_compress_py/ds9"
  
  MAIN = "/home/james/Desktop/sbit_compress_py/"
  

  
I will provide a better update of the methods and their description in the near future, but for now, this is sufficient 
enough to see a working simulation.

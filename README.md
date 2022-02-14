# Motivation

Balloon-borne telescopes have grown tremendously in their capabilities for capturing high quality science
data. However, there is a challenge associated with these advancements: the limited down-link bandwidth
available to most balloon payloads to transmit science data. 

Progress in astronomical research
demonstrates that the compression of crucial data is becoming increasingly important. Such a clear
example lies in the balloon-borne telescopes BLAST-TNG and SuperBIT. Being able to down-link science
data during the flight is crucial to evaluate payload performance, and debug any inevitable problems. 

The use of compression algorithms proves to be an effective solution in increasing the rate at which data can
be down-linked, while ensuring the down-linked data have sufficient quality for science analysis.

# Magna

Magna is an open source compression optimization software that will compress your data and analyze the information for you pre and post compression 
ensuring the maximal compression factor possible while minimizing information loss to the data.

Magna will compress your data using HCOMPRESS, RICE, GZIP, BZIP2 and return the post compression results in a neat textfile. From there you can analyze 
comrpession results for your data structure and inform magna which compression algorithm you wish to use.

# Installation 

Make sure to install the dependencies using pip in Python by downloading the requirements.txt file. This program is primarily used as a script and can be incorporated into your project.

```python
pip install -r requirements.txt
```

# Image Compression Simulation

An Image compression simulator that uses Source Extractor and Monte Carlo methods to examine the post compressive effects of different compression algorithms.


# Dependencies
Type the following below to install the required modules.

```
pip install -r requirements.txt
```

# Author's Note

This work done behind this program was to investigate the compression effects of different compression algorithms on an real science image which then has over 10000 simulated copies (due to the lack of real data) of it via Monte Carlo methods. These simulated images are then analyzed by Source Extractor- https://sextractor.readthedocs.io/. to examine the pre and post compressive effects on the image.

# Some Cool Results from Magna

Some simulated stars using Magna

![another simulated star](https://user-images.githubusercontent.com/28542017/145659035-45a2616c-070f-4e4b-a97c-6ccfaf28fee2.png)
![simulated_star](https://user-images.githubusercontent.com/28542017/145659037-a35ef1ba-0459-401b-bdf3-acc5d4333932.png)


Analysis showing the compression effects of the HCOMPRESS algorithm. We see that the distribution of the ellipticity value detected by source extractor did not get distorted from our Monte Carlo simulation of over 1000 simulated stars as shown above. We conclude that the HCOMPRESS algorithm can be safely used for sources of this nature in our science data.

![analysis](https://user-images.githubusercontent.com/28542017/145659076-38b4478c-9cfd-4483-b386-893ee3c27969.png)


Signal to noise plot showing the limitations of Source Extractor. Essentially Source Extractor cannot detect sources with a FWHM less than 1.5 sigma.

![signaltonoise](https://user-images.githubusercontent.com/28542017/145659083-3641effb-6fc6-4d3c-a548-3d17a2697756.png)



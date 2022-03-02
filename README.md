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

Magna is an open source optimization software that uses machine and deep learning techniques to determine the optimal factor of a chosen compression algorithm based on the provided dataset.

Magna will compress your data using HCOMPRESS, RICE, GZIP, BZIP2 and test the limitation of how much the test images can be quantized (lossy technique) with various algorithms in order to predict compression limits on future datasets.

# Installation 

Make sure to install the dependencies using pip in Python by downloading the requirements.txt file. This program is primarily used as a script and can be incorporated into your project.

```python
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



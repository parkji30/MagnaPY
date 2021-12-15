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

# Guide To Use
Soon to write something here!


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
Magna is a real-time compression optimizer software that will allow the user to implement an optimal compression algorithm in any data pipeline.

```python
import numpy
import matplotlib.pyplot
import astropy
import scipy
```

<h1>Future Work</h1>
     1) Manual selection of desired compressed image.
<br> 2) Event listener for automated compression through TCP socket server.
<br> 3) Expansion to other types of file extensions.


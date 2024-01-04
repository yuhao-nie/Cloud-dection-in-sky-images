# Cloud detection in sky images

Clouds significantly impact PV panel output and pose challenges to the large-scale deployment of solar PV systems. Accurate detection of clouds in sky images is a critical step in cloud modeling, which is essential for reliable solar power forecasting. 

![demo_intermittency](/figs/demo_pv_output_cloudy_day.gif)
<p align=justify>
Figure 1. Power output of a 30-kW roof-top PV system on a partly cloudy day. Note how PV output fluctuates during the cloud events.
</p>

This repository presents an easy-to-implement yet effective algorithm for detecting clouds in ground-based sky images. This algorithm has been used in the study by [Nie et al. (2020)](https://pubs-aip-org.stanford.idm.oclc.org/aip/jrse/article/12/4/046101/284973) to identify cloud pixels in sky images for sky condition classification, which enables the development of tailored models for solar nowcasting specific to each sky condition. This classification-prediction framework show better performance with less model trainable parameters than the deep learning model [SUNSET](https://pubs-rsc-org.stanford.idm.oclc.org/en/content/articlehtml/2018/ee/c7ee03420b) that learns a map from sky images to PV power generation in an end-to-end fashion.

## Cloud detection algorithm
The cloud detection algorithm essentially performs binary classification, i.e., distinguishing each pixel in a sky image as either a cloud or non-cloud pixel. Various methods have been developed for this purpose, ranging from simple thresholding techniques to more complex approaches such as neural network models, Markov Random Fields models, and Gaussian Mixture Models [[1]](#1).

we select the thresholding method, favored for its simplicity and low computational requirements, which facilitates near real-time application. Our algorithm specifically integrates the **normalized red blue ratio (NRBR)** and **clear sky library (CSL)** methods. To better understand our proposed approach, it is essential to first explore NRBR and CSL and examine their advantages and limitations.

### NRBR
NRBR is defined by the following equation: $$NRBR = (B-R)/(B+R)$$
where R and B stand for the pixel values of the red and blue channels of a sky image, , ranging from 0 to 255. According to the Rayleigh scattering law, the intensity of scattered light in clear air is inversely proportional to the fourth power of the wavelength [[2]](#2). This implies that the blue spectrum of visible light is predominately scattered in the clear atmosphere, whereas cloud particles scatter blue and red light almost equally [[1]](#1). It results that clear sky appears blue (pixels with high NRBR) and clouds appear white or grey (pixels with low NRBR). 

Applying a NRBR threshold works well when the sun is totally shrouded by clouds, but the results are not satisfactory when it is clear sky or when the sun is partially shrouded by clouds (see Figure 2). The alrgorithm misclassifies the circumsolar pixels as cloud pixels because such pixels are often brighter than other areas and have a white or yellow-white character that activates the NRBR threshold. 

![demo_intermittency](/figs/demo_NRBR.png)
<p align=justify>
Figure 2. Cloud detection using NRBR method for different sky conditions: (a) sun entirely shrouded by
clouds; (b) clear sky; and (c) sun partially shrouded by clouds. The pixels are identified as clouds when their NRBR$\leq0.05$. Red pixels in original image indicates the identified sun position. Green pixels in each cloud detection method indicates the identified
cloud pixels.
</p>

 The column ``Fixed threshold method" of Figure \ref{fig:cloud_detection_results} shows the pixels identified as clouds (highlighted with a light green transparent color) for different sky conditions when a fixed NRBR threshold 0.05 is applied. The pixels are identified as clouds when their NRBR$\mathrm{\leq0.05}$. It can be observed that the method works well when the sun is totally shrouded by clouds (see row (C) column ``Fixed threshold method" of Figure \ref{fig:cloud_detection_results}), but the results are not satisfactory when it is clear sky or when the sun is partially shrouded by clouds (see row (A) and (B) column ``Fixed threshold method" of Figure \ref{fig:cloud_detection_results}), mainly due to misclassification of the circumsolar area pixels as clouds.

### CSL

### Our approach

## Demonstration


## Limitations and future work
poor adaptation, parameters need to be tuned for specific dataset. 

Neural network, need labels

## References
<a id="1">[1]</a> 
Chauvin, R., Nou, J., Thil, S., Traore, A. and Grieu, S., 2015. Cloud detection methodology based on a sky-imaging system. Energy Procedia, 69, pp.1970-1980.

<a id="2">[2]</a>
Bohren, C.F. and Huffman, D.R., 2008. Absorption and scattering of light by small particles. John Wiley & Sons.
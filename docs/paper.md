---
title: 'arcesetc: ARC Echelle Spectrograph Exposure Time Calculator'
tags:
  - Python
  - astronomy
  - spectroscopy
authors:
  - name: Brett M. Morris
    orcid: 0000-0003-2528-3409
    affiliation: 1
  - name: Trevor Dorn-Wallenstein
    orcid: 0000-0003-3601-3180
    affiliation: 1
  - name: Emily M. Levesque
    orcid: 0000-0003-2184-1581
    affiliation: 1
  - name: Charli Sakari
    orcid: 0000-0002-5095-4000
    affiliation: 1
  - name: Doug Gies
    orcid: 0000-0001-8537-3583
    affiliation: 2
  - name: Katherine Lester
    orcid: 0000-0002-9903-9911
    affiliation: 2
  - name: Yuta Notsu
    orcid: 0000-0002-0412-0849
    affiliation: 3
  - name: Allison Youngblood
    orcid: 0000-0002-1176-3391
    affiliation: 4
  - name: Russet McMillan
    affiliation: 5

affiliations:
 - name: Astronomy Department, University of Washington, Seattle, WA, USA
   index: 1
 - name: Physics-Astronomy Department, Georgia State University, Atlanta, GA, USA
   index: 2
 - name: Department of Astronomy, Kyoto University, Sakyo Ward, Kyoto, Kyoto Prefecture 606-8501, Japan
   index: 3
 - name: NASA Goddard Space Flight Center, Greenbelt, MD, USA
   index: 4
 - name: Apache Point Observatory
   index: 5
date: 1 Feb 2019
bibliography: paper.bib
--- 

# Summary

The ARC Echelle Spectroscopic (ARCES) Exposure Time Calculator, or ``arcesetc``,
is a simple exposure time calculator for the ARCES instrument on the 
Astrophysical Research Consortium (ARC) 3.5 m Telescope at Apache Point 
Observatory for stellar spectroscopy. Astronomers can use it to plan observations
with the ARCES instrument. Users can supply ``arcesetc`` functions 
with the spectral type of their target star, the V band magnitude, and either: 
the desired exposure time in order to determine the counts and signal-to-noise
ratio as a function of wavelength; or the desired signal-to-noise ratio at a 
given wavelength to determine the required exposure time. 

We estimate the count rates for stars as a function of wavelength by fitting 
15th-order polynomials to each spectral order of real observations of a star of 
each spectral type. These polynomial coefficients and some wavelength metadata
are stored in an HDF5 archive for compactness and ease of reconstruction. Then
upon calling ``arcesetc``, the archive is opened and the spectral order closest
to the wavelength of interest is reconstructed from the polynomial 
coefficients, for a star of the closest available spectral type to the one 
requested. 

At present, the 79 stellar spectral types included in the ``arcesetc`` library
span from mid F to mid M stars on the main sequence, a variety of M giants, 
a handful of O and B, and a white dwarf and a Wolf-Rayet star. Contributions
from the community are welcome to expand the library to include other spectral 
types.

``arcesetc`` was built from the Astropy package-template, and thus includes 
self-building documentation and continuous integration [@astropy:2018].

# Acknowledgements

We acknowledge guidance from Suzanne L. Hawley, and the invaluable 
framework and dev team behind the astropy package-template.

# References

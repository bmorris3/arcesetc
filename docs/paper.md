---
title: 'arcesetc: ARC Echelle Spectroscopic Exposure Time Calculator'
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
affiliations:
 - name: Astronomy Department, University of Washington, Seattle, WA, USA
   index: 1
date: 1 Jan 2019
bibliography: paper.bib
--- 

# Summary

The ARC Echelle Spectroscopic (ARCES) Exposure Time Calculator, or ``arcesetc``,
is a simple exposure time calculator for the ARCES instrument on the 
Astrophysical Research Consortium (ARC) 3.5 m Telescope at Apache Point 
Observatory for stellar spectroscopy. Users can supply ``arcesetc`` functions 
with the spectral type of their target star, the V band magnitude, and either: 
the desired exposure time in order to determine the counts and signal-to-noise
ratio as a function of wavelength; or the desired signal-to-noise ratio at a 
given wavelength to determine the required exposure time. 

We estimate the count rates for stars as a function of wavelength by fitting 
15th-order polynomials to each spectral order of real observations of a star of 
each spectral type. These polynomial coefficients and some wavelength metadata
are stored in an HDF5 archive for compactness and easy of reconstruction. Then
upon calling ``arcesetc``, the archive is opened and the spectral order closest
to the wavelength of interest is reconstructed from the polynomial 
coefficients, for a star of the closest available spectral type to the one 
requested. 

At present, the stellar spectral types included in the ``arcesetc`` library
span from late F to early M stars on the main sequence, and one each of an 
O, B, and Wolf-Rayet star. Contributions from the community are welcome to 
expand the library to include other spectral types.

``arcesetc`` was built from the Astropy package-template, and thus includes 
self-building documentation and continuous integration [@astropy:2018].

# Acknowledgements

We acknowledge guidance from Suzanne L. Hawley and Emily Levesque, and the invaluable 
framework and dev team behind the astropy package-template.

# References

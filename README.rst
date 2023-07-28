Exposure time calculator for APO/ARCES
--------------------------------------

.. image:: https://github.com/bmorris3/arcesetc/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/bmorris3/arcesetc/actions/workflows/ci.yml
   :alt: Testing status

.. image:: https://readthedocs.org/projects/arcesetc/badge/?version=latest
    :target: https://arcesetc.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: http://img.shields.io/pypi/v/arcesetc.svg?text=version
    :target: https://pypi.python.org/pypi/arcesetc/
    :alt: Latest release

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge
    
.. image:: http://joss.theoj.org/papers/10.21105/joss.01130/status.svg
   :target: https://doi.org/10.21105/joss.01130

.. image:: https://zenodo.org/badge/160124540.svg
   :target: https://zenodo.org/badge/latestdoi/160124540

Calculate S/N and exposure times for
stellar spectroscopy with the `ARC Echelle Spectrograph (ARCES)
<https://www.apo.nmsu.edu/arc35m/Instruments/ARCES/>`_ on the
`ARC 3.5 m Telescope <https://www.apo.nmsu.edu/arc35m/>`_ at
`Apache Point Observatory <https://www.apo.nmsu.edu>`_.

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


Installation
------------

You can install ``arcesetc`` with pip::

    pip install arcesetc

You can install ``arcesetc`` from the source code by doing the following::

    git clone https://github.com/bmorris3/arcesetc.git
    cd arcesetc
    pip install .

``arcesetc`` requires python >=3.5, numpy, astropy, h5py, and matplotlib.

For more information, `read the docs <https://arcesetc.readthedocs.io/>`_.

License
-------

This project is Copyright (c) Brett Morris & Trevor Dorn-Wallenstein and licensed under
the terms of the MIT license. This package is based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.

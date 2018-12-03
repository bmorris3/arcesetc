import os
import pytest
import numpy as np
import astropy.units as u
from astropy.io import fits
from specutils.io import read_fits

from ..util import (reconstruct_order, closest_sptype, archive, scale_flux,
                    signal_to_noise_to_exp_time)

path = os.path.dirname(__file__)


class Spectrum1D(object):
    """
    Simple 1D spectrum object; taken from `aesop`.

    A ``Spectrum1D`` object can be used to describe one order of an echelle
    spectrum, for example.

    If the spectrum is initialized with ``wavelength``s that are not strictly
    increasing, ``Spectrum1D`` will sort the ``wavelength``, ``flux`` and
    ``mask`` arrays so that ``wavelength`` is monotonically increasing.
    """
    @u.quantity_input(wavelength=u.Angstrom)
    def __init__(self, wavelength=None, flux=None, name=None, mask=None,
                 wcs=None, meta=dict(), time=None, continuum_normalized=None):
        """
        Parameters
        ----------
        wavelength : `~numpy.ndarray`
            Wavelengths
        flux : `~numpy.ndarray`
            Fluxes
        name : str (optional)
            Name for the spectrum
        mask : `~numpy.ndarray` (optional)
            Boolean mask of the same shape as ``flux``
        wcs : `~specutils.Spectrum1DLookupWCS` (optional)
            Store the WCS parameters
        meta : dict (optional)
            Metadata dictionary.
        continuum_normalized : bool (optional)
            Is this spectrum continuum normalized?
        """

        # Are wavelengths stored in increasing order?
        wl_inc = np.all(np.diff(wavelength) > 0)

        # If not, force them to be, to simplify linear interpolation later.
        if not wl_inc:
            wl_sort = np.argsort(wavelength)
            wavelength = wavelength[wl_sort]
            flux = flux[wl_sort]
            if mask is not None:
                mask = mask[wl_sort]

        self.wavelength = wavelength
        self.wavelength_unit = wavelength.unit
        self.flux = flux if hasattr(flux, 'unit') else u.Quantity(flux)
        self.name = name
        self.mask = mask
        self.wcs = wcs
        self.meta = meta
        self.time = time
        self.continuum_normalized = continuum_normalized

    @classmethod
    def from_specutils(cls, spectrum1d, name=None, **kwargs):
        """
        Convert a `~specutils.Spectrum1D` object into our Spectrum1D object.

        Parameters
        ----------
        spectrum1d : `~specutils.Spectrum1D`
            Input spectrum
        name : str
            Target/spectrum name
        """
        return cls(wavelength=spectrum1d.wavelength, flux=spectrum1d.flux,
                   mask=spectrum1d._mask, name=name, **kwargs)


@pytest.mark.parametrize("order", [35, 41, 60])
def test_reconstruct_order(order):
    """
    End-to-end functional test on several well-behaved orders of an early-type
    star.
    """

    fits_path = os.path.join(path, os.pardir, 'data', 'HR3454.0016.wfrmcpc.fits')

    b3v = [Spectrum1D.from_specutils(s)
           for s in read_fits.read_fits_spectrum1d(fits_path)]
    header = fits.getheader(fits_path)

    wave, flux, sp_type, exp_time = reconstruct_order('B3V',
                                                      b3v[order].wavelength.mean(),
                                                      4.3,
                                                      exp_time=header['EXPTIME']*u.s)

    interp_flux = np.interp(b3v[order].wavelength, wave, flux)
    np.testing.assert_allclose(b3v[order].flux, interp_flux, atol=500, rtol=1e-1)
    assert sp_type == 'B3V'


def test_closest_sptype():
    """Test that package finds closest available sptype"""
    assert closest_sptype('G4V') == 'G5V'


def test_scale_flux():
    """
    Check that the flux scaling is workign appropriately by inputting the actual
    magnitude of a particular star, show that it returns flux scaling == 1
    """
    assert np.abs(scale_flux(archive['HR 3454'], V=4.3) - 1) < 1e-6


def test_sn_to_exptime():
    """
    Check that the plot-less function works appropriately.
    """
    sptype = 'M0V'
    wavelength = 6562 * u.Angstrom
    signal_to_noise = 30
    V = 12
    exp_time = signal_to_noise_to_exp_time(sptype, wavelength, V,
                                           signal_to_noise)
    assert np.abs(exp_time.to(u.s).value - 642.11444) < 1e-2

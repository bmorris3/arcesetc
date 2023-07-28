import os

import astropy.units as u
import numpy as np
import pytest
from astropy.io import fits
from specutils import SpectrumCollection

from ..util import (reconstruct_order, closest_sptype, archive, scale_flux,
                    signal_to_noise_to_exp_time)

path = os.path.dirname(__file__)


@pytest.mark.parametrize("order,", [30, 35, 41, 60, 65, 70, 75, 80, 90])
def test_reconstruct_order_B3V(order):
    """
    End-to-end functional test on several well-behaved orders of an early-type
    star.
    """

    fits_path = os.path.join(path, os.pardir, 'data',
                             'HR5191.0002.wfrmcpc.fits')

    b3v = SpectrumCollection.read(fits_path)
    header = fits.getheader(fits_path)

    # Reconstruct the order for a star with the same V mag as the template
    wave, flux, sp_type, exp_time = reconstruct_order('B3V',
                                                      b3v[order].wavelength.mean(),
                                                      1.86,
                                                      exp_time=header['EXPTIME']*u.s)

    interp_flux = np.interp(b3v[order].wavelength, wave, flux)
    np.testing.assert_allclose(b3v[order].flux.value, interp_flux, atol=500, rtol=1e-1)
    assert sp_type == 'B3V'


@pytest.mark.parametrize("order", [30, 35, 41, 60, 65, 70, 75, 80, 90])
def test_reconstruct_order_white_dwarf(order):
    """
    End-to-end functional test on several well-behaved orders of a white dwarf
    """

    fits_path = os.path.join(path, os.pardir, 'data',
                             'BD28_4211.0026.wfrmcpc.fits')

    wd = SpectrumCollection.read(fits_path)
    header = fits.getheader(fits_path)

    # Reconstruct the order for a star with the same V mag as the template

    wave, flux, sp_type, exp_time = reconstruct_order('sdO2VIIIHe5',
                                                      wd[order].wavelength.mean(),
                                                      10.58,
                                                      exp_time=header['EXPTIME']*u.s)

    interp_flux = np.interp(wd[order].wavelength, wave, flux)
    np.testing.assert_allclose(wd[order].flux.value, interp_flux, atol=500, rtol=0.05)
    assert sp_type == 'sdO2VIIIHe5'


@pytest.mark.parametrize("order", [30, 35, 41, 60, 65, 75, 80])
def test_reconstruct_order_white_dwarf_2(order):
    """
    End-to-end functional test on several well-behaved orders of a white dwarf
    """

    fits_path = os.path.join(path, os.pardir, 'data',
                             'HIP107864.0003.wfrmcpc.fits')

    wd = SpectrumCollection.read(fits_path)
    header = fits.getheader(fits_path)

    # Reconstruct the order for a star with the same V mag as the template

    wave, flux, sp_type, exp_time = reconstruct_order('sdO2VIIIHe5',
                                                      wd[order].wavelength.mean(),
                                                      10.58,
                                                      exp_time=header['EXPTIME']*u.s)

    interp_flux = np.interp(wd[order].wavelength, wave, flux)
    np.testing.assert_allclose(wd[order].flux.value, interp_flux, atol=500, rtol=0.2)
    assert sp_type == 'sdO2VIIIHe5'


def test_closest_sptype():
    """Test the function that finds closest available sptype"""
    assert closest_sptype('G4V') == 'G5V'
    assert closest_sptype('B4V') == 'B3V'


def test_scale_flux():
    """
    Check that the flux scaling is working appropriately by inputting the actual
    magnitude of a particular star, show that it returns flux scaling == 1
    """
    assert np.abs(scale_flux(archive['HR 3454'], V=4.3) - 1) < 1e-6
    assert np.abs(scale_flux(archive['HR5191'], V=1.86) - 1) < 1e-6


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

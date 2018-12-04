import os

import astropy.units as u
import numpy as np
import pytest
from astropy.io import fits

from .legacy_specutils import readspec
from ..util import (reconstruct_order, closest_sptype, archive, scale_flux,
                    signal_to_noise_to_exp_time)

path = os.path.dirname(__file__)


@pytest.mark.parametrize("order", [35, 41, 60])
def test_reconstruct_order(order):
    """
    End-to-end functional test on several well-behaved orders of an early-type
    star.
    """

    fits_path = os.path.join(path, os.pardir, 'data', 'HR3454.0016.wfrmcpc.fits')

    b3v = readspec.read_fits_spectrum1d(fits_path)
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

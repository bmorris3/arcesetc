from json import load
from difflib import get_close_matches
import os
import numpy as np
import h5py
import astropy.units as u

__all__ = ['available_sptypes', 'signal_to_noise_to_exp_time',
           'reconstruct_order']

directory = os.path.dirname(__file__)

sptypes = load(open(os.path.join(directory, 'data', 'sptype_dict.json'), 'r'))
archive = h5py.File(os.path.join(directory, 'data', 'archive.hdf5'), 'r')

sptype_to_temp = load(open(os.path.join(directory, 'data',
                                        'sptype_to_temp.json'), 'r'))
spectral_types = [key for key in sptype_to_temp.keys() if key in sptypes]
temps = np.array([sptype_to_temp[key] for key in spectral_types
                  if key in sptype_to_temp])


def closest_sptype(sptype):
    """
    Return closest spectral type in the archive.
    
    If ``sptype`` is a dwarf star of spectral class V and
    the exact spectral type is not present in the archive,
    return the star with the closest spectral type to the 
    input spectral type. 

    Parameters
    ----------
    sptype : str
        Spectral type in the format: ``G2V``.

    Returns
    -------
    closest_spectral_type : str
        Closest spectral type available in the archive.
    """
    if sptype in sptypes:
        return sptype
    elif len(sptype) == 3 and sptype.endswith("V"):
        return spectral_types[np.argmin(np.abs(sptype_to_temp[sptype] - temps))]
    else:
        raise ValueError("We don't have a match to this spectral type. The "
                         "nearest ones we have on hand are: {0}"
                         .format(get_close_matches(sptype, available_sptypes())))


def closest_target(sptype):
    """
    Return target with the closest spectral type in the archive.

    Parameters
    ----------
    sptype : str
        Spectral type in the format: ``G2V``.

    Returns
    -------
    target_name : str
        Name of the target closest to spectral type ``sptype``.
    closest_spectral_type : str
        Closest spectral type available in the archive.
    """
    closest_spectral_type = closest_sptype(sptype)
    return sptypes[closest_spectral_type], closest_spectral_type


def available_sptypes():
    """
    Return a list of available spectral types in the archive.

    Returns
    -------
    sptypes : list
        List of available spectral types.
    """
    return sorted(sptypes.keys())


def get_closest_order(matrix, wavelength):
    """
    Return the spectral order index closest to wavelength ``wavelength``.

    Parameters
    ----------
    matrix : `~np.ndarray`
        Matrix of blaze function curves from the archive.
    wavelength : `~astropy.units.Quantity`
        Wavelength of interest.

    Returns
    -------
    closest_order : int
        Closest spectral order to wavelength ``wavelength``.
    """
    return np.argmin(np.abs(matrix[:, 0] - wavelength.to(u.Angstrom).value))


def matrix_row_to_spectrum(matrix, closest_order):
    """
    Given a ``matrix`` from the archive and a spectral order index
    ``closest_order``, return the spectrum (wavelength and flux).

    Parameters
    ----------
    matrix : `~np.ndarray`
        Matrix of blaze function curves from the archive.
    closest_order : int
        Closest spectral order to wavelength ``wavelength``.

    Returns
    -------
    wave : `~astropy.units.Quantity`
        Wavelengths.
    flux : `~np.ndarray`
        Fluxes in counts per second at each wavelength.
    """
    lam_0, delta_lam, n_lam = matrix[closest_order][:3]
    polynomial_coeffs = matrix[closest_order][3:]
    wave = np.arange(lam_0 - n_lam*delta_lam/2, lam_0 + n_lam*delta_lam/2,
                     delta_lam)
    flux = np.polyval(polynomial_coeffs, wave-lam_0)
    return wave * u.Angstrom, flux


def scale_flux(dataset, V):
    """
    Parameters
    ----------
    dataset : `~h5py.File.dataset`
        h5py dataset of the form ``archive[target]``.
    V : float
        V magnitude of the target of interest.
    """
    template_vmag = dataset.attrs['V'][0]
    magnitude_scaling = 10**(0.4 * (template_vmag - V))
    return magnitude_scaling


def sn_to_exp_time(wave, flux, wavelength, signal_to_noise):
    """
    Calculate the required exposure time to achieve signal-to-noise ratio
    ``signal_to_noise`` given the count rates ``flux`` as a function of
    wavelength ``wave``.

    Parameters
    ----------
    wave : `~astropy.units.Quantity`
        Wavelengths.
    flux : `~np.ndarray`
        Flux in counts per second.
    wavelength : `~astropy.units.Quantity`
        Wavelength of interest at which the S/N is ``signal_to_noise``.
    signal_to_noise : float
        Desired signal-to-noise.

    Returns
    -------
    exp_time : `~astropy.units.Quantity`
        Exposure time that will yield signal-to-noise ``signal_to_noise`` at
        wavelength ``wavelength``.
    """

    # `flux` at the test wavelength
    flux_0 = flux[np.argmin(np.abs(wave - wavelength))]
    exp_time = signal_to_noise**2 / flux_0
    return exp_time * u.s


@u.quantity_input(exp_time=u.s, wavelength=u.Angstrom)
def reconstruct_order(sptype, wavelength, V, exp_time=None,
                      signal_to_noise=None):
    """
    Return the counts as a function of wavelength for the spectral
    order nearest to ``wavelength`` for a star of spectral type ``sptype`` and
    V magnitude ``V``.

    Either ``exp_time`` or ``signal_to_noise`` should be supplied to the
    function (but not both).

    .. warning ::
        ``arcesetc`` doesn't know anything about saturation. Ye be warned!

    Parameters
    ----------
    sptype : str
        Spectral type of the star.
    wavelength : `~astropy.units.Quantity`
    V : float
        V magnitude of the target.
    exp_time : None or float
        If ``exp_time`` is a float, show the counts curve for that exposure
        time. Otherwise, use ``signal_to_noise`` to compute the appropriate
        exposure time.
    signal_to_noise : None or float
        If ``signal_to_noise`` is a float, compute the appropriate exposure time
        to generate the counts curve that has S/N = ``signal_to_noise`` at
        wavelength ``wavelength``. Otherwise, generate counts curve for
        exposure time ``exp_time``.

    Returns
    -------
    wave : `~astropy.units.Quantity`
        Wavelengths.
    flux : `~np.ndarray`
        Flux at each wavelength.
    exp_time : `~astropy.units.Quantity`
        Exposure time input; or required to reach S/N of ``signal_to_noise``.
    """

    target, closest_spectral_type = closest_target(sptype)

    matrix = archive[target][:]

    closest_order = get_closest_order(matrix, wavelength)
    wave, flux = matrix_row_to_spectrum(matrix, closest_order)
    flux *= scale_flux(archive[target], V)

    if exp_time is not None and signal_to_noise is None:
        flux *= exp_time.to(u.s).value

    elif exp_time is None and signal_to_noise is not None:
        exp_time = sn_to_exp_time(wave, flux, wavelength, signal_to_noise)
        flux *= exp_time.value
    else:
        raise ValueError("Supply either the `exp_time` or the "
                         "`signal_to_noise` keyword argument.")
    return wave, flux, closest_spectral_type, exp_time


@u.quantity_input(exp_time=u.s, wavelength=u.Angstrom)
def signal_to_noise_to_exp_time(sptype, wavelength, V, signal_to_noise):
    """
    Compute the exposure time required to collect signal-to-noise ratio
    ``signal_to_noise`` at wavelength ``wavelength`` for a star of spectral type
    ``sptype`` and V magnitude ``V``.

    .. warning ::
        ``arcesetc`` doesn't know anything about saturation. Ye be warned!

    Parameters
    ----------
    sptype : str
        Spectral type of the star.
    wavelength : `~astropy.units.Quantity`
        Wavelength of interest.
    V : float
        V magnitude of the target.
    signal_to_noise : float
        If ``signal_to_noise`` is a float, compute the appropriate exposure time
        to generate the S/N curve that has S/N = ``signal_to_noise`` at
        wavelength ``wavelength``. Otherwise, generate S/N curve for
        exposure time ``exp_time``.

    Returns
    -------
    exp_time : `~astropy.units.Quantity`
        Exposure time input, or computed to achieve S/N ratio
        ``signal_to_noise`` at wavelength ``wavelength``.

    Examples
    --------

    How many seconds must one expose ARCES on a V=12 mag M0V star to get a S/N
    of 30 at the wavelength of H-alpha?

    >>> from arcesetc import signal_to_noise_to_exp_time
    >>> import astropy.units as u
    >>> sptype = 'M0V'
    >>> wavelength = 6562 * u.Angstrom
    >>> signal_to_noise = 30
    >>> V = 12
    >>> print(signal_to_noise_to_exp_time(sptype, wavelength, V, signal_to_noise)) # doctest: +FLOAT_CMP
    642.11444 s
    """
    target, closest_spectral_type = closest_target(sptype)

    matrix = archive[target][:]

    closest_order = get_closest_order(matrix, wavelength)
    wave, flux = matrix_row_to_spectrum(matrix, closest_order)
    flux *= scale_flux(archive[target], V)

    exp_time = sn_to_exp_time(wave, flux, wavelength, signal_to_noise)
    return exp_time

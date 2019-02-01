import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from .util import reconstruct_order

__all__ = ['plot_order_counts', 'plot_order_sn']


@u.quantity_input(exp_time=u.s, wavelength=u.Angstrom)
def plot_order_counts(sptype, wavelength, V, exp_time=None,
                      signal_to_noise=None, **kwargs):
    """
    Plot the counts as a function of wavelength for the spectral
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
    kwargs : dict
        All extra keyword arguments will be passed to the plot function.

    Returns
    -------
    fig : `~matplotlib.pyplot.Figure`
        Matplotlib figure object.
    ax : `~matplotlib.pyplot.Axes`
        Matplotlib axes object.
    exp_time : `~astropy.units.Quantity`
        Exposure time input, or computed to achieve S/N ratio
        ``signal_to_noise`` at wavelength ``wavelength``.

    Examples
    --------

    Given an exposure time:

    >>> import matplotlib.pyplot as plt
    >>> import astropy.units as u
    >>> from arcesetc import plot_order_counts
    >>> sptype = 'G4V'
    >>> wavelength = 6562 * u.Angstrom
    >>> exp_time = 30 * u.min
    >>> V = 10
    >>> fig, ax, exp_time = plot_order_counts(sptype, wavelength, V, exp_time=exp_time) #doctest: +SKIP
    >>> plt.show() #doctest: +SKIP

    ...or given a desired signal-to-noise ratio:

    >>> import matplotlib.pyplot as plt
    >>> import astropy.units as u
    >>> from arcesetc import plot_order_counts
    >>> sptype = 'G4V'
    >>> wavelength = 6562 * u.Angstrom
    >>> signal_to_noise = 30
    >>> V = 10
    >>> fig, ax, exp_time = plot_order_counts(sptype, wavelength, V, signal_to_noise=signal_to_noise) #doctest: +SKIP
    >>> plt.show() #doctest: +SKIP

    """

    wave, flux, closest_sptype, exp_time = reconstruct_order(sptype,
                                                             wavelength,
                                                             V,
                                                             exp_time=exp_time,
                                                             signal_to_noise=signal_to_noise)

    fig, ax = plt.subplots()

    ax.set_title('Sp. Type: {0}, Exposure time: {1:.1f}'
                 .format(closest_sptype, exp_time.to(u.min)))
    ax.plot(wave, flux, **kwargs)
    ax.set_xlabel('Wavelength [Angstrom]')
    ax.set_ylabel('Flux [DN]')
    for s in ['right', 'top']:
        ax.spines[s].set_visible(False)
    ax.grid(ls=':', color='silver')
    return fig, ax, exp_time


@u.quantity_input(exp_time=u.s, wavelength=u.Angstrom)
def plot_order_sn(sptype, wavelength, V, exp_time=None, signal_to_noise=None,
                  **kwargs):
    """
    Plot the signal-to-noise ratio as a function of wavelength for the spectral
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
        If ``exp_time`` is a float, show the S/N curve for that exposure time.
        Otherwise, use ``signal_to_noise`` to compute the appropriate exposure
        time.
    signal_to_noise : None or float
        If ``signal_to_noise`` is a float, compute the appropriate exposure time
        to generate the S/N curve that has S/N = ``signal_to_noise`` at
        wavelength ``wavelength``. Otherwise, generate S/N curve for
        exposure time ``exp_time``.
    kwargs : dict
        All extra keyword arguments will be passed to the plot function.

    Returns
    -------
    fig : `~matplotlib.pyplot.Figure`
        Matplotlib figure object.
    ax : `~matplotlib.pyplot.Axes`
        Matplotlib axes object.
    exp_time : `~astropy.units.Quantity`
        Exposure time input, or computed to achieve S/N ratio
        ``signal_to_noise`` at wavelength ``wavelength``.

    Examples
    --------

    Given an exposure time:

    >>> import matplotlib.pyplot as plt
    >>> import astropy.units as u
    >>> from arcesetc import plot_order_sn
    >>> sptype = 'G4V'
    >>> wavelength = 6562 * u.Angstrom
    >>> exp_time = 30 * u.min
    >>> V = 10
    >>> fig, ax, exp_time = plot_order_sn(sptype, wavelength, V, exp_time=exp_time) #doctest: +SKIP
    >>> plt.show() #doctest: +SKIP

    ...or given a desired signal-to-noise ratio:

    >>> import matplotlib.pyplot as plt
    >>> import astropy.units as u
    >>> from arcesetc import plot_order_sn
    >>> sptype = 'G4V'
    >>> wavelength = 6562 * u.Angstrom
    >>> signal_to_noise = 30
    >>> V = 10
    >>> fig, ax, exp_time = plot_order_sn(sptype, wavelength, V, signal_to_noise=signal_to_noise) #doctest: +SKIP
    >>> plt.show() #doctest: +SKIP
    """

    fig, ax = plt.subplots()

    wave, flux, closest_sptype, exp_time = reconstruct_order(sptype,
                                                             wavelength,
                                                             V,
                                                             exp_time=exp_time,
                                                             signal_to_noise=signal_to_noise)
    sn = flux / np.sqrt(flux)
    ax.set_title('Sp. Type: {0}, Exposure time: {1:.1f}'
                 .format(closest_sptype, exp_time.to(u.min)))
    ax.plot(wave, sn, **kwargs)
    ax.set_xlabel('Wavelength [Angstrom]')
    ax.set_ylabel('Signal/Noise')
    for s in ['right', 'top']:
        ax.spines[s].set_visible(False)
    ax.grid(ls=':', color='silver')
    return fig, ax, exp_time


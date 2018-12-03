Next steps
==========

No plots, just exposure times
-----------------------------

You can also calculate the exposure time required to obtain a given S/N using
the `~arcesetc.signal_to_noise_to_exp_time` function. For example - how many
seconds must one expose ARCES on a V=12 mag M0V star to get a S/N of 30 at the
wavelength of H-alpha::

    from arcesetc import signal_to_noise_to_exp_time
    sptype = 'M0V'
    wavelength = 6562 * u.Angstrom
    signal_to_noise = 30
    V = 12
    print(signal_to_noise_to_exp_time(sptype, wavelength, V, signal_to_noise))

This returns ``642.11444 s``, a `~astropy.units.Quantity` object containing the
required exposure time.

Available spectral types
------------------------

You can see which spectral types are available with the
`~arcesetc.available_sptypes` function.

.. warning::
    At present, the best coverage is for late-F through early-M type main
    sequence stars.
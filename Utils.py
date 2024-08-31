import numpy as np


def create_time_scale(n_samples, sf, unit='s'):
    """
    Create a one-dimensional time scale for a signal.

    Parameters
    ----------
    n_samples : int
        Total number of samples in the signal for which the time scale has to be created.
    sf : int
        Sampling frequency of the signal, i.e., the number of samples per second.
    unit : str, optional
        Time unit in which the time scale has to be expressed.
        Available units: 'h' (hours), 'min' (minutes), 's' (seconds), 'ms' (milliseconds),
        'us' (microseconds), 'ns' (nanoseconds). Default value is 's'.

    Returns
    -------
    time_scale : 1D np.ndarray
        One-dimensional time scale with values expressed in the specified time unit.

    Raises
    ------
    ValueError
        If the input parameters are of incorrect type or have inappropriate values.
    """

    # Validate input parameters
    if not isinstance(n_samples, int) or not isinstance(sf, int):
        raise ValueError("`n_samples` and `sf` must be integers.")

    if unit not in ['h', 'min', 's', 'ms', 'us', 'ns']:
        raise ValueError(
            "`unit` must be one of the following: 'h', 'min', 's', 'ms', 'us', 'ns'.")

    # Unit conversion factors
    unit_conversion = {
        'h': 3600,  # hours to seconds
        'min': 60,  # minutes to seconds
        's': 1,  # seconds to seconds
        'ms': 1e-3,  # milliseconds to seconds
        'us': 1e-6,  # microseconds to seconds
        'ns': 1e-9  # nanoseconds to seconds
    }

    # Compute total time in the specified unit
    total_time_in_unit = (n_samples / sf) / unit_conversion[unit]
    # Compute time step in the specified unit
    dt = (1 / sf) / unit_conversion[unit]

    # Create time scale using numpy arange
    time_scale = np.arange(0, total_time_in_unit, dt)

    return time_scale

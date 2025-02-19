from scipy import signal as scisig
import scipy.fftpack as scifft
import os
from itertools import chain
import numpy as np
import xml.etree.ElementTree as ET
import math
import pandas as pd

# ARTIFACTS REMOVAL
def remove_current_pulse_artifacts(sig, markers, window, n_draws, return_artifacts=False):
    """Remove current pulse artifacts from one-dimensional signal based on artifacts occurences represented
    by one-dimensional markers signal. Current pulse artifacts removal is performed in following steps:
    1. Extract current pulse artifacts from 'sig' based on 'markers' which contains ones and zeros, whereas ones
    indicate current pulse artifact occurences.
    2. Extraction is performed around the artifact occurence in accordance to range described by 'window'.
    3. Extracted artifacts are stored in two-dimensional numpy.ndarray.
    4. We draw from stored artifacts 'n_draws' without repetition and average them in order to get averaged
    representation of current pulse artifact.
    5. We substract this averaged artifact representation from the first occurence of the artifact in 'sig'.
    6. We now repeat steps 4 and 5 for all next subsequent artifact occurences in 'sig'.

    Parameters
    ----------
    sig : 1D numpy.ndarray
        One-dimensional signal with the occurences of current pulse artifacts.
    markers : 1D numpy.ndarray
        One-dimensional signal consisted of ones and zeros, where ones correspond to the exact sample occurences
        of current pulse artifact in 'sig'. That's why 'markers'.size' must equal to 'sig.size'.
    window : list of int of length 2
        List consisted of two values describing sample range (window) of the current pulse artifact around
        its occurence.
    n_draws : int
        Number of draws from the collection of stored artifacts. Must be >= 1.
    return_artifacts : boolean
        If True, beside of cleared signal, function will return also collection of the stored artifacts. Default value
        is False.

    Returns
    -------
    cleared : 1D numpy.ndarray
        Cleared signal.
    artifacts : 2D numpy.ndarray
        Collection of the stored artifacts.
    """
    if (isinstance(sig, np.ndarray) and sig.ndim == 1 and isinstance(markers, np.ndarray) and markers.ndim == 1
            and ndarray_contains_only(markers, np.array([0, 1])) and sig.size == markers.size and len(window) in range(
                1, 3)
            and list_is_int(window) and isinstance(n_draws, int) and n_draws >= 1):

        # Extract artifacts.
        artifacts = []
        iterator = 0
        for marker in markers:
            if marker == 1:
                artifacts.append(sig[iterator - window[0]:iterator + window[1]])
            iterator += 1
        artifacts = np.asarray(artifacts)

        # Remove artifacts from the signal.
        iterator = 0
        for marker in markers:
            if marker == 1:

                if n_draws > np.shape(artifacts)[0]:
                    n_draws = np.shape(artifacts)[0]

                random_artifact_indices = np.random.choice(np.arange(np.shape(artifacts)[0]), n_draws, replace=False)
                avg_artifact = np.mean(np.take(artifacts, random_artifact_indices, axis=0), axis=0)
                sig[iterator - window[0]:iterator + window[1]] -= avg_artifact
            iterator += 1
        cleared = sig

        # Return cleared signal and extracted artifacts.
        if return_artifacts:
            return cleared, artifacts
        else:
            return cleared
    else:
        raise ValueError(
            "Inappropriate type or value of one of the arguments. Please read carefully function docstring.")


# EXPLORATION AND MARKING
def mark_photodiode_changes(sig, threshold, wait_n_samples, direction='left-to-right'):
    """Create one-dimensional array of zeros and ones, where ones indicate places where photodiode signal exceeds some
    specific threshold value. This one-dimensional array is the same length as photodiode signal.

    Parameters
    ----------
    sig : 1D numpy.ndarray
        Photodiode signal.
    threshold : float
        Threshold value above which photodiode signal will be marked.
    wait_n_samples : int
        Wait n samples after last marker before trying to put next marker. Must be >= 0.
    direction : str
        Direction in which photodiode signal course will be analyzed and marked. There are three directions, ie.
        'left-to-right', 'right-to-left', 'both'. In case of 'both' photodiode signal course will be first analyzed
        'left-to-right' and than 'right-to-left'. Default value is 'left-to-right'.

    Returns
    -------
    markers : 1D numpy.ndarray
        Array of zeros and ones, where ones are markers.
    """
    if (isinstance(sig, np.ndarray) and sig.ndim == 1 and isinstance(threshold, float) and isinstance(wait_n_samples,
                                                                                                      int) and wait_n_samples >= 0 and direction in [
        'left-to-right', 'right-to-left', 'both']):
        if direction == 'left-to-right':
            markers = np.zeros(len(sig))
            wait_until_next_mark = wait_n_samples
            iterator = 0
            for sample in sig:
                if sample > threshold and wait_until_next_mark >= wait_n_samples:
                    markers[iterator] = 1
                    wait_until_next_mark = 0
                iterator += 1
                wait_until_next_mark += 1
            return markers
        elif direction == 'right-to-left':
            markers = np.zeros(len(sig))
            iterator = len(sig) - 1
            wait_until_next_mark = wait_n_samples
            for sample in reversed(sig):
                if sample > threshold and wait_until_next_mark >= wait_n_samples:
                    markers[iterator] = 1
                    wait_until_next_mark = 0
                iterator -= 1
                wait_until_next_mark += 1
            return markers
        else:
            markers_left_to_right = mark_photodiode_changes(sig, threshold, wait_n_samples, direction='left-to-right')
            markers_right_to_left = mark_photodiode_changes(sig, threshold, wait_n_samples, direction='right-to-left')
            markers = markers_left_to_right + markers_right_to_left
            return markers
    else:
        raise ValueError(
            "Inappropriate type, shape or value of one of the arguments. Please read carefully function docstring.")


# FILTERING, SMOOTHING, UP- AND DOWNSAMPLING
def downsample(sig, d_factor):
    """Downsample one-dimensional signal with the use of reshaping.

    Parameters
    ----------
    sig : 1D numpy.ndarray
        One-dimensional signal for downsampling.
    d_factor : int, range(1, inf)
        Downsampling factor. Must be higher than 0.

    Returns
    -------
    d_sig : 1D numpy.ndarray
        One-dimensional signal downsampled lineary by factor equal to 'd_factor'.
    """
    if (isinstance(sig, np.ndarray) and sig.ndim == 1 and isinstance(d_factor, int) and d_factor >= 1):
        d_sig = sig.reshape(-1, d_factor).mean(axis=1)
        return d_sig
    else:
        raise ValueError(
            "Inappropriate type, shape or value of one of the arguments. Please read carefully function docstring.")


def filtfilt_butterworth(sig, sf, cf, order=1, btype='bandpass'):
    """Two-sided Butterworth filter.

    Parameters
    ----------
    sig : numpy.ndarray
        Signal to filter.
    sf : float
        Signal sampling frequecy (number of samples per second).
    cf : float | list of float of length 2
        Filter frequencies. When using btype 'lowpass' or 'highpass' use single float. When using btype 'bandstop'
        or 'bandpass' use list of float of length 2.
    order : int in range of 1-5.
        Order of the filter. Default value is 1.
    btype : str
        One of the four filter types, ie. 'lowpass', 'highpass', 'bandstop', 'bandpass'. Default value is 'bandpass'.

    Returns
    -------
    filtered : numpy.ndarray
        Filtered sig.
    """
    # if (isinstance(sig, np.ndarray) and isinstance(sf, float) and sf > 0 and isinstance(cf, list)
    #         and len(cf) in range(1, 3) and isinstance(order, int) and order in range(1, 6)
    #         and btype in ['lowpass', 'highpass', 'bandstop', 'bandpass']):

    if True:

        if btype == 'highpass' or btype == 'lowpass':
            b, a = scisig.butter(order, Wn=cf / (0.5 * sf), btype=btype, analog=0, output='ba')
            return scisig.filtfilt(b, a, sig)
        elif btype == 'bandstop' or btype == 'bandpass':
            b, a = scisig.butter(order, Wn=(cf[0] / (0.5 * sf), cf[1] / (0.5 * sf)), btype=btype, analog=0, output='ba')
            return scisig.filtfilt(b, a, sig)
    else:
        raise ValueError(
            "Inappropriate type or value of one of the arguments. Please read carefully function docstring.")


def upsample(sig, i_factor):
    """Upsample one-dimensional signal with the use of linear interpolation.

    Parameters
    ----------
    sig : 1D numpy.ndarray
        One-dimensional signal for interpolation.
    i_factor : int, range(1, inf)
        Interpolation factor. Must be higher than 0.

    Returns
    -------
    i_sig : 1D numpy.ndarray
        One-dimensional signal interpolated lineary by factor equal to 'i_factor'.
    """
    if (isinstance(sig, np.ndarray) and sig.ndim == 1 and isinstance(i_factor, int) and i_factor >= 1):
        x = np.linspace(0, sig.size, sig.size)
        y = sig
        i_x = np.linspace(0, sig.size, sig.size * i_factor)
        i_y = np.interp(i_x, x, y)
        i_sig = i_y
        return i_sig
    else:
        raise ValueError(
            "Inappropriate type, shape or value of one of the arguments. Please read carefully function docstring.")


# MUTUAL INFORMATION
def shannon_entropy(data):
    """Calculate Shannon's entropy.

    Parameters
    ----------
    data : 1D numpy.ndarray
        Discrete data serie.

    Returns
    -------
    shannon_entropy : 1D numpy.ndarray
        Shanon entropy.
    """
    hist, _ = np.histogram(data)
    probability = hist / hist.sum()
    return -np.sum(probability * np.log2(probability))


# SIGNAL CREATION
def create_sawtooth_pulse(freq, sf, amp, first_peak='positive'):
    """Create one-period sawtooth pulse.

    Parameters
    ----------
    freq : float
        Frequency of the pulse wave in Hz. Must be > 0.
    sf : int
        Sampling frequency of the pulse (number of samples per second). Must be > 0.
    amp : float
        Amplitude of the pulse in microamperes (uA). Must be > 0.
    first_peak : str
        Polarity of the first pulse hillock. Available options: 'positive', 'negative'. Default value is 'positive'.

    Returns
    -------
    pulse : 1D numpy.ndarray
        One-period sawtooth pulse.
    """
    if (isinstance(freq, float) and freq > 0 and isinstance(sf, int) and sf > 0 and isinstance(amp, float)
            and amp > 0 and first_peak in ['positive', 'negative']):

        duration = 1 / freq
        time_scale = np.arange(0, duration, 1 / sf)
        pulse = scisig.sawtooth(2 * np.pi * freq * time_scale) * (amp / 2)
        if first_peak == 'negative':
            pulse *= -1
        return pulse
    else:
        raise ValueError(
            "Inappriopriate type or value of one of the arguments. Please read carefully function docstring.")


def create_sin_pulse(freq, sf, amp, first_peak='positive'):
    """Create one-period sinusoidal pulse.

    Parameters
    ----------
    freq : float
        Frequency of the pulse wave in Hz. Must be > 0.
    sf : int
        Sampling frequency of the pulse (number of samples per second). Must be > 0.
    amp : float
        Amplitude of the pulse in microapers (uA). Must be > 0.
    first_peak : str
        Polarity of the first pulse hillock. Available options: 'positive', 'negative'. Default value is 'positive'.

    Returns
    -------
    pulse : 1D numpy.ndarray
        One-period sinusoidal pulse.
    """
    if (isinstance(freq, float) and freq > 0 and isinstance(sf, int) and sf > 0 and isinstance(amp, float)
            and amp > 0 and first_peak in ['positive', 'negative']):

        duration = 1 / freq
        time_scale = np.arange(0, duration, 1 / sf)
        pulse = np.sin(2 * np.pi * freq * time_scale) * (amp / 2)
        if first_peak == 'negative':
            pulse *= -1
        return pulse
    else:
        raise ValueError(
            "Inappriopriate type or value of one of the arguments. Please read carefully function docstring.")


def create_square_pulse(freq, sf, amp, first_peak='positive'):
    """Create one-period square pulse.

    Parameters
    ----------
    freq : float
        Frequency of the pulse wave in Hz. Must be > 0.
    sf : int
        Sampling frequency of the pulse (number of samples per second). Must be > 0.
    amp : float
        Amplitude of the pulse in microamperes (uA). Must be > 0.
    first_peak : str
        Polarity of the first pulse hillock. Available options: 'positive', 'negative'. Default value is 'positive'.

    Returns
    -------
    pulse : 1D numpy.ndarray
        One-period squarewave pulse.
    """
    if (isinstance(freq, float) and freq > 0 and isinstance(sf, int) and sf > 0 and isinstance(amp, float)
            and amp > 0 and first_peak in ['positive', 'negative']):

        duration = 1 / freq
        time_scale = np.arange(0, duration, 1 / sf)
        pulse = scisig.square(2 * np.pi * freq * time_scale) * (amp / 2)
        if first_peak == 'negative':
            pulse *= -1
        return pulse
    else:
        raise ValueError(
            "Inappropriate type or value of one of the arguments. Please read carefully function docstring.")


def create_alternating_signal(duration, sf, freq, amp, s_type='sinusoidal', first_peak='positive'):
    """Create one-dimensional alternating signal using sawtooth, sinusoidal or square wave.

    Parameters
    ----------
    duration : float
        Duration of the signal in seconds. Must be > 0.
    sf : int
        Sampling frequency of the pulse (number of samples per second). Must be > 0.
    freq : float
        Frequency of the signal in Hz.
    amp : float
        Amplitude of the pulse in microampers (uA). Must be > 0.
    s_type : str
        Type of the wave used in the signal creation. Available types: 'sawtooth', sinusoidal', 'square'.
        Default value is 'sinusoidal'.
    first_peak : str
        Polarity of the first pulse hillock. Available options: 'positive', 'negative'. Default value is 'positive'.

    Returns
    -------
    sig : 1D numpy.ndarray
        Created one-dimensional alternating signal.
    """
    if (isinstance(duration, float) and duration > 0 and isinstance(sf, int) and sf > 0 and isinstance(freq, float)
            and freq > 0 and isinstance(amp, float) and amp > 0 and s_type in ['sawtooth', 'sinusoidal', 'square']
            and first_peak in ['positive', 'negative'] and duration * sf >= 1):

        temp_sig = []
        pulse_time_in_s = 1.0 / freq
        n_pulses = int(math.ceil(duration / pulse_time_in_s))
        if s_type == 'sawtooth':
            for i in np.arange(n_pulses):
                pulse = create_sawtooth_pulse(freq, sf, amp, first_peak=first_peak)
                temp_sig.append(pulse)
        elif s_type == 'sinusoidal':
            for i in np.arange(n_pulses):
                pulse = create_sin_pulse(freq, sf, amp, first_peak=first_peak)
                temp_sig.append(pulse)
        else:
            for i in np.arange(n_pulses):
                pulse = create_square_pulse(freq, sf, amp, first_peak=first_peak)
                temp_sig.append(pulse)
        temp_sig = np.asarray(temp_sig).reshape(-1)

        sig = np.zeros(int(np.around(duration * sf, decimals=0)))
        sig = temp_sig[:sig.size]

        return sig
    else:
        raise ValueError(
            "Inappropriate type or value of one of the arguments. Please read carefully function docstring.")

# def create_random_noise_signal(duration, sf, min_freq, max_freq, )

# SIMPLE CALCULATIONS
def z_score(x, avg, sd):
    """Calculate z-score.

    Parameters
    ----------
    x : float
        Standardized variable..
    avg : float
        Average from population.
    sd : float
        Standard deviation from population.

    Returns
    -------
    z : float
        Z-score.
    """
    return (x - avg) / sd


def create_time_scale(n_samples, sf, unit='s'):
    """Create one-dimensional time scale.

    Parameters
    ----------
    n_samples : int
        Total number of samples in the signal for which time scale has to be created.
    sf : int
        Sampling frequency of the signal, ie. number of samples per second.
    unit : str
        Time unit in which time scale has to be expressed. Available units: hours 'h', minutes 'min', seconds 's',
        milliseconds 'ms', microseconds 'us', nanoseconds 'ns'. Default value is 's'.

    Returns
    -------
    time_scale : 1D np.ndarray
        One-dimensional time scale with values expressed in a specific time unit.
    """
    if (isinstance(n_samples, int) and isinstance(sf, int) and unit in ['h', 'min', 's', 'ms', 'us', 'ns']):
        unit_convertion = {'h': 3600, 'min': 60, 's': 1, 'ms': 0.001, 'us': 0.000001, 'ns': 0.000000001}
        total_time_in_unit = (n_samples / sf) / unit_convertion[unit]
        dt = (1 / sf) / unit_convertion[unit]
        time_scale = np.arange(0, total_time_in_unit, dt)
        return time_scale
    else:
        raise ValueError(
            "Innapriopriate type or value of one of the arguments. Please read carefully function docstring.")


def list_is_int(list_of_ints):
    """Check whether given list contains only int values.

    Parameters
    ----------
    list_of_ints : list
        List of presumably only int values.

    Returns
    -------
    verdict : boolean
        Return True, if 'list_of_ints" contains only in values. Otherwise, return False.
    """
    if (isinstance(list_of_ints, list) and len(list_of_ints) > 0):
        for item in list_of_ints:
            if not isinstance(item, int):
                return False
        return True
    else:
        raise ValueError("Inappropriate type or size of the argument.")


def ndarray_contains_only(ndarray, values):
    """Check whether numpy.ndarray contains only some specific values.

    Parameters
    ----------
    ndarray : numpy.ndarray
        One-dimensional array.
    values : 1D numpy.ndarray
        One-dimensional array with values to check whether they occur in 'ndarray'.

    Returns
    -------
    verdict : boolean
        Return True, if 'ndarray' contains only 'values'. Otherwise, return False.

    """
    if (isinstance(ndarray, np.ndarray) and ndarray.ndim == 1 and isinstance(values, np.ndarray) and values.ndim == 1):
        mask = np.isin(ndarray, values)
        matches = np.sum(mask)
        if matches != ndarray.size:
            return False
        else:
            return True
    else:
        raise ValueError("Inappropriate type or shape of the argument.")


def twodim_to_onedim_list(twodim_list):
    return list(chain.from_iterable(twodim_list))


# TRANSFORMATIONS AND CORRECTIONS
def baseline_correction(sig, b_window, c_window, b_type='absolute'):
    """Perform baseline correction on a given one-dimensional signal.

    Parameters
    ----------
    sig : 1D numpy.ndarray
        One-dimensional signal for which baseline correction has to be performed.
    b_window : list of int of length 2
        Range of the 'sig' samples from which baseline should be calculated. Minimum and maximum range
        is [0, sig.size-1].
    c_window : list of int of length 2
        Range of the 'sig' samples which should be baseline-corrected. Minimum and maximum range is [0, sig.size-1].
    b_type : str
        Type of baseline. Available options: 'absolute', 'relative', 'relchange', 'decibel' (based on
        http://bjornherrmann.com/baseline_correction.html). Default values is 'absolute'. For 'X' is the signal
        and for 'B' is the baseline calculated as mean(sig[window[0]:window[1]]):
        1. 'absolute' - absolute baseline, range of possible values: [-inf, inf], calculated as X - B;
        2. 'relative' - relative baseline, range of possible values: [0, inf], calculated as X / B;
        3. 'relchange' - relative change baseline, range of possible values: [-1, inf], calculated as (X - B) / B;
        4. 'decibel' - decibel baseline (defined only for power), range of possible values: [-inf, inf], calculated as
        10 * log10(X / B).

    Returns
    -------
    corrected : numpy.ndarray
        Baseline-corrected signal.
    """
    if (isinstance(sig, np.ndarray) and sig.ndim == 1 and isinstance(b_window, list) and list_is_int(b_window)
            and len(b_window) in range(1, 3) and isinstance(c_window, list) and list_is_int(c_window)
            and len(c_window) in range(1, 3) and b_type in ['absolute', 'relative', 'relchange', 'decibel']):

        baseline = np.mean(sig[b_window[0]:b_window[1]])

        if b_type == 'absolute':
            sig[c_window[0]:c_window[1]] -= baseline
        elif b_type == 'relative':
            sig[c_window[0]:c_window[1]] /= baseline
        elif b_type == 'relchange':
            sig[c_window[0]:c_window[1]] = (sig[c_window[0]:c_window[1]] - baseline) / baseline
        else:
            sig[c_window[0]:c_window[1]] = 10 * np.log10(sig[c_window[0]:c_window[1]] / baseline)

        return sig
    else:
        raise ValueError(
            "Inappropriate type, value or shape of one of the arguments. Please read carefully function docstring.")


def hanning_correction(sig, c_window, mode='full'):
    """Perform Hanning window correction on a given one-dimensional signal.

    Parameters
    ----------
    sig : 1D numpy.ndarray
        One-dimensional signal.
    c_window : list of int of length 2
        Range of the 'sig' samples which should be Hanning-corrected. Minimum and maximum range is [0, sig.size-1].
    mode : str
        Mode of the Hanning correction. There are three available modes: 'half-left', 'half-right', 'full'.
        Default value is 'full'. Modes description:
        1. 'half-left' - only half left part of the Hanning window is used for the correction.
        2. 'half-right' - only half right part of the Hanning window is used for the correction.
        3. 'full' - full Hanning window is used for the correction.

    Returns
    -------
    corrected : 1D numpy.ndarray
        Hanning-corrected signal.
    """
    if (isinstance(sig, np.ndarray) and sig.ndim == 1 and list_is_int(c_window) and len(c_window) in range(1, 3)
            and mode in ['half-left', 'half-right', 'full']):

        c_window_size = sig[c_window[0]:c_window[1]].size
        if mode == 'half-left':
            hann = np.hanning(c_window_size * 2)[:c_window_size]
            sig[c_window[0]:c_window[1]] = np.multiply(sig[c_window[0]:c_window[1]], hann)
        elif mode == 'half-right':
            hann = np.hanning(c_window_size * 2)[c_window_size:]
            sig[c_window[0]:c_window[1]] = np.multiply(sig[c_window[0]:c_window[1]], hann)
        else:
            hann = np.hanning(c_window_size)
            sig[c_window[0]:c_window[1]] = np.multiply(sig[c_window[0]:c_window[1]], hann)
        return sig
    else:
        raise ValueError(
            "Inappropriate type, value or shape of one of the arguments. Please read carefully function docstring.")


def spectrum(sig, time_scale, abs=True):
    """Compute the one-dimensional Discrete Fourier Transform (DFT) for given N-dimensional signal.

    Parameters
    ----------
    sig : numpy.ndarray
        Signal for DFT (can be complex).
    time_scale : 1D numpy.ndarray
        One-dimensional time scale in seconds.
    abs : boolean
        If True, the result of DFT will be absolute, thus converted from complex to real space and contain information only
         about signal magnitude. If False, the result of DFT will be complex. Default value is True.

    Returns
    -------
    freqs : 1D numpy.ndarray
        One-dimensional array containing information about the signal frequencies.
    fft : numpy.ndarray or complex numpy.ndarray
        One-dimensional array containing the result of DFT. If parameter 'abs' is equal to False, the result will
        be complex numpy.ndarray.
    """
    # if (isinstance(sig, np.ndarray) and isinstance(time_scale, np.ndarray) and time_scale.ndim == 1):
    if True:
        freqs = scifft.fftfreq(sig.size, d=time_scale[1] - time_scale[0])
        fft = np.fft.fft(sig)
        if abs:
            return freqs, np.abs(fft)
        else:
            return freqs, fft
    else:
        raise ValueError(
            "Inappropriate type or shape of one of the arguments. Please read carefully function docstring.")

def new_range(signal, new_min, new_max):
    new_signal = (((signal - np.min(signal)) * (new_max - new_min)) / (np.max(signal) - np.min(signal))) + new_min
    return new_signal

# FREQUENCY ANALYSIS
def itpc(k, rayleigh_z=False):
    """Compute inter-trial phase clustering (ITPC) for a vector of phase angles at one time-frequency point over trials.

    Parameters
    ----------
    k : 1D numpy.ndarray
        Vector of phase angles at one time-frequency point over trials
    rayleigh_z : boolean
        If True transform ITPC to ITPC-Z, also known as Rayleigh's Z. If False compute default ITPC.

    Returns
    -------
    itpc : float
        If rayleigh_z was False return default ITPC value between 0.0 and 1.0.
        If rayleigh_z was True return ITPC-Z value which is > 0.0.
    """
    if rayleigh_z:
        return len(k) * np.abs(np.mean(np.exp(1j * k))) ** 2
    else:
        return np.abs(np.mean(np.exp(1j * k)))


# VISUALIZATION


# OTHER
def phase_shift_in_degrees(time_difference, wave_period):
    """
    Calculate phase shift in degrees based on time difference and wave period.
    :param time_difference:
    :param wave_period:
    :return:
    """
    return 360 * time_difference / wave_period

def wave_period_in_seconds(wave_frequency_in_hz):
    return 1 / wave_frequency_in_hz

def degrees_to_radians(degrees, ndecimals=4):
    return np.around(degrees * np.pi / 180, decimals=ndecimals)

def dot_product(a, b):
    """Calculate the dot product of the two 1D vectors of equal size.

    Parameters
    ----------
    a, b : 1D numpy.ndarray
        One-dimensional vectors of the same length (the same number of elements).

    Returns
    -------
    dotproduct : float
        Dot product of the a and b vectors.
    """
    if np.size(a, axis=0) == np.size(b, axis=0):
        multiplication_results = []
        for i in np.arange(np.size(a)):
            multiplication_results.append(a[i] * b[i])
            multiplication_results = np.asarray(multiplication_results)
        return np.sum(multiplication_results)
    else:
        raise ValueError("Unequal size of the a and b vectors.")


def sine_wave(amp, freq, duration, phi, sf):
    """

    Parameters
    ----------
    amp : float
        Amplitude.
    freq : float
        Frequency.
    duration : float
        Duration in seconds.
    phi : float
        Phase angle offset.
    sf : int
        Sampling frequency of the signal.

    Returns
    -------
    sin_wave : 1D numpy.ndarray
        Sinusoidal wave of a given properties.
    """
    time_scale = np.arange(0, duration, 1 / sf)
    return amp * np.sin(2 * np.pi * freq * time_scale + phi)


def rgb255to1(rgb):
    """Convert RGB values expressed in range 0-255 to values expressed in range 0.0-1.0.

    Parameters
    ----------
    rgb : 3-element list of ints
        List of three RGB values expressed in 0-255 range, e.g. [255, 255, 255].

    Returns
    -------
    rgb_1 : 3-element list of floats
        List of three RGB values expressed in 0.0-1.0 range, e.g. [1.0, 1.0, 1.0].
    """
    return [rgb[0] / 255, rgb[1] / 255, rgb[2] / 255]


def hex_to_rgb(hex, rgb_type=255):
    """Convert HEX colour value to RGB.

    Parameters
    ----------
    hex : String, eg. '#FFFFFF'.
        HEX colour value to convert.
    rgb_type : int, 255 or 1
        If rgb_type equals 255, HEX value will be converted to RGB values in range 0-255. If rgb_type equals 1,
        HEX value will be converted to RGB values in range 0.0-1.0. Default is 255.

    Returns
    -------
    rgb : 3-element tuple of ints (if rgb_type = 255) or floats (if rgb_type = 1).
        Converted RGB values.

    Raises
    ------
    ValueError
        If rgb_type is not equal to 255 or 1.
    """
    h = hex.lstrip('#')
    if rgb_type == 255:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    elif rgb_type == 1:
        rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        return tuple(rgb255to1(rgb))
    else:
        raise ValueError("Innapriopriate rgb_type value. It should be 255 or 1.")


def div_range_of_numbers(r_of_n, segments):
    """Divide range of equally spaced integer numbers e.g. [0, 1, 2, 3] into
    equally spaced segments, e.g. [0, 1], [2, 3].

    Parameters
    ==========
    r_of_n : int
        Length of range of numbers. E.g. if r_of_n equals 3, it will result with
        integer list [0, 1, 2, 3].
    segments : int
        Number of segments to which range of numbers should be divided. If segments
        equal e.g. 2, than range of numbers [0, 1, 2, 3] will be divided into 2
        segments [0, 1] and [2, 3].

    Returns
    =======
    ranges : list
        Returns formatted list ['0,1', '2,3'].
    """
    step = r_of_n / segments
    return ["{},{}".format(round(step * i), round(step * (i + 1))) for i in range(segments)]


def get_file_names_from_path(path, file_type='.txt'):
    """Get file names from given path.

    Parameters
    ==========
    path : str
        Path to folder with files.
    file_type
        Type of files to find for. Default is '.txt'.

    Returns
    =======
     files : list of strings
        Returns list of strings being file names with a given extension, e.g. 'file.txt'.

    """
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if file_type in file:
                files.append(os.path.join(r, file))


def superimpose_two_vectors(a, b, shift=0):
    """
    Superimpose two vectors with the same or different lengths with a possible shift between two.
    :param a: Vector 1.
    :param b: Vector 2.
    :param shift: Shift in samples between two vectors.
    :return: Vector.
    """
    if len(a) < len(b):
        c = b.copy()
        c[shift:shift+len(a)] += a
    else:
        c = a.copy()
        c[shift:shift+len(b)] += b
    return c


def create_signal_template(sf, prefix, postfix, n_trials, trial_base_length, trial_random_length):
    """
    Generate a signal template consisting of pulse-like trials with specified properties.

    Parameters
    ----------
    sf : int
        Sampling frequency in Hz. Must be > 0.
    prefix : float or None
        Length of the prefix in seconds before the trials. Set to None if not needed.
    postfix : float or None
        Length of the postfix in seconds after the trials. Set to None if not needed.
    n_trials : int
        Number of trials to generate. Must be > 0.
    trial_base_length : float
        Base length of each trial in seconds. Must be > 0.
    trial_random_length : float or None
        Optional random additional length for each trial. Set to None if not needed.

    Returns
    -------
    numpy.ndarray
        Generated signal template.

    Raises
    ------
    ValueError
        If sf, n_trials, trial_base_length is equal to zero, or if any value is None or less than zero.
    """

    # Check if any of the parameters are None or less than zero
    if sf is None or n_trials is None or trial_base_length is None or \
            sf <= 0 or n_trials <= 0 or trial_base_length <= 0 or \
            prefix is not None and prefix <= 0 or postfix is not None and postfix <= 0 or \
            trial_random_length is not None and trial_random_length <= 0:
        raise ValueError("Error: sf, n_trials, trial_base_length, prefix, postfix, or trial_random_length "
                         "cannot be None or less than or equal to zero. Stopping function.")

    # Initialize list to store signal partial templates
    signal_template = []

    # Add prefix if specified and greater than zero
    if prefix is not None and prefix > 0:
        # Create zeros for the prefix length converted to samples and append to the signal template
        signal_template.append(np.zeros(int(prefix * sf)))

    # Loop to generate individual trials
    for _ in range(n_trials):
        # Calculate the base samples for each trial based on the specified base length
        trial_base_samples = trial_base_length * sf

        # Add random length if specified and greater than zero
        if trial_random_length is not None and trial_random_length > 0:
            # Generate random additional samples within the specified range and adjust trial base samples
            trial_random_samples = int(np.random.uniform(-trial_random_length * sf, trial_random_length * sf))
            trial_base_samples += trial_random_samples

        trial = np.zeros(int(trial_base_samples))

        # Set the first sample of each trial to 1 (pulse-like signal)
        trial[0] = 1

        # Append each trial to the signal template
        signal_template.append(trial)

    # Add postfix if specified and greater than zero
    if postfix is not None and postfix > 0:
        signal_template.append(np.zeros(int(postfix * sf)))

    # Combine all signal indicators into a single template
    signal_template = np.concatenate(signal_template)

    return signal_template



# def create_sin_pulse(freq, sf, amp, first_peak='positive'):
#     """
#     Create one-period sinusoidal pulse.
#
#     Parameters
#     ----------
#     freq : float
#         Frequency of the pulse wave in Hz. Must be > 0.
#     sf : int
#         Sampling frequency of the pulse (number of samples per second). Must be > 0.
#     amp : float
#         Amplitude of the pulse in microamperes (uA). Must be > 0.
#     first_peak : str, optional
#         Polarity of the first pulse hillock. Available options: 'positive', 'negative'.
#         Default value is 'positive'.
#
#     Returns
#     -------
#     pulse : numpy.ndarray
#         One-period sinusoidal pulse.
#     """
#     # Check if input arguments are valid
#     if (isinstance(freq, float) and freq > 0 and
#         isinstance(sf, int) and sf > 0 and
#         isinstance(amp, float) and amp > 0 and
#         first_peak in ['positive', 'negative']):
#
#         # Calculate the duration of one pulse period
#         duration = 1 / freq
#
#         # Generate time scale using the sampling frequency
#         time_scale = np.arange(0, duration, 1 / sf)
#
#         # Generate the sinusoidal pulse
#         pulse = np.sin(2 * np.pi * freq * time_scale) * (amp / 2)
#
#         # Reverse the pulse if first_peak is 'negative'
#         if first_peak == 'negative':
#             pulse *= -1
#
#         return pulse  # Return the generated pulse
#     else:
#         # Raise a ValueError if the input arguments are invalid
#         raise ValueError(
#             "Inappropriate type or value of one of the arguments. Please read the function docstring.")


def create_sin_pulse(freq, sf, amp, first_peak='positive'):
    """
    Create a one-period sinusoidal pulse.

    Parameters
    ----------
    freq : float
        Frequency of the pulse wave in Hz. Must be > 0.
    sf : int
        Sampling frequency of the pulse (number of samples per second). Must be > 0.
    amp : float
        Amplitude of the pulse in microamperes (µA). Must be > 0.
    first_peak : str
        Polarity of the first pulse peak. Available options: 'positive', 'negative'.
        Default is 'positive'.

    Returns
    -------
    pulse : numpy.ndarray
        One-period sinusoidal pulse.
    time_scale : numpy.ndarray
        Corresponding time values for the pulse.

    Raises
    ------
    ValueError
        If the input values are not valid.
    """
    # Check input arguments
    if not (isinstance(freq, (float, int)) and freq > 0):
        raise ValueError("Frequency must be a positive float or int.")
    if not (isinstance(sf, int) and sf > 0):
        raise ValueError("Sampling frequency must be a positive integer.")
    if not (isinstance(amp, (float, int)) and amp > 0):
        raise ValueError("Amplitude must be a positive float or int.")
    if first_peak not in ['positive', 'negative']:
        raise ValueError("first_peak must be either 'positive' or 'negative'.")

    # Calculate the duration of one period of the pulse
    duration = 1 / freq
    # Generate the time scale
    time_scale = np.arange(0, duration, 1 / sf)
    # Generate the sinusoidal pulse
    pulse = np.sin(2 * np.pi * freq * time_scale) * (amp / 2)

    # Adjust the polarity if necessary
    if first_peak == 'negative':
        pulse *= -1

    return pulse, time_scale

def brainvision_bvef_spherical_to_simnibs_csv_cartesian(bvef_file_path, csv_output_path, mltpr_x=1, mltpr_y=1, mltpr_z=1, shift_x=0, shift_y=0, shift_z=0):
    """
    Convert BrainVision BVEF file containing electrode spherical coordinates to SimNIBS CSV file with Cartesian coordinates.

    Parameters:
    - bvef_file_path (str): Path to the BrainVision BVEF file.
    - csv_output_path (str): Path to save the resulting SimNIBS CSV file.
    - mltpr_x (float): Multiplier for X-coordinate conversion.
    - mltpr_y (float): Multiplier for Y-coordinate conversion.
    - mltpr_z (float): Multiplier for Z-coordinate conversion.
    - shift_x (float): Shift for X-coordinate.
    - shift_y (float): Shift for Y-coordinate.
    - shift_z (float): Shift for Z-coordinate.

    Returns:
    - pd.DataFrame: DataFrame containing the converted Cartesian coordinates and electrode labels.

    This function parses the BrainVision BVEF file, extracts electrode spherical coordinates (Theta, Phi, Radius),
    and converts them to Cartesian coordinates (X, Y, Z). The resulting coordinates are saved to a SimNIBS-compatible
    CSV file, and a DataFrame is returned.

    SimNIBS CSV format:
    - The file will have columns 'Type', 'X', 'Y', 'Z', 'Label'.
    - 'Type' will be set to 'Electrode' for each entry.
    - 'X', 'Y', 'Z' are the Cartesian coordinates.
    - 'Label' is the electrode label.

    Example Usage:
    > bvef_file_path = 'path/to/your/file.bvef'
    > csv_output_path = 'path/to/your/output.csv'
    > df = brainvision_bvef_spherical_to_simnibs_csv_cartesian(bvef_file_path, csv_output_path)
    """

    # Parse the BVEF file
    tree = ET.parse(bvef_file_path)
    root = tree.getroot()

    # Create lists to store data
    types = []
    x_coordinates = []
    y_coordinates = []
    z_coordinates = []
    labels = []

    # Iterate through each Electrode element in the BVEF
    for electrode_elem in root.findall('.//Electrode'):

        # Extract information from the BVEF
        label = electrode_elem.find('Name').text
        theta = math.radians(float(electrode_elem.find('Theta').text))
        phi = math.radians(float(electrode_elem.find('Phi').text))
        radius = float(electrode_elem.find('Radius').text)

        # Convert spherical coordinates to Cartesian coordinates
        x = radius * math.sin(theta) * math.cos(phi) * mltpr_x + shift_x
        y = radius * math.sin(theta) * math.sin(phi) * mltpr_y + shift_y
        z = radius * math.cos(theta) * mltpr_z + shift_z

        # Append data to lists
        types.append("Electrode")
        x_coordinates.append(x)
        y_coordinates.append(y)
        z_coordinates.append(z)
        labels.append(label)

    # Create DataFrame
    df = pd.DataFrame({
        'Type': types,
        'X': x_coordinates,
        'Y': y_coordinates,
        'Z': z_coordinates,
        'Label': labels
    })

    # Save DataFrame to CSV
    df.to_csv(csv_output_path, index=False, header=False)

    return df


def simnibs_csv_to_geo(csv_file_path, geo_file_path):
    """
    Generate a Gmsh template from EEG electrode coordinates stored in a CSV file.

    Parameters:
    - csv_file_path (str): The file path of the CSV file containing EEG electrode coordinates.
    - geo_file_path (str): The desired file path for the generated Gmsh (.geo) file.

    Returns:
    - str: Returns a Gmsh template in the form of a string.

    This function reads electrode coordinates from a CSV file and generates a Gmsh template
    based on the specified format. The template includes SP (Sphere) and T3 (Triangle) elements
    for each electrode. The resulting template is saved to a Gmsh (.geo) file.

    The template string can be further used or printed if needed.

    Example Usage:
    > csv_file_path = 'eeg_coordinates_cartesian.csv'
    > geo_file_path = 'eeg_coordinates_cartesian.geo'
    > template_string = generate_geo_template(csv_file_path, geo_file_path)
    """
    # Define custom column names
    column_names = ['Type', 'X', 'Y', 'Z', 'Label']

    # Read the CSV file with specified header=None and custom column names
    df = pd.read_csv(csv_file_path, header=None, names=column_names)

    # Initialize the template
    template = "View\"\"{\n"

    # Iterate through rows and fill the template
    for index, row in df.iterrows():
        X = row['X']
        Y = row['Y']
        Z = row['Z']
        electrode_label = row['Label']

        template += f"SP({X}, {Y}, {Z-0.05}){{0}};\n"
        template += f"T3({X}, {Y}, {Z}, 0){{\"{electrode_label}\"}};\n"

    template += "};\nmyView = PostProcessing.NbViews-1;\n"
    template += "View[myView].PointType=1;\n"
    template += "View[myView].PointSize=6;\n"
    template += "View[myView].LineType=1;\n"
    template += "View[myView].LineWidth=2;"

    # Write the template to a .geo file
    with open(geo_file_path, 'w') as file:
        file.write(template)

    return template


def brainvision_bvef_to_xyz_coordinates(bvef_file_path, csv_output_file, mltpr_x=1, mltpr_y=1, mltpr_z=1, shift_x=0, shift_y=0, shift_z=0):
    """
    Convert BrainVision BVEF file containing electrode information to XYZ coordinates and save to a CSV file.

    Parameters:
    - bvef_file_path (str): Path to the BrainVision BVEF file.
    - csv_output_file (str): Path to save the resulting CSV file.
    - mltpr_x (float): Multiplier for X-coordinate conversion.
    - mltpr_y (float): Multiplier for Y-coordinate conversion.
    - mltpr_z (float): Multiplier for Z-coordinate conversion.
    - shift_x (float): Shift for X-coordinate.
    - shift_y (float): Shift for Y-coordinate.
    - shift_z (float): Shift for Z-coordinate.

    Returns:
    - pd.DataFrame: DataFrame containing the converted XYZ coordinates and electrode labels.

    This function parses the BrainVision BVEF file, extracts electrode information, and converts spherical
    coordinates (Theta, Phi, Radius) to Cartesian coordinates (X, Y, Z). The resulting coordinates are saved
    to a CSV file, and a DataFrame is returned.

    Example Usage:
    > bvef_file_path = 'path/to/your/file.bvef'
    > csv_output_file = 'path/to/your/output.csv'
    > df = brainvision_bvef_to_xyz_coordinates(bvef_file_path, csv_output_file)
    """

    # Parse the BVEF file
    tree = ET.parse(bvef_file_path)
    root = tree.getroot()

    # Create lists to store data
    names = []
    x_coordinates = []
    y_coordinates = []
    z_coordinates = []


    # Iterate through each Electrode element in the BVEF
    for electrode_elem in root.findall('.//Electrode'):

        # Extract information from the BVEF
        label = electrode_elem.find('Name').text
        theta = math.radians(float(electrode_elem.find('Theta').text))
        phi = math.radians(float(electrode_elem.find('Phi').text))
        radius = float(electrode_elem.find('Radius').text)

        # Convert spherical coordinates to Cartesian coordinates
        x = radius * math.sin(theta) * math.cos(phi) * mltpr_x + shift_x
        y = radius * math.sin(theta) * math.sin(phi) * mltpr_y + shift_y
        z = radius * math.cos(theta) * mltpr_z + shift_z

        # Append data to lists
        names.append(label)
        x_coordinates.append(x)
        y_coordinates.append(y)
        z_coordinates.append(z)


    # Create DataFrame
    df = pd.DataFrame({
        'name': names,
        'x': x_coordinates,
        'y': y_coordinates,
        'z': z_coordinates,
    })

    # Save DataFrame to CSV
    df.to_csv(csv_output_file, index=False, header=False)

    return df


def calc_pulse_current_at_given_timestamp(t, f, I_max):
    """
    Calculate the pulse current and corresponding currents at electrodes A and B at a given timestamp.

    Parameters:
    - t (float): Timestamp in seconds.
    - f (float): Frequency of the alternating current in Hz.
    - I_max (float): Maximum amplitude of the current in µA.

    Returns:
    - I_t (float): Total current in µA.
    - I_A (float): Current at electrode A (anode) in µA.
    - I_B (float): Current at electrode B (cathode) in µA.
    """
    # Calculate current using the sine function
    I_t = I_max * np.sin(2 * np.pi * f * t)

    # Calculate currents at electrodes A and B
    I_A = I_t
    I_B = -I_t

    return I_t, I_A, I_B

# This file is part of QuantumPolyspectra: a Python Package for the
# Analysis and Simulation of Quantum Measurements
#
#    Copyright (c) 2020 and later, Markus Sifft and Daniel Hägele.
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the QuTiP: Quantum Toolbox in Python nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

import h5py
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pickle

import arrayfire as af
from arrayfire.arith import conjg as conj
from arrayfire.interop import from_ndarray as to_gpu
from arrayfire.signal import fft_r2c
from arrayfire.statistics import mean

from matplotlib.colors import LinearSegmentedColormap
from numba import njit
from scipy.fft import rfftfreq
from scipy.ndimage.filters import gaussian_filter
from tqdm import tqdm_notebook


class MissingValueError(Exception):
    """Base class for missing value exceptions"""
    pass


def pickle_save(path, obj):
    """
    Helper function to pickle system objects

    Parameters
    ----------
    path : str
        Location of saved data
    obj : System obj

    """
    f = open(path, mode='wb')
    pickle.dump(obj, f)
    f.close()


def to_hdf(dt, data, path, group_name, dataset_name):
    """
    Helper function to generated h5 file from numpy array.

    Parameters
    ----------
    dt : float
        Inverse sampling rate of the signal (is saved as attribute "dt" to the dataset)
    data : array
        E.g. simulation results
    path : str
        Path for the data to be saved at
    group_name : str
        Name of the group in the h5 file
    dataset_name : str
        Name of the dataset in the h5 file

    """
    with h5py.File(path, "w") as f:
        grp = f.create_group(group_name)
        d = grp.create_dataset(dataset_name, data=data)
        d.attrs['dt'] = dt


def import_data(path, group_key, dataset, full_import=False):
    """
    Helper function to load data from h5 file into numpy array.
    Import of .h5 data with format group_key -> data + attrs[dt]

    Parameters
    ----------
    full_import: bool
        If true all data is loaded in RAM (recommended if possible)
    path : str
        Path for the data to be saved at
    group_key : str
        Name of the group in the h5 file
    dataset : str
        Name of the dataset in the h5 file

    Returns
    -------
    Returns simulation result and inverse sampling rate
    """

    main = h5py.File(path, 'r')
    main_group = main[group_key]
    main_data = main_group[dataset]
    delta_t = main_data.attrs['dt']
    if full_import:
        return main_data[()], delta_t
    else:
        return main_data, delta_t


@njit(parallel=False)
def calc_a_w3(a_w_all, f_max_ind, m):
    """
    Preparation of a_(w1+w2) for the calculation of the bispectrum

    Parameters
    ----------
    a_w_all : array
        Fourier coefficients of the signal
    f_max_ind : int
        Index of the maximum frequency to be used for the calculation of the spectra
    m : int
        Number of windows per spectrum

    Returns
    -------
    a_w3 : array
        Matrix of Fourier coefficients
    """

    a_w3 = 1j * np.empty((f_max_ind // 2, f_max_ind // 2, m))
    for i in range(f_max_ind // 2):
        a_w3[i, :, :] = a_w_all[i:i + f_max_ind // 2, 0, :]
    return a_w3.conj()


def c2(a_w, a_w_corr, m, coherent):
    """calculation of c2 for power spectrum"""
    # ---------calculate spectrum-----------
    # C_2 = m / (m - 1) * (< a_w * a_w* > - < a_w > < a_w* >)
    #                          sum_1         sum_2   sum_3
    mean_1 = mean(a_w * conj(a_w_corr), dim=2)

    if coherent:
        s2 = mean_1
    else:
        mean_2 = mean(a_w, dim=2)
        mean_3 = mean(conj(a_w_corr), dim=2)
        s2 = m / (m - 1) * (mean_1 - mean_2 * mean_3)
    return s2


def c3(a_w1, a_w2, a_w3, m):
    """
    Calculation of c3 for bispectrum (see arXiv:1904.12154)
    # C_3 = m^2 / (m - 1)(m - 2) * (< a_w1 * a_w2 * a_w3 >
    #                                      sum_123
    #       - < a_w1 >< a_w2 * a_w3 > - < a_w1 * a_w2 >< a_w3 > - < a_w1 * a_w3 >< a_w2 >
    #          sum_1      sum_23           sum_12        sum_3         sum_13      sum_2
    #       + 2 < a_w1 >< a_w2 >< a_w3 >)
    #             sum_1   sum_2   sum_3
    # with w3 = - w1 - w2

    Parameters
    ----------
    a_w1 : array
        Fourier coefficients of signal as vertical array
    a_w2 : array
        Fourier coefficients of signal as horizontal array
    a_w3 : array
        a_w1+w2 as matrix
    m : int
        Number of windows used for the calculation of one spectrum

    Returns
    -------
    Returns the c3 estimator as matrix
    """

    ones = to_gpu(np.ones_like(a_w1.to_ndarray()))
    d_1 = af.matmulNT(ones, a_w1)
    d_2 = af.matmulNT(a_w2, ones)
    d_3 = a_w3
    d_12 = d_1 * d_2
    d_13 = d_1 * d_3
    d_23 = d_2 * d_3
    d_123 = d_1 * d_2 * d_3

    d_1_mean = mean(d_1, dim=2)
    d_2_mean = mean(d_2, dim=2)
    d_3_mean = mean(d_3, dim=2)
    d_12_mean = mean(d_12, dim=2)
    d_13_mean = mean(d_13, dim=2)
    d_23_mean = mean(d_23, dim=2)
    d_123_mean = mean(d_123, dim=2)

    s3 = m ** 2 / ((m - 1) * (m - 2)) * (d_123_mean - d_12_mean * d_3_mean -
                                         d_13_mean * d_2_mean - d_23_mean * d_1_mean +
                                         2 * d_1_mean * d_2_mean * d_3_mean)
    return s3


def c4(a_w, a_w_corr, m):
    """
    calculation of c4 for trispectrum
    # C_4 = (Eq. 60, in arXiv:1904.12154)

    Parameters
    ----------
    a_w : array
        Fourier coefficients of the signal
    a_w_corr : array
        Fourier coefficients of the signal or a second signal
    m : int
        Number of windows used for the calculation of one spectrum

    Returns
    -------
    Returns the c4 estimator as matrix

    """

    a_w_conj = conj(a_w)
    a_w_conj_corr = conj(a_w_corr)

    ones = to_gpu(np.ones_like(a_w.to_ndarray()[:, :, 0]))

    sum_11c22c = af.matmulNT(a_w * a_w_conj, a_w_corr * a_w_conj_corr)
    sum_11c22c_m = mean(sum_11c22c, dim=2)

    sum_11c2 = af.matmulNT(a_w * a_w_conj, a_w_corr)
    sum_11c2_m = mean(sum_11c2, dim=2)
    sum_122c = af.matmulNT(a_w, a_w_corr * a_w_conj_corr)
    sum_122c_m = mean(sum_122c, dim=2)
    sum_1c22c = af.matmulNT(a_w_conj, a_w_corr * a_w_conj_corr)
    sum_1c22c_m = mean(sum_1c22c, dim=2)
    sum_11c2c = af.matmulNT(a_w * a_w_conj, a_w_conj_corr)
    sum_11c2c_m = mean(sum_11c2c, dim=2)

    sum_11c = a_w * a_w_conj
    sum_11c_m = mean(sum_11c, dim=2)
    sum_22c = a_w_corr * a_w_conj_corr
    sum_22c_m = mean(sum_22c, dim=2)
    sum_12c = af.matmulNT(a_w, a_w_conj_corr)
    sum_12c_m = mean(sum_12c, dim=2)
    sum_1c2 = af.matmulNT(a_w_conj, a_w_corr)
    sum_1c2_m = mean(sum_1c2, dim=2)

    sum_12 = af.matmulNT(a_w, a_w_corr)
    sum_12_m = mean(sum_12, dim=2)
    sum_1c2c = af.matmulNT(a_w_conj, a_w_conj_corr)
    sum_1c2c_m = mean(sum_1c2c, dim=2)

    sum_1_m = mean(a_w, dim=2)
    sum_1c_m = mean(a_w_conj, dim=2)
    sum_2_m = mean(a_w_corr, dim=2)
    sum_2c_m = mean(a_w_conj_corr, dim=2)

    sum_11c_m = af.matmulNT(sum_11c_m, ones)
    sum_22c_m = af.matmulNT(ones, sum_22c_m)
    sum_1_m = af.matmulNT(sum_1_m, ones)
    sum_1c_m = af.matmulNT(sum_1c_m, ones)
    sum_2_m = af.matmulNT(ones, sum_2_m)
    sum_2c_m = af.matmulNT(ones, sum_2c_m)

    s4 = m ** 2 / ((m - 1) * (m - 2) * (m - 3)) * (
            (m + 1) * sum_11c22c_m - (m + 1) * (sum_11c2_m * sum_2c_m + sum_11c2c_m * sum_2_m +
                                                sum_122c_m * sum_1c_m + sum_1c22c_m * sum_1_m)
            - (m - 1) * (sum_11c_m * sum_22c_m + sum_12_m * sum_1c2c_m + sum_12c_m * sum_1c2_m)
            + 2 * m * (sum_11c_m * sum_2_m * sum_2c_m + sum_12_m * sum_1c_m * sum_2c_m +
                       sum_12c_m * sum_1c_m * sum_2_m + sum_22c_m * sum_1_m * sum_1c_m +
                       sum_1c2c_m * sum_1_m * sum_2_m + sum_1c2_m * sum_1_m * sum_2c_m)
            - 6 * m * sum_1_m * sum_1c_m * sum_2_m * sum_2c_m)

    return s4


@njit
def find_end_index(data, start_index, T_window, m, frame_number, j):
    """

    Parameters
    ----------
    data : array
        timestamps of detector clicks
    start_index : int
        index of the last timestamp in the whole dataset that fitted into the prior window (zero in case of first window)
    T_window : float
        window length in seconds (or unit of choice)
    m : int
        number of windows to calculate the cumulant estimator from
    frame_number : int
        keeps track of the current frame (1 frame = m windows)
    j : int
        number of the current window in the frame

    Returns
    -------

    """
    end_time = T_window * (m * frame_number + (j + 1))

    if data[start_index] > end_time:
        return start_index

    if end_time > data[-1]:
        return -1

    i = 1
    while True:
        if data[start_index + i] > end_time:
            return start_index + i
        i += 1


@njit
def g(x_, N_window, L, sigma_t):
    """
    Helper function to calculate the approx. confined gaussian window as defined in https://doi.org/10.1016/j.sigpro.2014.03.033

    Parameters
    ----------
    x_ : array
        points at which to calculate the function
    N_window : int
        length of window in points
    L : int
        N_window + 1
    sigma_t : float
        parameter of the approx. confined gaussian window (here chosen to be 0.14)

    Returns
    -------

    """
    return np.exp(-((x_ - N_window / 2) / (2 * L * sigma_t)) ** 2)


@njit
def calc_window(x, N_window, L, sigma_t):
    """
    Helper function to calculate the approx. confined gaussian window as defined in https://doi.org/10.1016/j.sigpro.2014.03.033

    Parameters
    ----------
    x : array
        points at which to calculate the function
    N_window : int
        length of window in points
    L : int
        N_window + 1
    sigma_t : float
        parameter of the approx. confined gaussian window (here chosen to be 0.14)

    Returns
    -------

    """
    return g(x, N_window, L, sigma_t) - (g(-0.5, N_window, L, sigma_t) * (
            g(x + L, N_window, L, sigma_t) + g(x - L, N_window, L, sigma_t))) / (
                   g(-0.5 + L, N_window, L, sigma_t) + g(-0.5 - L, N_window, L, sigma_t))


@njit
def cgw(N_window, fs=None, ones=False):
    """
    Helper function to calculate the approx. confined gaussian window as defined in https://doi.org/10.1016/j.sigpro.2014.03.033

    Parameters
    ----------
    ones : bool
        if true, the window is simply set to one resulting in a rectangular window
    fs : float
        sampling rate of the signal
    N_window : int
        length of window in points

    Returns
    -------

    """
    x = np.linspace(0, N_window, N_window)
    L = N_window + 1
    sigma_t = 0.14
    window = calc_window(x, N_window, L, sigma_t)
    if ones:
        window = np.ones(N_window)

    norm = np.sum(window ** 2) / fs

    return window / np.sqrt(norm), norm


@njit
def apply_window(window_width, t_clicks, fs, sigma_t=0.14):
    """
    This function take the timestamps of the detector and applies the window function as an envelope treating the
    clicks as steps with height one.

    Parameters
    ----------
    window_width : float
        timely width of the window in unit of choice
    t_clicks : array
        timestamps of the dataset that lie within the current window
    fs : float
        sampling rate of the signal
    sigma_t : float
        parameter of the approx. confined gaussian window (here chosen to be 0.14)

    Returns
    -------

    """

    # ----- Calculation of g_k -------

    dt = 1 / fs
    x = t_clicks / dt

    N_window = window_width / dt
    L = N_window + 1

    window = calc_window(x, N_window, L, sigma_t)
    # if ones:
    #    window = np.ones(N_window)

    # ------ Normalizing by calculating full window with given resolution ------

    N_window_full = 70
    dt_full = window_width / N_window_full

    # window_full, norm = cgw(N_window_full, 1 / dt_full, ones=ones)
    window_full, norm = cgw(N_window_full, 1 / dt_full)

    return window / np.sqrt(norm), window_full, N_window_full


def arcsinh_scaling(s_data, arcsinh_const, order, s_err=None, s_err_p=None, s_err_m=None):
    """
    Helper function to improve visibility in plotting (similar to a log scale but also works for negative values)

    Parameters
    ----------
    s_data : array
        spectral values of any order
    arcsinh_const : float
        these parameters sets the rescaling amount (the smaller, the stronger the rescaling)
    order : int
        important since the error arrays are called differently in the second-order case
    s_err : array
        spectral errors of order 3 or 4
    s_err_p : array
        spectral values + error of order 2
    s_err_m : array
        spectral values - error of order 2

    Returns
    -------

    """
    x_max = np.max(np.abs(s_data))
    alpha = 1 / (x_max * arcsinh_const)
    s_data = np.arcsinh(alpha * s_data) / alpha

    if order == 2:
        if s_err_p is not None:
            for i in range(0, 5):
                s_err_p[i] = np.arcsinh(alpha * s_err_p[i]) / alpha
                s_err_m[i] = np.arcsinh(alpha * s_err_m[i]) / alpha
        return s_data, s_err_p, s_err_m
    else:
        if s_err is not None:
            s_err = np.arcsinh(alpha * s_err) / alpha
        return s_data, s_err


def connect_broken_axis(s_f, broken_lims):
    """
    Helper function to enable broken axis during plotting

    Parameters
    ----------
    s_f : array
        frequencies at with the spectra had been calculated
    broken_lims : list
        list of arrays containing the endpoints of the disconnected frequency regions

    Returns
    -------

    """
    broken_lims_scaled = [(i, j) for i, j in broken_lims]
    diffs = []
    for i in range(len(broken_lims_scaled) - 1):
        diff = broken_lims_scaled[i + 1][0] - broken_lims_scaled[i][1]
        diffs.append(diff)
        s_f[s_f > broken_lims_scaled[i][1]] -= diff
    return s_f, diffs, broken_lims_scaled


def add_random_phase(a_w, window_size, delta_t, m):
    """(Experimental function) Adds a random phase proportional to the frequency to deal with ultra coherent signals

    Parameters
    ----------
    m : int
        number of windows per frame
    delta_t : float
        inverse of the sampling rate of the signal
    window_size : int
        size of the window in points
    a_w : array
        Fourier coefficients pf the window

    """

    random_factors = np.random.uniform(high=window_size * delta_t, size=m)
    freq_all_freq = rfftfreq(int(window_size), delta_t)
    freq_mat = np.tile(np.array([freq_all_freq]).T, m)
    factors = np.exp(1j * 2 * np.pi * freq_mat * random_factors)
    factors = factors.reshape(a_w.shape)
    factors_gpu = to_gpu(factors)
    a_w_phased = a_w * factors_gpu
    return a_w_phased


def plot_first_frame(chunk, delta_t, window_size):
    """
    Helper function for plotting one window during the calculation of the spectra for checking data and correct
    window length

    Parameters
    ----------
    chunk : array
        one frame of the dataset
    delta_t : float
        inverse sampling rate of the signal
    window_size : int
        size of window in points

    """
    first_frame = chunk[:window_size]
    t = np.arange(0, len(first_frame) * delta_t, delta_t)
    plt.figure(figsize=(14, 3))
    plt.plot(t, first_frame)
    plt.show()


class Spectrum:
    """
    Spectrum class stores signal data, calculated spectra and error of spectral values.
    Allows for the calculation of the polyspectra of the signal and their visualization.
    Also hold methods for saving spectrum objects.

    Parameters
    ----------
    path : str
        Path to h5 file with stored signal
    group_key : str
        Group key for h5 file
    dataset : str
        Name of the dataset in h5 file
    data : array
        Signal to be analyzed as Numpy array
    corr_data : array
        Second signal used as correlation data as Numpy array
    corr_path : str
        Path to h5 file with stored second signal for correlation
    corr_group_key : str
        Group key for h5 file with correlation signal
    corr_dataset : str
        Name of the dataset in h5 file with correlation signal

    Attributes
    ----------
    corr_data_path: str
        Path to h5 file with a second stored signal to be correlated with the first on (see path)
    T_window : float
        Length of window in seconds (or unit of choice) used for the calculation of
        any spectra
    path : str
        Path to h5 file with stored signal
    freq : array
        Stores frequencies at with the spectra are calculated
    f_max : float
        Used to limit the upper frequency to calculate spectral values at (especially important for high sampling rates)
    fs : float
        Stores the sampling rate of the signal
    f_lists: dict
        Used for the calculation of Poisson spectra. Stores all frequency values for the calculation of the
        non-uniform discreet Fourier transformation. (Also used for plotting with broken frequency axis.)
    S : dict
        Stores spectra values (final storage at the end of the calculation)
    S_gpu : dict
        Temporarily stores spectra values during calculation on the GPU
    S_err : dict
        Stores errors of spectra values (final storage at the end of the calculation)
    S_err_gpu : dict
        Temporarily stores errors of spectra values during calculation on the GPU
    S_errs : dict
        Temporarily stores m_var spectra used for the calculation of the errors
    S_stationarity_temp : dict
        Stores m_stationarity spectra which are then averaged and used for the stationarity plot
    S_stationarity : dict
        Stores the m_stationarity averaged spectra used for the stationarity plot
    group_key : str
        Group key of the dataset within the h5 file
    dataset : str
        Name of the dataset in the h5 file
    window_points : int
        Number of points in a window
    m : int
        Number of windows for the estimation of the cumulant
    m_var : int
        m_var single spectra are used at a time for the calculation of the spectral errors
    m_stationarity : int
        Number of spectra which are then averaged and used for the stationarity plot
    first_frame_plotted : bool
        If true the first frame is plotted during the calculation of the spectra
    delta_t : float
        Inverse of the sampling rate of the signal
    data : array / pointer
        Stores the full dataset or is a pointer to the data in the h5 file (recommended of the dataset
        is larger than your RAM)
    corr_data : array / pointer
        Stores the full second dataset or is a pointer to the data in the h5 file (recommended of the dataset
        is larger than your RAM)
    corr_group_key : str
        Group key of the second dataset within the h5 file
    corr_dataset : str
        Name of the second dataset in the h5 file
    main_data : array / pointer
        (outdated / for old methods) Stores the full dataset or is a pointer to the data in the h5 file (recommended of the dataset
        is larger than your RAM)
    err_counter : dict
        Counts the number single spectra already stored for the calculation of errors
     stationarity_counter : dict
        Counts the number single spectra already stored for the averaging for the stationarity plot
    """

    def __init__(self, path=None, group_key=None, dataset=None, delta_t=None, data=None, corr_data=None,
                 corr_path=None, corr_group_key=None, corr_dataset=None):
        self.corr_data_path = None
        self.T_window = None
        self.path = path
        self.freq = {2: None, 3: None, 4: None}
        self.f_max = 0
        self.fs = None
        self.f_lists = {2: None, 3: None, 4: None}
        self.S = {2: None, 3: None, 4: None}
        self.S_gpu = {2: None, 3: None, 4: None}
        self.S_err = {2: None, 3: None, 4: None}
        self.S_err_gpu = {2: None, 3: None, 4: None}
        self.S_errs = {2: [], 3: [], 4: []}
        self.S_stationarity_temp = {2: None, 3: None, 4: None}
        self.S_stationarity = {2: [], 3: [], 4: []}
        self.group_key = group_key
        self.dataset = dataset
        self.window_points = None
        self.m = {2: None, 3: None, 4: None}
        self.m_var = {2: None, 3: None, 4: None}
        self.m_stationarity = {2: None, 3: None, 4: None}
        self.first_frame_plotted = False
        self.delta_t = delta_t
        self.data = data
        self.corr_data = corr_data
        self.corr_path = corr_path
        self.corr_group_key = corr_group_key
        self.corr_dataset = corr_dataset
        self.main_data = None
        self.err_counter = {2: 0, 3: 0, 4: 0}
        self.stationarity_counter = {2: 0, 3: 0, 4: 0}

    def save_spec(self, path):
        """
        Method for storing the Spectrum object. Pointers and the full dataset are remove from the object before saving.

        Parameters
        ----------
        path : str
            Location of stored file

        """
        self.S_gpu = None
        self.S_err_gpu = None
        self.main_data = None
        self.corr_data = None
        self.data = None
        self.S_errs = None
        self.S_stationarity_temp = None
        pickle_save(path, self)

    def stationarity_plot(self, f_unit='Hz', t_unit='s', contours=False, s2_filter=0, arcsinh_plot=False,
                          arcsinh_const=1e-4, f_max=None,
                          normalize=False):
        """
        Plots the S_stationarity spectra versus time to make changes over time visible

        Parameters
        ----------
        f_unit : str
            Frequencies nit
        t_unit
        contours
        s2_filter
        arcsinh_plot
        arcsinh_const
        f_max
        normalize

        Returns
        -------

        """
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(24, 7))
        plt.rc('text', usetex=False)
        plt.rc('font', size=10)
        plt.rcParams["axes.axisbelow"] = False

        if self.f_lists[2] is not None:
            broken_lims = []
            for part in self.f_lists[2]:
                broken_lims.append((part[0], part[-1]))
        else:
            broken_lims = None

        s2_array = np.real(self.S_stationarity[2]).T.copy()
        s2_array = gaussian_filter(s2_array, sigma=[0, s2_filter])

        if normalize == 'area':
            s2_array /= np.sum(s2_array, axis=0)
        elif normalize == 'zero':
            s2_array /= np.max(s2_array, axis=0)

        if arcsinh_plot:
            s2_array, _, _ = arcsinh_scaling(s2_array, arcsinh_const, order=2)

        vmin = np.min(s2_array)
        vmax = np.max(s2_array)

        t_for_one_spec = self.T_window * self.m[2] * self.m_stationarity[2]
        time_axis = np.arange(0, s2_array.shape[1] * t_for_one_spec, t_for_one_spec)
        print(f'One spectrum calculated from a {t_for_one_spec * (s2_filter + 1)} ' + t_unit + ' measurement')

        s2_f = self.freq[2].copy()
        if broken_lims is not None:
            s2_f, diffs, broken_lims_scaled = connect_broken_axis(s2_f, broken_lims)
        else:
            diffs = None
            broken_lims_scaled = None

        x, y = np.meshgrid(time_axis, s2_f)

        c = ax.pcolormesh(x, y, s2_array, cmap='rainbow', vmin=vmin, vmax=vmax)  # norm=norm)
        if contours:
            ax.contour(x, y, s2_array, 7, colors='k', linewidths=0.7)

        if f_max:
            ax.axis([0, np.max(time_axis), 0, f_max])
        ax.set_xlabel(r"$t$ (" + t_unit + r")", fontdict={'fontsize': 14})
        ax.set_ylabel(r"$\omega / 2 \pi$ (" + f_unit + r")", fontdict={'fontsize': 14})
        ax.tick_params(axis='both', direction='in')
        ax.set_title(r'$S^{(2)}_z $ (' + f_unit + r'$^{-1}$) vs $' + t_unit + r'$',
                     fontdict={'fontsize': 16})
        _ = fig.colorbar(c, ax=ax)

        if broken_lims is not None:
            xlims = ax.get_xlim()
            for i, diff in enumerate(diffs):
                ax.hlines(broken_lims_scaled[i][-1] - sum(diffs[:i]), xlims[0], xlims[1], linestyles='dashed')

            ax.set_xlim(xlims)

            y_labels = ax.get_yticks()
            y_labels = np.array(y_labels)
            for i, diff in enumerate(diffs):
                y_labels[y_labels > broken_lims_scaled[i][-1]] += diff
            y_labels = [str(np.round(i * 1000) / 1000) for i in y_labels]
            ax.set_yticklabels(y_labels)

    def store_single_spectrum(self, single_spectrum, order, m_var, m_stationarity):

        if self.S_gpu[order] is None:
            self.S_gpu[order] = single_spectrum
        else:
            self.S_gpu[order] += single_spectrum

        if order == 2:
            self.S_errs[order][:, self.err_counter[order]] = single_spectrum
        else:
            self.S_errs[order][:, :, self.err_counter[order]] = single_spectrum
        self.err_counter[order] += 1

        if m_stationarity is not None:
            if order == 2:
                self.S_stationarity_temp[order][:, self.stationarity_counter[order]] = single_spectrum
            else:
                self.S_stationarity_temp[order][:, :, self.stationarity_counter[order]] = single_spectrum
            self.stationarity_counter[order] += 1

            if self.stationarity_counter[order] % m_stationarity == 0:
                if order == 2:
                    self.S_stationarity[order].append(af.mean(self.S_stationarity_temp[order], dim=1).to_ndarray())
                else:
                    self.S_stationarity[order].append(af.mean(self.S_stationarity_temp[order], dim=2).to_ndarray())
                self.stationarity_counter[order] = 0

        if self.err_counter[order] % m_var == 0:
            if order == 2:
                self.S_err_gpu = af.sqrt(
                    m_var / (m_var - 1) * (af.mean(self.S_errs[order] * af.conjg(self.S_errs[order]), dim=1) -
                                           af.mean(self.S_errs[order], dim=1) * af.conjg(
                                af.mean(self.S_errs[order], dim=1))))

            else:
                self.S_err_gpu = af.sqrt(m_var / (m_var - 1) * (
                        af.mean(self.S_errs[order] * af.conjg(self.S_errs[order]), dim=2) -
                        af.mean(self.S_errs[order], dim=2) * af.conjg(af.mean(self.S_errs[order], dim=2))))

            if self.S_err[order] is None:
                self.S_err[order] = self.S_err_gpu.to_ndarray()
            else:
                self.S_err[order] += self.S_err_gpu.to_ndarray()

            self.err_counter[order] = 0

    def calc_overlap(self, unit, imag=False, scale_t=1):
        plt.figure(figsize=(28, 13))

        overlap_s2 = [np.var(self.S_stationarity[2][:, i] * self.S[2]) for i in range(self.S_stationarity[2].shape[1])]

        overlap_s3 = [np.var(self.S_stationarity[3][:, :, i] * self.S[3]) for i in
                      range(self.S_stationarity[3].shape[2])]

        overlap_s4 = [np.var(self.S_stationarity[4][:, :, i] * self.S[4]) for i in
                      range(self.S_stationarity[4].shape[2])]

        t = np.linspace(0, self.delta_t * self.main_data.shape[0], self.S_stationarity[4][1, 1, :].shape[0]) / scale_t
        t_main = np.linspace(0, self.delta_t * self.main_data.shape[0], self.main_data.shape[0]) / scale_t

        if imag:
            overlap_s2 = np.imag(overlap_s2)
            overlap_s3 = np.imag(overlap_s3)
            overlap_s4 = np.imag(overlap_s4)

        plt.plot(t, overlap_s2 / max(overlap_s2), label='s2')
        plt.plot(t, overlap_s3 / max(overlap_s3), label='s3')
        plt.plot(t, overlap_s4 / max(overlap_s4), label='s4')

        plt.plot(t_main, self.main_data / max(self.main_data))
        plt.legend()
        plt.xlabel(unit)
        plt.ylabel('normalized')
        if not imag:
            plt.title('real part')
        else:
            plt.title('imaginary part')
        plt.show()
        return t, t_main, overlap_s2, overlap_s3, overlap_s4

    def fourier_coeffs_to_spectra(self, orders, a_w_all_gpu, f_max_ind, delta_t, m, m_var, m_stationarity,
                                  single_window, window=None, chunk_corr_gpu=None,
                                  coherent=False, random_phase=False,
                                  window_points=None):

        for order in orders:
            if order == 2:
                a_w = af.lookup(a_w_all_gpu, af.Array(list(range(f_max_ind))), dim=0)

                if self.corr_data is not None:
                    a_w_all_corr = fft_r2c(window * chunk_corr_gpu, dim0=0, scale=1)
                    a_w_corr = af.lookup(a_w_all_corr, af.Array(list(range(f_max_ind))), dim=0)
                    single_spectrum = c2(a_w, a_w_corr, m, coherent=coherent) / (
                            delta_t * (single_window ** order).sum())

                else:
                    single_spectrum = c2(a_w, a_w, m, coherent=coherent) / (delta_t * (single_window ** order).sum())

            elif order == 3:
                a_w1 = af.lookup(a_w_all_gpu, af.Array(list(range(f_max_ind // 2))), dim=0)
                a_w2 = a_w1
                a_w3 = to_gpu(calc_a_w3(a_w_all_gpu.to_ndarray(), f_max_ind, m))
                single_spectrum = c3(a_w1, a_w2, a_w3, m) / (delta_t * (single_window ** order).sum())

            else:  # order 4
                a_w = af.lookup(a_w_all_gpu, af.Array(list(range(f_max_ind))), dim=0)

                if self.corr_data is not None:
                    a_w_all_corr = fft_r2c(window * chunk_corr_gpu, dim0=0, scale=1)
                    if random_phase:
                        a_w_all_corr = add_random_phase(a_w_all_corr, window_points, delta_t, m)

                    a_w_corr = af.lookup(a_w_all_corr, af.Array(list(range(f_max_ind))), dim=0)
                else:
                    a_w_corr = a_w

                single_spectrum = c4(a_w, a_w_corr, m) / (delta_t * (single_window ** order).sum())

            self.store_single_spectrum(single_spectrum, order, m_var, m_stationarity)

    def prep_f_and_S_arrays(self, orders, f_all_in, f_max_ind, m_var, m_stationarity):
        for order in orders:
            if order == 3:
                self.freq[order] = f_all_in[:int(f_max_ind // 2)]
            else:
                self.freq[order] = f_all_in

            if order == 2:
                self.S_errs[2] = to_gpu(1j * np.empty((f_max_ind, m_var)))
            elif order == 3:
                self.S_errs[3] = to_gpu(1j * np.empty((f_max_ind // 2, f_max_ind // 2, m_var)))
            elif order == 4:
                self.S_errs[4] = to_gpu(1j * np.empty((f_max_ind, f_max_ind, m_var)))

            if m_stationarity is not None:
                if order == 2:
                    self.S_stationarity_temp[2] = to_gpu(1j * np.empty((f_max_ind, m_stationarity)))
                elif order == 3:
                    self.S_stationarity_temp[3] = to_gpu(
                        1j * np.empty((f_max_ind // 2, f_max_ind // 2, m_stationarity)))
                elif order == 4:
                    self.S_stationarity_temp[4] = to_gpu(1j * np.empty((f_max_ind, f_max_ind, m_stationarity)))
        print('Number of points: ' + str(len(self.freq[orders[0]])))

    def reset_variables(self, orders, m, m_var, m_stationarity, f_lists=None):
        self.err_counter = {2: 0, 3: 0, 4: 0}
        self.stationarity_counter = {2: 0, 3: 0, 4: 0}
        for order in orders:
            self.f_lists[order] = f_lists
            self.m[order] = m
            self.m_var[order] = m_var
            self.m_stationarity[order] = m_stationarity
            self.freq[order] = None
            self.S[order] = None
            self.S_gpu[order] = None
            self.S_err_gpu = None
            self.S_err[order] = None
            self.S_errs[order] = []
            self.S_stationarity_temp[order] = []

    def store_final_spectra(self, orders, n_chunks, n_windows, m_var):
        for order in orders:
            self.S_gpu[order] /= n_chunks
            self.S[order] = self.S_gpu[order].to_ndarray()

            self.S_err[order] /= n_windows // m_var * np.sqrt(n_windows)

    def find_datapoints_in_windows(self, data, m, start_index, T_window, frame_number, enough_data):
        windows = []
        for i in range(m):
            end_index = find_end_index(data, start_index, T_window, m, frame_number, i)
            if end_index == -1:
                enough_data = False
                break
            else:
                if start_index == end_index:
                    windows.append(None)
                else:
                    windows.append(self.data[start_index:end_index])
                start_index = end_index
        return windows, start_index, enough_data

    def calc_spec(self, order_in, T_window, f_max, backend='opencl', scaling_factor=1,
                  corr_shift=0, filter_func=False, verbose=True, coherent=False, corr_default=None,
                  break_after=1e6, m=10, m_var=10, window_shift=1, random_phase=False,
                  rect_win=False, m_stationarity=None):
        """Calculation of spectra of orders 2 to 4 with the arrayfire library."""

        af.set_backend(backend)

        if order_in == 'all':
            orders = [2, 3, 4]
        else:
            orders = order_in

        self.reset_variables(orders, m, m_var, m_stationarity)

        # -------data setup---------
        if self.data is None:
            self.data, self.delta_t = import_data(self.path, self.group_key, self.dataset)
        if self.delta_t is None:
            raise MissingValueError('Missing value for delta_t')

        n_chunks = 0
        self.T_window = T_window

        corr_shift /= self.delta_t  # conversion of shift in seconds to shift in dt

        window_points = int(np.round(T_window / self.delta_t))
        print('Actual T_window:', window_points * self.delta_t)
        self.window_points = window_points

        if self.corr_data is None and not corr_default == 'white_noise' and self.corr_path is not None:
            corr_data, _ = import_data(self.corr_data_path, self.corr_group_key, self.corr_dataset)
        elif self.corr_data is not None:
            corr_data = self.corr_data
        else:
            corr_data = None

        n_data_points = self.data.shape[0]
        n_windows = int(np.floor(n_data_points / (m * window_points)))
        n_windows = int(
            np.floor(n_windows - corr_shift / (m * window_points)))  # number of windows is reduced if corr shifted

        self.fs = 1 / self.delta_t
        freq_all_freq = rfftfreq(int(window_points), self.delta_t)
        if verbose:
            print('Maximum frequency:', np.max(freq_all_freq))

        # ------ Check if f_max is too high ---------
        f_mask = freq_all_freq <= f_max
        f_max_ind = sum(f_mask)

        single_window, _ = cgw(int(window_points), self.fs)
        window = to_gpu(np.array(m * [single_window]).flatten().reshape((window_points, 1, m), order='F'))

        self.prep_f_and_S_arrays(orders, freq_all_freq[f_mask], f_max_ind, m_var, m_stationarity)

        for i in tqdm_notebook(np.arange(0, n_windows - 1 + window_shift, window_shift), leave=False):
            chunk = scaling_factor * self.data[int(i * (window_points * m)): int((i + 1) * (window_points * m))]

            if not self.first_frame_plotted:
                plot_first_frame(chunk, self.delta_t, window_points)
                self.first_frame_plotted = True

            chunk_gpu = to_gpu(chunk.reshape((window_points, 1, m), order='F'))
            if self.corr_data == 'white_noise':  # use white noise to check for false correlations
                chunk_corr = np.random.randn(window_points, 1, m)
                chunk_corr_gpu = to_gpu(chunk_corr)
            elif self.corr_data is not None:
                chunk_corr = scaling_factor * corr_data[int(i * (window_points * m) + corr_shift): int(
                    (i + 1) * (window_points * m) + corr_shift)]
                chunk_corr_gpu = to_gpu(chunk_corr.reshape((window_points, 1, m), order='F'))
            else:
                chunk_corr_gpu = None

            if n_chunks == 0:
                if verbose:
                    print('chunk shape: ', chunk_gpu.shape[0])

            # ---------count windows-----------
            n_chunks += 1

            # -------- perform fourier transform ----------
            if rect_win:
                ones = to_gpu(
                    np.array(m * [np.ones_like(single_window)]).flatten().reshape((window_points, 1, m), order='F'))
                a_w_all_gpu = fft_r2c(ones * chunk_gpu, dim0=0, scale=1)
            else:
                a_w_all_gpu = fft_r2c(window * chunk_gpu, dim0=0, scale=1)

            # --------- modify data ---------
            if filter_func:
                pre_filter = filter_func(self.freq[2])
                filter_mat = to_gpu(
                    np.array(m * [1 / pre_filter]).flatten().reshape((a_w_all_gpu.shape[0], 1, m), order='F'))
                a_w_all_gpu = filter_mat * a_w_all_gpu

            if random_phase:
                a_w_all_gpu = add_random_phase(a_w_all_gpu, window_points, self.delta_t, m)

            # --------- calculate spectra ----------
            self.fourier_coeffs_to_spectra(orders, a_w_all_gpu, f_max_ind, self.delta_t, m, m_var, m_stationarity,
                                           single_window, window, chunk_corr_gpu=chunk_corr_gpu,
                                           coherent=coherent, random_phase=random_phase,
                                           window_points=window_points)

            if n_chunks == break_after:
                break

        self.store_final_spectra(orders, n_chunks, n_windows, m_var)

        return self.freq, self.S, self.S_err

    def calc_spec_poisson(self, order_in, T_window, f_max, f_lists=None, backend='opencl', m=10, m_var=10,
                          m_stationarity=None, full_import=False, scale_t=1,
                          sigma_t=0.14, rect_win=False):
        """

        Parameters
        ----------
        m_var: int
            number of spectra to calculate the variance from (should be set as high as possible)
        rect_win: bool
            if true no window function will be applied to the window
        scale_t: float
            scaling factor to scale timestamps and dt (not yet implemented, due to type error)
        full_import: bool
            whether to load all data into RAM (should be set true if possible)
        m_stationarity: int
            number of spectra after which their mean is stored to varify stationarity of the data
        f_lists: list of arrays
            frequencies at which the spectra will be calculated (can be multiple arrays with different frequency steps)
        sigma_t: float
            width of approximate confined gaussian windows
        order_in: array of int, str ('all')
            orders of the spectra to be calculated, e.g., [2,4]
        T_window: int
            spectra for m windows of window_points is calculated
        f_max: float
            maximum frequency of the spectra to be calculated
        backend: str
            backend for arrayfire
        m: int
            spectra for m windows of window_points is calculated
        Returns
        -------

        """

        af.set_backend(backend)

        if order_in == 'all':
            orders = [2, 3, 4]
        else:
            orders = order_in

        self.reset_variables(orders, m, m_var, m_stationarity, f_lists)

        # -------data setup---------
        if self.data is None:
            self.data, self.delta_t = import_data(self.path, self.group_key, self.dataset, full_import=full_import)
        if self.delta_t is None:
            raise MissingValueError('Missing value for delta_t')

        n_chunks = 0
        self.T_window = T_window

        if f_lists is not None:
            f_list = np.hstack(f_lists)
        else:
            f_list = None

        self.delta_t *= scale_t
        f_min = 1 / T_window
        if f_list is None:
            f_list = np.arange(0, f_max + f_min, f_min)

        start_index = 0

        enough_data = True
        f_max_ind = len(f_list)
        w_list = 2 * np.pi * f_list
        w_list_gpu = to_gpu(w_list)
        n_windows = int(self.data[-1] * scale_t // (T_window * m))
        print('number of points:', f_list.shape[0])
        print('delta f:', f_list[1] - f_list[0])

        self.prep_f_and_S_arrays(orders, f_list, f_max_ind, m_var, m_stationarity)

        for frame_number in tqdm_notebook(range(n_windows)):

            windows, start_index, enough_data = self.find_datapoints_in_windows(self.data, m, start_index,
                                                                                T_window / scale_t,
                                                                                frame_number, enough_data)
            if not enough_data:
                break

            n_chunks += 1

            a_w_all = 1j * np.empty((w_list.shape[0], m))
            a_w_all_gpu = to_gpu(a_w_all.reshape((len(f_list), 1, m), order='F'))
            for i, t_clicks in enumerate(windows):

                if t_clicks is not None:

                    t_clicks_minus_start = t_clicks - i * T_window / scale_t - m * T_window / scale_t * frame_number

                    if rect_win:
                        t_clicks_windowed = np.ones_like(t_clicks_minus_start)
                    else:
                        t_clicks_windowed, single_window, N_window_full = apply_window(T_window / scale_t,
                                                                                       t_clicks_minus_start,
                                                                                       1 / self.delta_t, sigma_t=sigma_t)

                    # ------ GPU --------
                    t_clicks_minus_start_gpu = to_gpu(t_clicks_minus_start * scale_t)
                    t_clicks_windowed_gpu = to_gpu(t_clicks_windowed).as_type(af.Dtype.c64)

                    temp1 = af.exp(1j * af.matmulNT(w_list_gpu, t_clicks_minus_start_gpu))
                    # temp2 = af.tile(t_clicks_windowed_gpu.T, w_list_gpu.shape[0])
                    # a_w_all_gpu[:, 0, i] = af.sum(temp1 * temp2, dim=1)
                    a_w_all_gpu[:, 0, i] = af.matmul(temp1, t_clicks_windowed_gpu)

                else:
                    a_w_all_gpu[:, 0, i] = to_gpu(1j*np.zeros_like(w_list))

            self.delta_t = T_window / N_window_full

            self.fourier_coeffs_to_spectra(orders, a_w_all_gpu, f_max_ind, self.delta_t, m, m_var, m_stationarity,
                                           single_window)

        assert n_windows == n_chunks, 'n_windows not equal to n_chunks'

        self.store_final_spectra(orders, n_chunks, n_windows, m_var)

        return self.freq, self.S, self.S_err

    def calc_spec_mini_bins(self, order_in, T_window, T_bin, f_max, backend='opencl', coherent=False,
                            m=10, m_var=10, m_stationarity=None, rect_win=False, verbose=False):
        """

        Parameters
        ----------
        m_stationarity: int
            number of spectra after which their mean is stored to varify stationarity of the data
        m_var: int
            number of spectra to calculate the variance from (should be set as high as possible)
        coherent: bool
            set if second moment should be used instead of cumulant
        verbose: bool
            set for more prints
        rect_win: bool
            set if no window function should be applied
        T_bin: int
            number of points in bin
        order_in: array of int, str ('all')
            orders of the spectra to be calculated, e.g., [2,4]
        T_window: int
            spectra for m windows of window_points is calculated
        f_max: float
            maximum frequency of the spectra to be calculated
        backend: str
            backend for arrayfire
        m: int
            spectra for m windows of window_points is calculated
        Returns
        -------

        """
        af.set_backend(backend)

        if order_in == 'all':
            orders = [2, 3, 4]
        else:
            orders = order_in

        self.reset_variables(orders, m, m_var, m_stationarity)

        # -------data setup---------
        if self.data is None:
            self.data, self.delta_t = import_data(self.path, self.group_key, self.dataset)
        if self.delta_t is None:
            raise MissingValueError('Missing value for delta_t')

        start_index = 0
        enough_data = True
        n_chunks = 0
        n_windows = int(self.data[-1] // (T_window * m))
        bins = int(T_window / T_bin)
        self.delta_t = T_bin

        self.fs = 1 / self.delta_t
        freq_all_freq = rfftfreq(int(bins), self.delta_t)
        if verbose:
            print('Maximum frequency:', np.max(freq_all_freq))

        # ------ Check if f_max is too high ---------
        f_mask = freq_all_freq <= f_max
        f_max_ind = sum(f_mask)
        print('preparing frequency array')
        self.prep_f_and_S_arrays(orders, freq_all_freq[f_mask], f_max_ind, m_var, m_stationarity)

        print('preparing window')
        single_window, _ = cgw(int(bins), self.fs)
        window = to_gpu(np.array(m * [single_window]).flatten().reshape((bins, 1, m), order='F'))

        print('calculating spectrum')
        for frame_number in tqdm_notebook(range(n_windows)):

            windows, start_index, enough_data = self.find_datapoints_in_windows(self.data, m, start_index, T_window,
                                                                                frame_number, enough_data)
            if not enough_data:
                break

            n_chunks += 1
            chunks = np.empty((bins, m))

            for i, t_clicks in enumerate(windows):
                t_clicks_minus_start = t_clicks - i * T_window - m * T_window * frame_number

                # --------- binning ----------

                chunk, division = np.histogram(t_clicks_minus_start, bins=bins)
                # t = division[:-1]
                chunks[:, i] = chunk

            chunk_gpu = to_gpu(chunks.reshape((bins, 1, m), order='F'))

            if n_chunks == 0:
                if verbose:
                    print('chunk shape: ', chunk_gpu.shape[0])

            # ---------count windows-----------
            n_chunks += 1

            # -------- perform fourier transform ----------
            if rect_win:
                ones = to_gpu(
                    np.array(m * [np.ones_like(single_window)]).flatten().reshape((bins, 1, m), order='F'))
                a_w_all_gpu = fft_r2c(ones * chunk_gpu, dim0=0, scale=1)
            else:
                a_w_all_gpu = fft_r2c(window * chunk_gpu, dim0=0, scale=1)

            # --------- calculate spectra ----------
            self.fourier_coeffs_to_spectra(orders, a_w_all_gpu, f_max_ind, self.delta_t, m, m_var, m_stationarity,
                                           single_window, window, coherent=coherent)

        self.store_final_spectra(orders, n_chunks, n_windows, m_var)

        return self.freq, self.S, self.S_err

    def import_spec_data_for_plotting(self, s_data, s_err, order, imag_plot):
        if imag_plot:
            s_data = np.imag(self.S[order]).copy() if s_data is None else np.imag(s_data).copy()
            if s_err is not None:
                s_err = np.imag(s_err).copy()
            elif self.S_err[order] is not None:
                s_err = np.imag(self.S_err[order]).copy()

        else:
            s_data = np.real(self.S[order]).copy() if s_data is None else np.real(s_data).copy()
            if s_err is not None:
                s_err = np.real(s_err).copy()
            elif self.S_err[order] is not None:
                s_err = np.real(self.S_err[order]).copy()

        return s_data, s_err

    def poly_plot(self, f_max=None, f_min=None, unit='Hz', sigma=1, green_alpha=0.3, arcsinh_plot=False,
                  arcsinh_const=0.02,
                  contours=False, s3_filter=0, s4_filter=0, s2_data=None, s2_err=None, s3_data=None, s3_err=None,
                  s4_data=None, s4_err=None, s2_f=None, s3_f=None, s4_f=None, imag_plot=False, plot_error=True,
                  broken_lims=None):

        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 7), gridspec_kw={"width_ratios": [1, 1.2, 1.2]})
        plt.rc('text', usetex=False)
        plt.rc('font', size=10)
        plt.rcParams["axes.axisbelow"] = False

        if self.f_lists[2] is not None:
            broken_lims = []
            for part in self.f_lists[2]:
                broken_lims.append((part[0], part[-1]))

        s_data_plot = {2: None, 3: None, 4: None}
        s_err_plot = {2: None, 3: None, 4: None}
        s_f_plot = {2: None, 3: None, 4: None}

        # -------- S2 ---------
        order = 2
        if self.S[order] is not None and not self.S[order].shape[0] == 0:
            s_data_plot[order], s_err_plot[order] = self.import_spec_data_for_plotting(s2_data, s2_err, order,
                                                                                       imag_plot)

            s2_err_p = []
            s2_err_m = []

            if s_err_plot[order] is not None or self.S_err[2] is not None:
                for i in range(0, 5):
                    s2_err_p.append(s_data_plot[order] + (i + 1) * s_err_plot[order])
                    s2_err_m.append(s_data_plot[order] - (i + 1) * s_err_plot[order])

            if arcsinh_plot:
                s_data_plot[order], s2_err_p, s2_err_m = arcsinh_scaling(s_data_plot[order], arcsinh_const, order,
                                                                         s_err_p=s2_err_p, s_err_m=s2_err_m)

            if s2_f is None:
                s_f_plot[order] = self.freq[2].copy()
            else:
                s_f_plot[order] = s2_f

            if broken_lims is not None:
                s_f_plot[order], diffs, broken_lims_scaled = connect_broken_axis(s_f_plot[order], broken_lims)
            else:
                diffs = None
                broken_lims_scaled = None

            if f_max is None:
                f_max = s_f_plot[order].max()
            if f_min is None:
                f_min = s_f_plot[order].min()
            ax[0].set_xlim([f_min, f_max])

            if plot_error and (s_err_plot[order] is not None or self.S_err[2] is not None):
                for i in range(0, 5):
                    ax[0].plot(s_f_plot[order], s2_err_p[i], color=[0.1 * i + 0.3, 0.1 * i + 0.3, 0.1 * i + 0.3],
                               linewidth=2, label=r"$%i\sigma$" % (i + 1))
                    ax[0].plot(s_f_plot[order], s2_err_m[i], color=[0.1 * i + 0.3, 0.1 * i + 0.3, 0.1 * i + 0.3],
                               linewidth=2, label=r"$%i\sigma$" % (i + 1))

            ax[0].plot(s_f_plot[order], s_data_plot[order], color=[0, 0.5, 0.9], linewidth=3)

            ax[0].tick_params(axis='both', direction='in')
            ax[0].set_ylabel(r"$S^{(2)}_z$ (" + unit + r"$^{-1}$)", labelpad=13, fontdict={'fontsize': 14})
            ax[0].set_xlabel(r"$\omega / 2\pi$ (" + unit + r")", labelpad=13, fontdict={'fontsize': 14})
            ax[0].set_title(r"$S^{(2)}_z$ (" + unit + r"$^{-1}$)", fontdict={'fontsize': 16})

            if broken_lims is not None:
                ylims = ax[0].get_ylim()
                for i, diff in enumerate(diffs):
                    ax[0].vlines(broken_lims_scaled[i][-1] - sum(diffs[:i]), ylims[0], ylims[1], linestyles='dashed')

                ax[0].set_ylim(ylims)
                x_labels = ax[0].get_xticks()
                x_labels = np.array(x_labels)
                for i, diff in enumerate(diffs):
                    x_labels[x_labels > broken_lims_scaled[i][-1]] += diff
                x_labels = [str(np.round(i * 1000) / 1000) for i in x_labels]
                ax[0].set_xticklabels(x_labels)

        # -------- S3 and S4 ---------

        cmap = colors.LinearSegmentedColormap.from_list('', [[0.1, 0.1, 0.8], [0.97, 0.97, 0.97], [1, 0.1, 0.1]])
        color_array = np.array([[0., 0., 0., 0.], [0., 0.5, 0., green_alpha]])
        cmap_sigma = LinearSegmentedColormap.from_list(name='green_alpha', colors=color_array)

        for order in [3, 4]:
            if self.S[order] is not None and not self.S[order].shape[0] == 0:

                if order == 3:
                    s_data = s3_data
                    s_err = s3_err
                    s_filter = s3_filter
                    s_f = s3_f
                else:  # order 4
                    s_data = s4_data
                    s_err = s4_err
                    s_filter = s4_filter
                    s_f = s4_f

                s_data_plot[order], s_err_plot[order] = self.import_spec_data_for_plotting(s_data, s_err, order,
                                                                                           imag_plot)

                if s_err_plot[order] is not None or self.S_err[order] is not None:
                    s_err_plot[order] *= sigma

                if arcsinh_plot:
                    s_data_plot[order], s_err_plot[order] = arcsinh_scaling(s_data_plot[order], arcsinh_const, order,
                                                                            s_err=s_err_plot[order])

                if s_f is None:
                    s_f_plot[order] = self.freq[order].copy()
                else:
                    s_f_plot[order] = s_f

                if broken_lims is not None:
                    s_f_plot[order], diffs, broken_lims_scaled = connect_broken_axis(s_f_plot[order], broken_lims)
                else:
                    diffs = None
                    broken_lims_scaled = None

                vmin = np.min(s_data_plot[order])
                vmax = np.max(s_data_plot[order])
                if vmin > 0:
                    vmin = -vmax / 20
                if vmax < 0:
                    vmax = -vmin / 20
                norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
                # norm = MidpointNormalize(midpoint=0, vmin=vmin, vmax=vmax)

                y, x = np.meshgrid(s_f_plot[order], s_f_plot[order])
                z = s_data_plot[order].copy()
                err_matrix = np.zeros_like(z)
                if s_err_plot[order] is not None or self.S_err[order] is not None:
                    err_matrix[np.abs(s_data_plot[order]) < s_err_plot[order]] = 1

                axis = order - 2
                c = ax[axis].pcolormesh(x, y, z, cmap=cmap, norm=norm, zorder=1, shading='auto')
                if s_err_plot[order] is not None or self.S_err[order] is not None:
                    ax[axis].pcolormesh(x, y, err_matrix, cmap=cmap_sigma, vmin=0, vmax=1, shading='auto')

                if contours:
                    ax[axis].contour(x, y, gaussian_filter(z, s_filter), colors='k', linewidths=0.7)

                if f_max is None:
                    f_max = s_f_plot[order].max()
                if f_min is None:
                    f_min = s_f_plot[order].min()
                ax[axis].axis([f_min, f_max, f_min, f_max])

                ax[axis].set_xlabel(r"$\omega_1 / 2 \pi$ (" + unit + r")", fontdict={'fontsize': 14})
                ax[axis].set_ylabel(r"$\omega_2 / 2 \pi$ (" + unit + r")", fontdict={'fontsize': 14})
                ax[axis].tick_params(axis='both', direction='in')

                if green_alpha == 0:
                    ax[axis].set_title(
                        r'$S^{(' + f'{order}' + r')}_z $ (' + unit + r'$^{-' + f'{order - 1}' + r'}$)',
                        fontdict={'fontsize': 16})
                else:
                    ax[axis].set_title(
                        r'$S^{(' + f'{order}' + r')}_z $ (' + unit + r'$^{-' + f'{order - 1}' + r'}$) (%i$\sigma$ confidence)' % (
                            sigma),
                        fontdict={'fontsize': 16})
                fig.colorbar(c, ax=(ax[axis]))

                if broken_lims is not None:
                    ylims = ax[axis].get_ylim()
                    for i, diff in enumerate(diffs):
                        ax[axis].vlines(broken_lims_scaled[i][-1] - sum(diffs[:i]), ylims[0], ylims[1],
                                        linestyles='dashed')
                        ax[axis].hlines(broken_lims_scaled[i][-1] - sum(diffs[:i]), ylims[0], ylims[1],
                                        linestyles='dashed')

                    ax[axis].set_ylim(ylims)
                    ax[axis].set_xlim(ylims)

                    x_labels = ax[axis].get_xticks()
                    x_labels = np.array(x_labels)
                    for i, diff in enumerate(diffs):
                        x_labels[x_labels > broken_lims_scaled[i][-1]] += diff
                    x_labels = [str(np.round(i * 1000) / 1000) for i in x_labels]
                    ax[axis].set_xticklabels(x_labels)
                    ax[axis].set_yticklabels(x_labels)

        plt.show()

        return fig

# brownian_motion_generator.py

'''
A series of functions to generate mean-reverting (or non mean reverting) Brownian motion simulations (via Ornstein–Uhlenbeck process) for multiple correlated processes.
This is particularly useful for running Monte Carlo simulations for complex systems, which typically invole multiple evolving processes that may be mean reverting and/or co-evolve according to a correlated relationship.
This library can handle:
 - series which are only positive (suggest transforming to log normal changes if the mean is not stable in raw form)
 - series with skewed and/or kurtotic distributions
 - correlated or inversely correlated series
Does not currently handle:
 - series which are only 0 or positive. One possible approach to synthetically duplicate the series with -1 * each sample, then take the absolute value of samples before applying any correlation adjustment
Original credit to these two resources which were the building blocks:
https://towardsdatascience.com/stochastic-processes-simulation-brownian-motion-the-basics-c1d71585d9f9
https://gist.github.com/raddy/4084ade3d3a82911d43df9375f9697f4
'''

from typing import Optional, Union
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.stats import skew, kurtosis
import statsmodels.sandbox.distributions.extras as extras
import scipy.interpolate as interpolate
import tqdm
import warnings

@dataclass
class OUParams:
    alpha: float  # mean reversion parameter
    gamma: float  # asymptotic mean
    beta: float  # Brownian motion scale (standard deviation)
    X_0: Optional[float] = None # initial starting value (otherwise gamma is used)
    distribution_type: Optional[str] = 'normal' # Type of distriubtion: normal, laplace, or custom
    distribution: Optional[list] = None # If custom: the created synthetic distribution which is sampled to create random walks for this process


def estimate_OU_params(
    X_t: np.ndarray,
    distribution_type: Optional[str] = 'normal'
) -> OUParams:
    """
    Estimate OU params from OLS regression.
    - X_t is a 1D array of the data series in question
    - distbributon_type: a string indicating the type of distrbution to sample for creating simulations of this series
    Returns instance of OUParams.
    """
    y = np.diff(X_t)
    X = X_t[:-1].reshape(-1, 1)
    reg = LinearRegression(fit_intercept=True)
    reg.fit(X, y)
    # regression coeficient and constant
    alpha = -reg.coef_[0]
    gamma = reg.intercept_ / alpha
    # residuals and their standard deviation
    y_hat = reg.predict(X)
    beta = np.std(y - y_hat)

    X_skew = skew(X_t)
    X_kurt = kurtosis(X_t)

    if distribution_type == 'custom':
        #Expand standard normal distribution to best approximate skew and kurtosis of provided series
        X_mean = 0
        X_variance = 1
        distribution = _create_custom_distribution(X_mean,X_variance,X_skew,X_kurt)
    elif distribution_type == 'normal' and (X_kurt > 1.5):
        #Common mistake in financial modeling is to use normal distribution when fat tail risk (kurtosis) is high
        #Empiricially laplace is a much better standard distributin to use in financial modeling
        # https://arxiv.org/pdf/1906.10325.pdf
        warnings.warn("Applying normal distribution with a series that has high (excess) kurtosis, consider using laplace or a custom fit distribution.")
        distribution = None
    else:
        distribution = None

    return OUParams(alpha, gamma, beta, distribution_type=distribution_type, distribution=distribution)


def simulate_corr_OU_procs(
    T: int,
    OU_params: tuple,
    RUNS: int,
    rho: Optional[tuple] = None,
    initial_random_state: Optional[int] = 0,
) -> np.ndarray:
    """
    Simulate multiple OU processes correlated with the first (primary) OU process.
        Creates a 2D array of n_procs discrete Brownian Motion increments dW for each simulation.
        Each column of the array per each simulation is one process.
        So the resulting shape of the array is (RUNS, T, n_procs).
        Correlation can be None (0 correlation between each process and the first process),
        or a tuple of correlations (floats form -1 to +1) the same length as the number of processes to be simulated,
        with each respective correlation representing that processes' correlation with the first (primary) process.
    - T is the integer number of timesteps to generate for each process, for each simulation
    - OU_params is a tuple of OUParams. When using tuple with length more than 1
        to simulate multiple processes in parallel, each column in the resulting 2D array
        corresponds to the tuple index
    - RUNS is the integer number of total runs/simulations to generate
    - rho is a tuple of correlation coefficients between each process and the first (primary) OU process
    - initial_random_state optional integer for initial random seed in order to make results reproduceable
    """
    
    _n_procs = len(OU_params) #_n_procs is the number of seperate processes to generate for each simulation
    
    #Ensure if rho is a tuple, that it is the same length as _n_procs
    if rho is not None:
        if len(rho) != _n_procs:
            raise ValueError("Tuple for rho must be equal in length to number of processes to simulate - length of OU_params.")
    
    all_run_corr_dWs = []
    
    for run in tqdm.tqdm(range(0,RUNS)):
        random_state = initial_random_state + run #random_state is iterated each process and run to ensure unique random state for every process
        
        corr_dWs = _get_corr_dW_matrix(
            T, OU_params, run, rho, random_state,
        )
        
        OU_procs = []
        for i in range(_n_procs):
            OU_params_i = OU_params[i]
            dW_i = corr_dWs[:, i]
            OU_procs.append(_get_OU_process_i(T, OU_params_i, dW_i))
        all_run_corr_dWs.append(np.asarray(OU_procs).T)
    return np.asarray(all_run_corr_dWs)


def _create_custom_distribution(
    mean: float, 
    variance: float, 
    skew: float, 
    kurt: float,
    dist_size: Optional[int] = 1_000_000, 
    sd_wide: Optional[int] = 10
) -> np.ndarray:
    '''
    Applies the Gram-Charlier expansion to the normal distribution to approximate a distribution with the provided mean, variance, skew, and kurtosis.
    See: https://www.statsmodels.org/dev/generated/statsmodels.sandbox.distributions.extras.pdf_mvsk.html
        - mean: the desired mean of the expanded normal distribution
        - variance: the desired variance of the expanded normal distribution
        - skew: the desired skew of the expanded normal distribution
        - kurt: the desired (excess) kurtosis of the expanded normal distribution
        - dist_size: the number of finite points used to approximate the continuous custom distribution
        - sd_wide: the range of standard deviations from the mean over which the disribution is creatd
    Returns a discrete array of "dist_size" length that approximates the continues distribtion matching the provided characteristics.
    '''
    sigma = variance ** .5
    f = extras.pdf_mvsk([mean, sigma, skew, kurt])
    x = np.linspace(mean - sd_wide * sigma, mean + sd_wide * sigma, num=dist_size)
    norm_x =  ((x/sd_wide) + 1) / 2 #normalized between 0-1
    y = [f(i) for i in x]
    yy = np.cumsum(y) / np.sum(y)
    inv_cdf = interpolate.interp1d(yy, x, fill_value="extrapolate")
    dist = inv_cdf(norm_x).clip(min=-sd_wide, max=sd_wide)
    #Correct any drift in target mean created in the discrete distribution approximation of the cdf
    dist = (dist - (dist.mean() - mean))
    return dist


def _get_corr_dW_matrix(
    T: int,
    OU_params: tuple,
    run: int,
    rho: Optional[float] = None,
    random_state: Optional[int] = None,
) -> np.ndarray:
    """
    Creates a 2D array of n_procs discrete Brownian Motion increments dW for a given simulation.
    Each column of the array is one process.
    So that the resulting shape of the array is (T, n_procs).
        - T is the number of timesteps of each process
        - OU_params is the tuple of OU_params for the processes to simulate
        - run is the integer representation of the current run/simulation
        - rho is the correlation constant used to generate a new process
            which has rho correlation to the first (primary) random process already generated,
            hence rho is only an approximation to the pairwise correlation
        - Optional random_state to reproduce results
    """
    
    dWs = []
    _n_procs = len(OU_params)
    for i in range(_n_procs):
        random_state_i = _get_random_state_i(random_state, i, _n_procs, run)
        if i == 0 or rho is None:
            dW_i = _get_dW(T, OU_params[i], random_state=random_state_i)
        else:
            dW_i = _get_correlated_dW(dWs[0], OU_params[i], rho[i], random_state_i) #Get a new dW correlated with the primary dW process
        dWs.append(dW_i)
    return np.asarray(dWs).T


def _get_dW(
    T: int,
    OU_params: OUParams,
    random_state: Optional[int] = None
) -> np.ndarray:
    """
    Sample T times from the distribution to simulate discrete increments (dW) of a Brownian Motion.
    - T: number of timesteps
    - OU_params: instance of OUParams for the series being simulated
    - random_state: optional random_state to reproduce results
    Uses np.random.default_rng for randomness as best practice over np.random.seed
    See: https://albertcthomas.github.io/good-practices-random-number-generators/
    """
    dW_rng = np.random.default_rng(random_state)
    if OU_params.distribution_type == 'normal':
        return dW_rng.normal(0.0, 1.0, T)
    elif OU_params.distribution_type == 'laplace':
        return dW_rng.laplace(0.0, 1.0 / 2**.5, T)
    elif OU_params.distribution_type == 'custom':
        return dW_rng.choice(OU_params.distribution, size=T, replace=True)
    else:
        raise ValueError("Unrecognized distribution_type provided for OU_params: ", OU_params)


def _get_correlated_dW(
    dW: np.ndarray,
    OU_params: OUParams,
    rho: float,
    random_state: Optional[int] = None
) -> np.ndarray:
    """
    Sample correlated discrete Brownian increments to given increments dW.
    """
    dW2 = _get_dW(
        len(dW), OU_params, random_state=random_state
    )  # generate Brownian icrements.
    if np.array_equal(dW2, dW):
        # dW cannot be equal to dW2.
        raise ValueError(
            "Brownian Increment error, try choosing different random state."
        )
    return rho * dW + np.sqrt(1 - rho ** 2) * dW2


def _get_random_state_i(
    random_state: Optional[int],
    i: int,
    num_procs: int,
    run: int
) -> Optional[int]:
    """
    Iterates the random_state each process in each simulation, so that every process has a unique random_state.
    This ensures there is no random_state used by any 2 processes, even across different simulation steps.
    """
    return random_state if random_state is None else random_state + i + (run * num_procs)


def _get_OU_process_i(
    T: int,
    OU_params: OUParams,
    dW: np.ndarray
) -> np.ndarray:
    """
    Simulates the OU process with an external dW.
    X_0 is taken as the asymptotic mean gamma if it is None.
    """
    t = np.arange(T, dtype=np.float64)  # float to avoid np.exp overflow
    exp_alpha_t = np.exp(-OU_params.alpha * t)
    integral_W = _get_integal_W(t, dW, OU_params)
    
    if OU_params.X_0 is None:
        OU_params.X_0 = OU_params.gamma
    
    return (
        OU_params.X_0 * exp_alpha_t
        + OU_params.gamma * (1 - exp_alpha_t)
        + OU_params.beta * exp_alpha_t * integral_W
    )


def _get_integal_W(
    t: np.ndarray,
    dW: np.ndarray,
    OU_params: OUParams
) -> np.ndarray:
    """
    Integral with respect to Brownian Motion (W), ∫...dW.
    """
    exp_alpha_s = np.exp(OU_params.alpha * t)
    integral_W = np.cumsum(exp_alpha_s * dW)
    return np.insert(integral_W, 0, 0)[:-1]
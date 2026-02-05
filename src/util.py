import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis, wasserstein_distance
from joblib import Parallel, delayed

from src.stationary_block_bootstrap import *

def calculate_simulation_moments(sims:np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    bootstrap_mean = np.mean(sims, axis=1)
    bootstrap_std = np.std(sims, axis=1)
    bootstrap_skew = skew(sims, axis=1)
    bootstrap_kurt = kurtosis(sims, axis=1)
    return bootstrap_mean, bootstrap_std, bootstrap_skew, bootstrap_kurt

def calculate_actual_moments(data:np.ndarray) -> tuple[float, float, float, float]:
    actual_mean = np.mean(data)
    actual_std = np.std(data)
    actual_skew = skew(data)
    actual_kurt = kurtosis(data)
    return actual_mean, actual_std, actual_skew, actual_kurt

def calculate_abs_distance_from_median(target:float, actual:float) -> float:
    return np.abs(np.median(target) - actual)

def generate_timestep_sims(data:np.ndarray, n_sims:int, avg_block_size:int, seed:int) -> list[np.ndarray]:
    t_steps = [int(np.ceil(len(data)*i)) for i in np.arange(0.1, 1.0+0.1, 0.1)]
    sims = Parallel(n_jobs=-2)(
        delayed(stationary_bootstrap)(data, n_sims, t, avg_block_size, seed+i)
        for i, t in enumerate(t_steps)
    )
    return sims

def average_wasserstein(data:np.ndarray, sim:np.ndarray) -> float:
    return np.mean([wasserstein_distance(path, data) for path in sim])

def calculate_average_wasserstein(data:np.ndarray, sims:np.ndarray) -> list[float]:
    expected_distance = Parallel(n_jobs=-2)(
        delayed(average_wasserstein)(data, sim) 
        for sim in sims
    )
    return expected_distance

def get_median_distance_df(data:np.ndarray, sims:np.ndarray) -> pd.DataFrame:
    results = []
    t_steps = [int(np.ceil(len(data)*i)) for i in np.arange(0.1, 1.0+0.1, 0.1)]
    actual_mean, actual_std, actual_skew, actual_kurt = calculate_actual_moments(data)
    for sim in sims:
        mu, vol, s, k = calculate_simulation_moments(sim)
        entry = {
            'mu_median_distance': calculate_abs_distance_from_median(mu, actual_mean),
            'std_median_distance':  calculate_abs_distance_from_median(vol, actual_std),
            'skew_median_distance': calculate_abs_distance_from_median(s, actual_skew),
            'kurt_median_distance': calculate_abs_distance_from_median(k, actual_kurt)
        }
        results.append(entry)

    results = pd.DataFrame(results)
    results['timesteps'] = t_steps
    return results
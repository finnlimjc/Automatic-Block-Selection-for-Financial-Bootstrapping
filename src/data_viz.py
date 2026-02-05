import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf
from src.util import *

class ACFPlot:
    def __init__(self, data:np.ndarray, sims:np.ndarray, max_lag:int, alpha:float=0.05):
        self.data = data.copy()
        self.sims = sims.copy()
        self.max_lag = int(max_lag)
        self.alpha = alpha
    
    def _acf_results(self) -> tuple[np.ndarray, np.ndarray]:
        acf_u = acf(self.data, nlags=self.max_lag)
        acf_b  = np.array([acf(self.sims[i], nlags=self.max_lag) for i in range(len(self.sims))])
        return (acf_u, acf_b)
    
    def _get_bounds(self) -> tuple[float, float]:
        interval = self.alpha*100/2
        lb, ub = interval, 100-interval
        return (lb, ub)
    
    def _bootstrap_stats(self, acf_b:np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        lb, ub = self._get_bounds()
        acf_b_mean = acf_b.mean(axis=0)
        acf_b_lo = np.percentile(acf_b, lb, axis=0)
        acf_b_hi = np.percentile(acf_b, ub, axis=0)
        return (acf_b_mean, acf_b_lo, acf_b_hi)
    
    def plot_acf_band(self, title:str, figsize:tuple[int,int]=(8,5)) -> plt.Figure:
        acf_u, acf_b = self._acf_results()
        acf_b_mean, acf_b_lo, acf_b_hi = self._bootstrap_stats(acf_b)
        lags = np.arange(self.max_lag+1)
        
        plt.figure(figsize=figsize)
        plt.fill_between(
            lags, acf_b_lo, acf_b_hi,
            color='lightblue', alpha=0.4, label=f'Bootstrap {100-self.alpha*100}% CI'
        )
        
        plt.plot(lags, acf_b_mean, color='blue', linewidth=2, label='Bootstrap Mean ACF')
        plt.plot(lags, acf_u, color='black', linestyle='--', linewidth=2, label='Underlying ACF')
        plt.axhline(0, color='gray', linewidth=1)
        
        plt.xlabel("Lag")
        plt.ylabel("ACF")
        plt.title(str(title))
        plt.legend()
        
        plt.grid(alpha=0.3)
        plt.tight_layout()
        return plt.gcf()

class CompareMoments:
    def __init__(self, data:np.ndarray, sims:np.ndarray):
        self.data = data.copy()
        self.sims = sims.copy()
        self.titles = ["First Central Moment: Mean (%)", "Second Central Moment: Volatility (%)", "Third Central Moment: Skewness", "Fourth Central Moment: Kurtosis"]
    
    def _plot_moment_distributions(self, ax, sim_moments:np.ndarray, actual_moment:float, title:str) -> plt.Figure:
        ax.hist(sim_moments, bins=50, density=True)
        ax.axvline(actual_moment, color='red', linestyle='--')
        ax.set_title(title)
    
    def plot(self, figsize:tuple[int,int]=(15,10)) -> plt.Figure:
        bootstrap_mean, bootstrap_std, bootstrap_skew, bootstrap_kurt = calculate_simulation_moments(self.sims)
        actual_mean, actual_std, actual_skew, actual_kurt = calculate_actual_moments(self.data)
        
        fig, axes = plt.subplots(ncols=2,nrows=2, figsize=figsize)
        self._plot_moment_distributions(axes[0][0], bootstrap_mean*100, actual_mean*100, self.titles[0])
        self._plot_moment_distributions(axes[0][1], bootstrap_std*100, actual_std*100, self.titles[1])
        self._plot_moment_distributions(axes[1][0], bootstrap_skew, actual_skew, self.titles[2])
        self._plot_moment_distributions(axes[1][1], bootstrap_kurt, actual_kurt, self.titles[3])
        return fig
import streamlit as st
from datetime import date

from src.data_io import *
from src.data_viz import *
from src.util import *

class ParamsSelector:
    def select_stock_info(self) -> str:
        st.subheader("💰 Ticker Information")
        symbol = st.text_input("Yahoo Finance Ticker Symbol", value='SPY')
        return str(symbol)
    
    def select_date(self) -> tuple[str, str]:
        st.subheader("📅 Select Date Range")
        default_start = date(2000, 1, 1)
        default_end = date(2025, 12, 31)
        start_date = st.date_input("Start Date", default_start, min_value=default_start, max_value=default_end)
        end_date = st.date_input("End Date", default_end, min_value=default_start, max_value=default_end)
        
        if start_date > end_date:
            st.error("Start date must be before end date.")
            return None
        
        # For YahooFinance
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        
        return (start_date, end_date)
    
    def render(self) -> dict:
        with st.sidebar:
            st.header("⚙️ Parameter Selector")
            symbol = self.select_stock_info()
            start_date, end_date = self.select_date()
            
            st.divider()

            yf_params = {
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date
            }
            
            return yf_params

@st.cache_data
def get_data(symbol:str, start_date:str, end_date:str) -> np.ndarray:
    yf = YahooFinance(symbol, start_date, end_date)
    df = yf.pipeline()
    data = df['log_return'].dropna().values
    return data

@st.cache_data
def get_sims(data:np.ndarray, n_sims:int, avg_block_size:int, seed:int) -> np.ndarray:
    sims = generate_timestep_sims(data, n_sims, avg_block_size, seed)
    return sims
    
def acf_plot(data:np.ndarray, sims:np.ndarray, max_lag:int, alpha:float, title:str, figsize:tuple[int,int]) -> plt.Figure:
    vc = ACFPlot(data, sims, max_lag, alpha)
    fig = vc.plot_acf_band(title=title, figsize=figsize)
    return fig

def acf_sq_plot(data:np.ndarray, sims:np.ndarray, max_lag:int, alpha:float, title:str, figsize:tuple[int,int]) -> plt.Figure:
    vc = ACFPlot(data**2, sims**2, max_lag, alpha)
    fig = vc.plot_acf_band(title=title, figsize=figsize)
    return fig

def wasserstein_plot(data:np.ndarray, sims:np.ndarray, figsize:tuple[int,int]) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    expected_distances = calculate_average_wasserstein(data, sims)
    t_steps = [int(np.ceil(len(data)*i)) for i in np.arange(0.1, 1.0+0.1, 0.1)]
    ax.plot(t_steps, expected_distances)
    ax.set_title("Wasserstein Distance with Longer Timesteps")
    ax.set_xlabel("Timestep")
    ax.set_ylabel("Expected Wasserstein Distance")
    return fig

def plot_moments(data:np.ndarray, sim:np.ndarray, figsize:tuple[int,int]) -> plt.Figure:
    cm = CompareMoments(data, sim)
    fig = cm.plot(figsize=figsize)
    return fig

def plot_median_distance(data:np.ndarray, sims:np.ndarray, figsize:tuple[int,int]) -> plt.Figure:
    results = get_median_distance_df(data, sims)
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=figsize)
    titles = ['Mean Absolute Distance from Median', 'Volatility Absolute Distance from Median', 'Skewness Absolute Distance from Median', 'Kurtosis Absolute Distance from Median']

    for ax, col, title in zip(axes.flat, results.columns[:-1], titles):
        ax.plot(results['timesteps'], results[col])
        ax.set_title(title, fontsize=10)
    
    return fig

if __name__ == '__main__':
    # Initial Params
    selector = ParamsSelector()
    yf_params = selector.render()
    n_sims = 1000
    seed = 123
    max_lag = 50
    alpha = 0.05
    
    # Initial Set Up
    st.set_page_config(layout="wide")
    st.header("📊 Stationary Block Bootstrap")
    
    # Simulation Data
    data = get_data(**yf_params)
    avg_block_size = OptimalBlockSize(data**2).optimal_stationary_block_size()
    avg_block_size = int(np.ceil(avg_block_size))
    sims = get_sims(data, n_sims, avg_block_size, seed)
    
    col1a, col1b = st.columns((0.4, 0.6))
    with col1a:
        fig1a = acf_plot(data, sims[-1], max_lag, alpha, f'Log Returns ACF with Average Block Size={avg_block_size}', (10,3))
        fig2a = acf_sq_plot(data, sims[-1], max_lag, alpha, f'Volatility Clustering ACF with Average Block Size={avg_block_size}', (10,3))
        st.pyplot(fig1a)
        st.pyplot(fig2a)
        
        fig3a = plot_moments(data, sims[-1], (16, 15))
        st.pyplot(fig3a)
    
    with col1b:
        fig1b = wasserstein_plot(data, sims, (10, 3.5))
        st.pyplot(fig1b)
        
        fig2b = plot_median_distance(data, sims, (10, 6))
        st.pyplot(fig2b)
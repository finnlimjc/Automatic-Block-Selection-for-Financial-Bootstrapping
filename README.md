# Instructions
1. Create a virtual environment:
```sh
# Open a terminal and navigate to your project folder
cd myproject

# Create the .venv folder
python -m venv .venv
```

2. Activate the virtual environment:
```sh
# Windows command prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS and LinuxS
source .venv/bin/activate
```

3. Install packages in the environment:
```sh
python -m pip install -r requirements.txt
```

4. Run the dashboard:
```sh
streamlit run app.py
```

5. Alternatively, if you have already completed the virtual environment and packages installation, run the appropriate commands as follows:
```sh
cd myproject
.venv\Scripts\activate
python -m streamlit run app.py
```

# Dashboard
<img width="1141" height="638" alt="image" src="https://github.com/user-attachments/assets/14100abf-92eb-45a7-991c-b537c975fbd6" />

# Automatic Block Size Selection Methodology for SBB
The best expected blocksize for the SBB is determined by minimizing the MSE as denoted:

$$
\text{MSE}(\hat{\sigma}_b^2) = 
\underbrace{\text{Bias}^2}_{\text{block too short}} + 
\underbrace{\text{Variance}}_{\text{blocks too long}}
$$

Here, we can break it down into its components:

$$Bias[\hat{\sigma}^2_b] = E[\sigma^2_b] - \sigma^2_{\infty} = -\frac{1}{b}G + o\left(\frac{1}{b}\right)$$

$$V[\hat{\sigma}^2_b] = \frac{b}{N}D + o\left(\frac{b}{N}\right)$$

$$G = \sum^\infty_{k=-\infty}|k|R(k) \qquad D = 2g^2(0) \qquad g(\omega) = \sum^\infty_{s=-\infty}R(s)cos(\omega s)$$

After differentiating w.r.t $b$, we can minimize MSE:

$$b = \left(\frac{2G^2}{D}\right)^{1/3} N^{1/3}$$

$$\text{MSE}(\hat{\sigma}_b^2) \approx \frac{3}{2^{2/3}}\frac{G^{2/3}D^{2/3}}{N^{2/3}}$$

However, the infinite sum is intractable in practice, so we will use the following approximations:

$$\hat{g}(\omega) = \sum^M_{k=-M}\lambda(k/M)\hat{R}(k)cos(\omega k)$$

$$\hat{G} = \sum^M_{k=-M}\lambda(k/M)|k|\hat{R}(k)$$

$$\hat{R}(k) = \frac{1}{N}\sum^{N-|k|}_{i=1}(X_i - \bar{X}_N)(X_{i+|k|} - \bar{X}_N)$$

$$
\lambda(t) = 
\begin{cases}
1 & \text{if } |t| \in [0, 0.5] \\
2(1 - |t|) & \text{if } |t| \in [0.5, 1] \\
0 & \text{otherwise}
\end{cases}
$$

where $t$ represents the ratio $k/M$, $k$ is the lag and $M$ is the chosen bandwidth.

Note that $M$ is set to $2\hat{m}$, where $\hat{m}$ is the point at which the smallest autocorrelation lag is not statistically significant from 0. Below are the steps:
1. Let $\hat{p}(k) = \hat{R}(k)/\hat{R}(0)$.
2. $\hat{m}$ is the smallest positive integar such that $|\hat{p}(\hat{m}+k)| < c\sqrt{logN/N}$, where $c>0$ is a fixed constant.
3. Set $M = 2\hat{m}$.

For a more detailed explanation, refer to: ```automatic_block_selection.ipynb```

# References
- Politis, D. N., & White, H. (2004). Automatic Block-Length Selection for the Dependent Bootstrap. Econometric Reviews, 23(1), 53–70. https://doi.org/10.1081/ETC-120028836
- Patton, A., Politis, D. N., & White, H. (2009). Correction to “Automatic Block-Length Selection for the Dependent Bootstrap” by D. Politis and H. White. Econometric Reviews, 28(4), 372–375. https://doi.org/10.1080/07474930802459016

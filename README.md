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

# References
- Politis, D. N., & White, H. (2004). Automatic Block-Length Selection for the Dependent Bootstrap. Econometric Reviews, 23(1), 53–70. https://doi.org/10.1081/ETC-120028836
- Patton, A., Politis, D. N., & White, H. (2009). Correction to “Automatic Block-Length Selection for the Dependent Bootstrap” by D. Politis and H. White. Econometric Reviews, 28(4), 372–375. https://doi.org/10.1080/07474930802459016

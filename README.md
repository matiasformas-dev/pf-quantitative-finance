# pf-quantitative-finance
#========================================
Programming In Finance Course Repo - UAI
#========================================

this is a project that i create due to a course in Adolfo Ibañez University.

Currently, this repository contains a simple Python script that downloads daily closing prices for three assets from Yahoo Finance and calculates basic risk statistics.

What the script does:
- Requests historical daily close prices for IVV, ILF and SOXX with `start='2024-01-01'` and `end='2026-09-30'`.
- Uses yfinance to fetch the data.
- Calculates daily returns with pct_change().
- Calculates the variance-covariance matrix of the returns.
- Prints the price dataframe, return dataframe and covariance matrix to the console.

This is not a portfolio optimizer, forecasting model, or a full analysis tool yet. The current implementation only prepares the data and computes the basic statistics shown above.

Requirements:
- Python 3
- pandas
- numpy
- yfinance
- openpyxl

To run it:
1. Create and activate a virtual environment.
2. Install dependencies with: pip3 install -r requirements.txt
3. Run the script with: python3 main.py

The script relies on Yahoo Finance as the data source, so availability and data access depend on that service.

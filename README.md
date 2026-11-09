# pf-quantitative-finance

Programming In Finance Course Repo - UAI

This project was created for a course at Adolfo Ibáñez University.

## Current implementation

`main.py` is a simple portfolio-volatility script. It downloads daily closing prices for IVV, ILF, and SOXX from Yahoo Finance for the date range specified in the script (`2024-01-01` to `2026-09-30`) and then:

- Calculates daily percentage returns.
- Computes the covariance matrix of those returns.
- Calculates portfolio variance using the fixed weights `[0.5, 0.3, 0.2]` and prints annualized volatility using 252 trading days per year.
- Prints the downloaded prices, daily returns, covariance matrix, weights, and intermediate arrays to the console.

The script uses fixed tickers, dates, and weights. It does not provide a portfolio optimizer, forecasting model, user interface, or data persistence.

The final comment in `main.py` refers to calculating a mean, but no mean calculation is implemented. Results are printed to the console; the script does not save them to a file.

## Requirements

- Python 3
- pandas
- numpy
- yfinance
- openpyxl

## Run

1. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```
3. Run the script:
   ```sh
   python3 main.py
   ```

The script retrieves data from Yahoo Finance. Data availability and access therefore depend on that external service. The script was not run as part of this README update.

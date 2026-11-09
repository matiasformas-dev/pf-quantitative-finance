import pandas as pd
import numpy as np
import yfinance as yf

#descargar precios desde Yahoo Finance
tickers = ['IVV', 'ILF', 'SOXX'] #sp500, latam, semiconductores
vector_w = [0.5, 0.3, 0.2] # pesos de cada activo 
vector_w = np.array(vector_w).reshape(-1, 1) # convertir a array (vector) de numpy 
df_prices = yf.download(tickers, start='2024-01-01', end='2026-09-30')['Close'] #descargar precios finales diarios
print(df_prices)

#calcular retornos diarios
df_ret = df_prices.pct_change().dropna() #calcular retornos diarios
print(df_ret)

#calcular matriz varianza covarianza
df_cov = df_ret.cov() #calcular matriz varianza covarianza
print(df_cov)

# calcular varianza del portafolio
w = vector_w
w_t = w.T
sigma = df_cov.values

print(w, w.shape)
print(w_t, w_t.shape)
print(sigma, sigma.shape)

varianza = np.dot(sigma, w)
varianza = np.dot(w_t, varianza)[0][0]  

desv = varianza**(0.5)
volatilidad_anual = desv * (252**0.5) #volatilidad anualizada
print(volatilidad_anual)
print(f'la volatilidad anual del portafolio es: {volatilidad_anual*100:.04}%')

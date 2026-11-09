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

# calcular media del portafolio
vector_ret = df_ret.mean()
vector_ret = vector_ret.values
vector_ret = vector_ret.reshape(-1, 1)
mu = np.dot(w_t, vector_ret)[0][0]
mu_anual = mu * 252 #media anualizada
print(f'la media anual del portafolio es: {mu_anual*100:.04}%')

# calcular value at risk (VaR) del portafolio, 95% de confianza
var_95 = mu_anual - 1.64 * volatilidad_anual #VaR a 95% de confianza
print(f'la VaR anual del portafolio es: {var_95*100:.04}%')

# calcular value at risk (VaR) del portafolio, 99% de confianza
var_99 = mu_anual - 2.33 * volatilidad_anual #VaR a 99% de confianza
print(f'la VaR anual del portafolio es: {var_99*100:.04}%')
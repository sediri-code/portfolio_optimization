# -*- coding: utf-8 -*-
"""portfolio_optimization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lG6hDKA-5VmMA2DgtXkxw_1Y00Ig5fk3
"""

#import python libraries
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

#select the tickers
tickers=['IBM','GOOG','AMZN']
tickers

#selectionner la période

end_date=datetime.today()
end_date

start_date=end_date - timedelta(days=2*365)
start_date

#create a dataframe to store close prices
close_df=pd.DataFrame()

for ticker in tickers:
  data=yf.download(ticker,start=start_date,end=end_date)
  close_df[ticker]=data['Close']

#afficher les prix de cloture
close_df

from matplotlib import pyplot as plt
close_df['GOOG'].plot(kind='line', figsize=(8, 4), title='GOOG')
plt.gca().spines[['top', 'right']].set_visible(False)

#calculer les rendements
returns=close_df.pct_change()
returns

#calculer le rendement moyen et la variance de chaque titre
mean_returns=np.mean(returns,axis=0)
mean_returns

#presenter la matrice var-cov

cov_matrix=returns.cov()
cov_matrix

title='Portfolio Price History'
mes_actions=close_df

from matplotlib import pyplot as plt

# Assuming close_df is a DataFrame with columns 'GOOG', 'IBM', and 'AMZN'
close_df[['GOOG', 'IBM', 'AMZN']].plot(kind='line', figsize=(8, 4))
plt.title('Stock Prices Comparison')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend(['GOOG', 'IBM', 'AMZN'])
plt.gca().spines[['top', 'right']].set_visible(False)
plt.show()

#calculer les proportions
proportions=np.array([0.2,0.3,0.5])

#calculer la variance et l'écart type
portfolio_variance=np.dot(proportions.T, np.dot(cov_matrix,proportions))
portfolio_variance

portfolio_volatility=np.sqrt(portfolio_variance)
portfolio_volatility

#calculer le rendement annuel du portefeuille
portfolio_annual_return=np.sum(returns.mean()*proportions)*252
portfolio_annual_return

#afficher le rendement,la variance et la volatilité en %
percent_return=str(round(portfolio_annual_return,4)*100)+'%'
percent_variance=str(round(portfolio_variance,4)*100)+'%'
percent_volatility=str(round(portfolio_volatility,4)*100)+'%'
percent_annual_return=str(round(portfolio_annual_return,4)*100)+'%'

print('Le rendement moyen esperé du portefeuille est de:' + percent_return)
print('Le variance du portefeuille est de:' + percent_variance)
print('Le volatilté du portfeuille est de: ' + percent_volatility)
print('Le rendement annuel du portfeuil est de '+percent_annual_return)

pip install cvxpy #objectif minimiser la variance (G²P)

import cvxpy as cp

weights = cp.Variable(len(mean_return))
weights

objective=cp.Minimize(cp.quad_form(weights,cov_matrix)) #code pour minimiser la variance

constraints= [cp.sum(weights)==1]

problem=cp.Problem(objective,constraints)

problem.solve()

optimal_weights=weights.value
print("optimal weights:",optimal_weights)

pip install fredapi

from fredapi import Fred
fred=Fred(api_key="fd56964a425884ac8b6314219efc5f26")
rate=fred.get_series_latest_release('GS10')/100
rf=rate.iloc[-1]
rf

sharpe_ratio=(portfolio_annual_return)/portfolio_volatility
sharpe_ratio

num_portfolios = 10000

portfolio_returns = []
portfolio_volatilities= []

for _ in range(num_portfolios):
  weights = np.random.rand(len(tickers))
  weights /= np.sum(weights)
  portfolio_return = np.dot(mean_returns,weights)
  portfolio_volatility = np.sqrt(np.dot(weights.T , np.dot(cov_matrix,weights)))
  portfolio_returns.append(portfolio_return)
  portfolio_volatilities.append(portfolio_volatility)

#convertir les rendements en un tableau Numpy

portfolio_returns = np.array(portfolio_returns)
portfolio_volatilities=np.array(portfolio_volatilities)

plt.scatter(portfolio_volatilities, portfolio_returns, marker ='o',s=10, label='Random Portfolios')
plt.title('Efficient Frontier')
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Return')
plt.legend()
sharpe_ratios = portfolio_returns / portfolio_volatilities
max_sharpe_ratio_index = np.argmax(sharpe_ratios)
plt.scatter(portfolio_volatilities[max_sharpe_ratio_index],
            portfolio_returns[max_sharpe_ratio_index],
            marker ='X', color ='red', s=200,label='Max Sharpe Ratio')
plt.show()
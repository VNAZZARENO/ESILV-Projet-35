# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:08:37 2022

@author: vince
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### Figures parameter ###
my_dpi = 144


file_name = "merged-data-2018-01-02.csv"
file_path = r"C:/Users/vince/OneDrive/Bureau/ESILV/Pi²/data/" + file_name


df = pd.read_csv(file_path, sep=";")
df = df.dropna()
df['daily_returns'] = df.EURGBP_Mid.pct_change()


def GEV(y, u, beta, xi):
    """Generalized Extreme Value distribution
    - u is the location
    - beta is the scale
    - xi is the shape
    """
    if xi != 0:
        g = np.exp(- (1 + xi * ((y - u)/beta))**(-1/xi))
    else:
        g = np.exp(- (1 + xi * ((y - u)/beta)))
    return g

#the log-likelihood function is :
def loglik_f(y_i, u, beta, xi):
    n = len(y_i)
    s = 0
    for i in range(len(y_i)):
        s += np.log(1 + xi * (y_i - u)/beta)
    loglik = - n * np.log(beta) - (1/xi + 1) * s
    return loglik


def beta_MLE(k, n, y_i, u, beta, xi):
    ext = y_i[k:k+n]
    s = 0
    for i in range(0, n):
        s+= (ext[i] - u)/(beta + xi * (ext[i] - u))
    beta_mle = 1/n * s - 1/(1 + xi)
    return beta_mle
 
    
def find_value(L):
    S = sorted(L)
    for i in range(1, len(S)):
        if S[i] * S[i-1] < 0:
            return i
            exit
    return min(S[i])


def Xi_Hill(k, n, y_i, u):
    s = 0
    ext = y_i[k:k+n]
    for i in range(2, n+2):
        s+= (np.log(abs(ext[n - i + 1])) - np.log(abs(u))) 
    return s/n
    

def Xi_Pickands(k, n, y_i, u):
    T = len(y_i)
    xi_pick = 1/np.log(2) * np.log(abs((y_i[T - n + 1]) - abs(y_i[T - 2*n +1]))
                                   /abs((y_i[T - 2*n + 1]) - abs(y_i[T - 4*n + 1])))
    return xi_pick


data = sorted(df.daily_returns.dropna().tolist())
reversed_data = data[::-1]
nb = len(data)
alpha = 0.1
k = int(nb * (1 - alpha))
u_upper = data[k]
u_lower = reversed_data[k]
n = nb - k

xi_pick_l = []
xi_hill_l = []
quantiles = np.linspace(0.9, 0.999, 1000)
for q in quantiles:
    try:
        data = sorted(df.daily_returns.dropna().tolist())
        reversed_data = data[::-1]
        nb = len(data)
        k = int(nb * q)
        u_upper = data[k]
        u_lower = reversed_data[k]
        n = nb - k
        
        xi_hill_l.append(Xi_Hill(k=k, n=n, y_i=data, u=u_upper))
        xi_pick_l.append(Xi_Pickands(k=k, n=n, y_i=data, u=u_upper))
    except IndexError:
        pass

plt.figure(1, figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
plt.plot(quantiles[:len(xi_hill_l)], xi_hill_l, label="Xi_Hill")
plt.plot(quantiles[:len(xi_pick_l)], xi_pick_l, label="Xi_Pickands")
plt.title('Pickands and Hill Estimator for Xi')
plt.legend()
plt.show()
        
xi_Hill_upper = sum(xi_hill_l)/len(xi_hill_l)
# xi_Hill < 0.5 so this is a fat tail density law 
# following a Weibull density function


beta = np.linspace(0.0001, 0.1, 1000000)
beta_mle = beta_MLE(k=k, n=n, y_i=data, u=u_upper, beta=beta, xi=xi_Hill_upper)
#### FIND 0 in BETA_MLE GIVES : ####
zero_beta_mle = 0.43

#Beta_MLE graph to find the x_0 such that MLE(x_0) = 0
# with the help of find_zero(L, beta)
plt.figure(2, figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
plt.plot(beta, beta_mle, label = "Beta_MLE = ")
plt.plot()
plt.title('BETA_0 such that MLE(BETA_0) = 0')
plt.grid()
plt.legend()


#GEV graph with parameters
plt.figure(3, figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
y = np.linspace(-1, 3, 1000)
g = GEV(y=y, u=u_upper, beta=zero_beta_mle, xi=xi_Hill_upper)
plt.plot(y, g, label="GEV(y)")
plt.title('Cumulative Distribution Function')
plt.xlabel('y')
plt.ylabel('GEV(y)')
plt.legend()

#PDF of the GEV CDF 
def Differential(function):
    d = []
    for i in range(1, len(function)):
        d.append(function[i] - function[i-1])
    return d

plt.figure(4, figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
plt.plot(y[1:], Differential(g), label="GEV'(y)")
plt.xlabel('y')
plt.ylabel('gev(y)')
plt.title('Probability Density Function (gev(y)) of GEV(y)')
plt.legend()
plt.show()        

alpha_q = 0.01
GEV(y=alpha_q, u=u_upper, beta=zero_beta_mle, xi=xi_Hill_upper)







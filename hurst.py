# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:03:24 2022

@author: vince
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


###### DATA IMPORTATION AND PREPARATION
print("#"*40)

# git_url = "https://raw.githubusercontent.com/VNAZZARENO/ESILV-Projet-35/main/EURGBP_2018-01-02.csv"
file_path = r"C:\Users\vince\OneDrive\Bureau\ESILV\Pi²\data" + r"\merged-data-2018-01-02.csv" 

df_raw = pd.read_csv(file_path,sep=";",header=0)
df_raw.rename(columns=lambda x: x.upper(), inplace=True)
df_raw.rename(columns={'UNNAMED: 0':'TIMESTAMP'}, inplace=True)


fx = ['EURGBP', 'EURJPY', 'EURUSD']
df = {}
for m in fx:
    df[m] = df_raw[['TIMESTAMP', f'{m}_MID', f'{m}_MID_EMA_10MIN_RET']]

for key in df.keys():
    # df[key]['AVERAGE'] = ""
    # df[key]['AVERAGE'] = (df[key]['HIGH'] + df[key]['LOW'])/2
    df[key] = df[key].dropna()
    df[key]['PCT_CHANGE'] = np.nan
    df[key]['PCT_CHANGE'] = df[key][f'{key}_MID'].pct_change()
    df[key]['PCT_CHANGE'] = df[key][f"{key}_MID"].fillna(value = 0)
    


#### a)

###### HAAR WAVELETS ######
        #WAVELET#
def HaarMotherWavelet(x):
    if (x >= 0) and (x < 1/2):
        return 1
    elif (x >= 1/2) and (x < 1):
        return -1
    else:
        return 0


#SCALING/Father FUNCTION
def HaarFatherWavelet(x):
    if (x >= 0) and (x <= 1):
        return 1
    else:
        return 0
    
    
def HaarWaveletFunctions(x, j, k):
    return (2**(j/2)) * HaarMotherWavelet((2**j)*x -k)


def plotHaarFunctions(x, j, k):
    y = []
    for v in x:
        y.append(HaarWaveletFunctions(j, k, v))
    str_label = "Wavelet transform, j="+str(j)+" k="+str(k)
    plt.plot(y, label = str_label, c = "r")
    plt.legend()
    plt.title('HAAR WAVELET')
    plt.grid()
    plt.show()
    
plotHaarFunctions(np.linspace(-5, 5, 10000), 2, -1)

### DWT ###
def haarFWT (signal, level):
    s = 0.5  # scaling -- try 1 or ( .5 ** .5 )

    h = [1,  1] # lowpass filter, haar father wavelet
    g = [1, -1] # highpass filter haar mother wavelet
    f = len(h)  # length of the filter

    t = signal  # 'workspace' array
    l = len(t)  # length of the current signal
    y = [0]*l   # initialise output

    t = t + [0, 0]  # padding for the workspace
    for i in range (level):
        y[0:l] = [0]*l   # initialise the next level 
        l2 = l//2        # half approximation, half detail
        for j in range(l2):            
            for k in range(f):                
                y[j] += t[2*j + k] * h[k]*s
                y[j+l2] += t[2*j + k] * g[k] * s

        l = l2   # continue with the approximation
        t[0:l] = y[0:l] 
    return y


def getDWT(df, row, window):
    dwt = {}
    for pair in tqdm(df.keys()):
        y = {}
        for level in range(1, 14):
            y['level'+str(level)] = haarFWT(df[pair]['PCT_CHANGE'][row:row+window].tolist(), level)
        dwt[pair] = y
    return dwt

### COVARIANCE ###   
def Covariance(c1, c2):
    assert len(c1) == len(c2)
    T = len(c1)
    s = 0
    for k in range(1, T):
        s_c1_inner = 0
        s_c2_inner = 0
        for i in range(1, T):
            s_c1_inner += c1[i]
            s_c1_inner *= 1/T
            s_c2_inner += c2[i]
            s_c2_inner *= 1/T
        s += (c1[k] - s_c1_inner)*(c2[k] - s_c2_inner)/(np.std(c1) * np.std(c2))
    s *= 1/T
    return s


def getCovMatrix(dwt, max_j):
    cov_matrix = {}
    for j in tqdm(range(1, max_j)):
        cov_matrix_j = np.zeros((3,3))
        for pair_r in dwt.keys():
            r = list(dwt.keys()).index(pair_r)
            for pair_c in dwt.keys():
                c = list(dwt.keys()).index(pair_c)
                cov_matrix_j[r,c] = Covariance(dwt[pair_r]['level'+str(j)], dwt[pair_c]['level'+str(j)])
        cov_matrix['cov_matrix_'+str(j)] = cov_matrix_j
    return cov_matrix
 
    
def getCoeffJ(dwt, max_j, my_dpi):
    cov_matrix = getCovMatrix(dwt, max_j)
    correlation_assets = {}

    x = []
    for j in range(1, max_j):
        x.append(cov_matrix['cov_matrix_'+str(j)][0,1])
    correlation_assets['EURGBP EURJPY'] = x
    
    x = []
    for j in range(1, max_j):
        x.append(cov_matrix['cov_matrix_'+str(j)][0,2])  
    correlation_assets['EURGBP EURUSD'] = x
    
    x = []
    for j in range(1, max_j):
        x.append(cov_matrix['cov_matrix_'+str(j)][1,2])
    correlation_assets['EURJPY EURUSD'] = x
    
    
    xlab = ['T2', '2-4', '4-8', '8-16', '16-32', '32-64', '64-128', '128-256', '256-512', '512-1024', '1024-2048', '2048-4096']
    for key in correlation_assets.keys():
        plt.figure(figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
        plt.plot(xlab, correlation_assets[key], label="Correlation "+str(key))
        plt.xlabel('Time Scale')
        plt.ylabel("Wavelet Correlation")
        plt.legend()
        plt.title(key)
        plt.grid()
        plt.savefig("correlation_"+key+'.png')
        plt.show()
    return correlation_assets

### b)

def EmpiricalAbsoluteMoments(X, n, k):
    m = 0
    T = len(X)
    for i in range(1, len(X)//n):
        m+= np.abs(X[n*i] - X[n*(i-1)])**k
    return n*m/T


def Increments(X, n):
    L = []
    for i in range(n, len(X)):
        if X[i-n] != 0:
            L.append(np.log(X[i]/X[i-n]))
        else:
            L.append(0)
    return L


def getIncrements(df, time_scale):
    increments = {}
    for key_pair in df.keys():
        increment_pair = {}
        for key, value in time_scale.items():
            increment_pair[key] = Increments(df[key_pair][f'{key_pair}_MID'].tolist(), value)
        increments[key_pair] = increment_pair
    return increments


def getMoments(df, increments, time_scale, row, window):
    moments = {}
    k_var = 2 # moments of order 2 == variance
    for key_pair in df.keys():
        moment_pair = {}
        for key, value in time_scale.items():
            moment_pair[key] = [EmpiricalAbsoluteMoments(increments[key_pair][key][i*row:i*row+window], value, k_var) 
                                for i in range(df[key_pair].shape[0] - window)]
        moments[key_pair] = moment_pair
    return moments


def HurstExponent(m2, m2bis, k):
    res = np.log2(m2bis/m2)/k
    if res < 0:
        return 0
    if res > 1:
        return 1
    else:
        return res


def getHurstExponent(moments, time_scale_hurst, time_scale):
    H = {}
    time_scale_values = list(time_scale.values())
    time_scale_hurst_list = list(time_scale_hurst.keys())
    time_scale_hurst_values = list(time_scale_hurst.values())
    for key in moments.keys():
        H_pair = {}
        for scale_i in range(0, len(moments[key]) - 1):
            res = pd.Series([HurstExponent(m2=moments[key][time_scale_hurst_list[scale_i]][i], 
                                           m2bis=moments[key][time_scale_hurst_list[scale_i+1]][i], 
                                           k=time_scale_hurst_values[scale_i+1]) 
                             for i in range(len(moments[key][time_scale_hurst_list[scale_i]]))]).rolling(window=time_scale_values[scale_i+1]).mean()
            res = res.dropna(axis=0)
            res = res.reset_index(drop=True)
            H_pair[time_scale_hurst_list[scale_i]+'_'+time_scale_hurst_list[scale_i+1]] = res.tolist()
        H[key] = H_pair  
    return H


def plotH(H, my_dpi):
    for key in H.keys():
        for scale in H[key].keys():
            plt.figure(figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
            n = len(H[key][scale])
            plt.plot(H[key][scale], label="H : "+key+" at "+scale)
            plt.plot(pd.Series(H[key][scale]).rolling(960).mean(), c = 'indigo', label = "Moving average of H")
            plt.plot([0,n], [0.5, 0.5], c = 'r', label="Optimal market efficiency when H = 0.5")
            plt.legend()
            plt.grid()
            plt.title('Hurst exponent of '+key+ " at "+ scale)
            plt.xlabel("increment i")
            plt.ylabel("value of H")
            # plt.savefig(key+"_"+scale+".png")
            plt.show()
 

#### Figure Parameters ####
my_dpi = 144    

#### PLOTTING OF THE MULTIRESOLUTION CORRELATION
dwt = getDWT(df, 1, 8192) #discret wavelet transform
plt.plot(dwt['EURGBP']['level1'], label="Discret Wavelet Transform at level 1")

max_j = 13
correlation_assets = getCoeffJ(dwt, max_j, my_dpi)
 
time_scale = {'15min':1, '30min':2, '60min':4, '120min':8, '360min':24} # number of 15min tranches per key
time_scale_hurst = {'15min':1, '30min':2, '60min':2, '120min':2, '360min':3} # the value is the corresponding multiplication

increments = getIncrements(df, time_scale)            
moments = getMoments(df, increments, time_scale, 1, 96)
H = getHurstExponent(moments, time_scale_hurst, time_scale)
plotH(H, my_dpi)


def getSigmas(increments, H, pair=""):
    sigma_daily_dict = {}
    sigma_yearly_dict = {}
    for key_pair in increments.keys():
        # key_pair = pair #choose which one is computed
        sigma_daily = {}
        temp = {'15min':96, '30min':48, '60min':24, '120min':12, '360min':4}
        for key_i in increments[key_pair].keys():
            sigma_daily[key_i] = pd.Series(increments[key_pair][key_i]).rolling(window = temp[key_i]).std()

        sigma_daily_dict[key_pair] = sigma_daily
    for key in H.keys():
        # key = pair #choose which one is computed
        sigma_temp = {}
        for scale in H[key].keys():
            sigma_yearly_list = []
            for i in range(0, len(H[key][scale])):
                sigma_y_i = 252**H[key][scale][i] * sigma_daily_dict[key][scale.split('_')[0]][i]
                sigma_yearly_list.append(sigma_y_i)   
            sigma_temp[scale.split('_')[0]] = pd.Series(sigma_yearly_list)
        sigma_yearly_dict[key] = sigma_temp
        
    return (sigma_daily_dict, sigma_yearly_dict)
            
    
def plotSigma(sigma, my_dpi, save):
    type_s = ['daily volatily', 'annualized volatility']
    col = {'15min':'mediumseagreen', '30min':'lightskyblue','60min':'slateblue', '120min':'coral', '360min':'maroon'}
    for s in range(len(sigma)):
        for key in sigma[s].keys():
            for scale in sigma[s][key]:
                plt.figure(figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
                plt.plot(sigma[s][key][scale], label=key+" "+scale+" "+type_s[s], c = col[scale])
                plt.legend()
                plt.grid()
                if save == True: plt.savefig(key+"_"+scale+"_"+type_s[s]+".png")
                plt.show()
  
    
sigmas = getSigmas(increments, H)
plotSigma(sigmas, my_dpi, save = False)
 
type_s = ['daily volatily', 'annualized volatility']  
for s in range(len(sigmas)):
    plt.figure(figsize=(1200/my_dpi, 700/my_dpi), dpi=my_dpi)
    for key in sigmas[s].keys():
        temp = []
        for scale in sigmas[s][key]:
            temp.append(np.mean(sigmas[s][key][scale]))
        
        plt.plot(list(sigmas[s][key].keys()), temp, label = 'mean of ' + type_s[s]+" of "+key)
        plt.legend()
        plt.grid()
    # plt.savefig("mean_"+type_s[s]+".png")
    plt.show()

    
    
    
    
    
    
    




# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:04:11 2023

@author: vince
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import mplfinance as mpf

import os

global df
global df_selection
global folder_selected
global date_selected
global symbol_selected

global df_entire_selection
global df_merged
global mat_cov

df_entire_selection = {}
df_merge = pd.DataFrame()

folder_selected = ""
    
def get_data(path):
    global df
    global df_entire_selection

    try:
        df_raw = pd.read_csv(path,sep=",",header=1,names=['Exness', 'Symbol', 'Timestamp', 'Bid', 'Ask'])
    except FileNotFoundError:
        print('No such file in the direction with inputed parameters')
    
    try: 
        df_raw['Mid'] = (df_raw['Ask'] + df_raw['Bid'])/2
        df_raw = df_raw.drop(['Ask', 'Bid'], axis=1)
        df = clean_df(df_raw)
        print(f"\nSuccessful data preparation.\nDimensions of prepared data : {df.shape[0]} rows and {df.shape[1]} columns")
        print(f"Column names : {df.columns.tolist()}") 
        
        df_entire_selection[symbol_selected+"_"+date_selected] = df
    except UnboundLocalError:
        print("Cannot load the file")
    

def clean_df(df):
    
    symbol = df['Symbol'][0]
    plateform = df['Exness'][0]
    sampled_day_100ms = pd.Series(pd.date_range(start=pd.to_datetime(min(df['Timestamp']), format='%Y-%m-%d %H:%M:%S.%f').date(), 
                               end=pd.to_datetime(max(df['Timestamp']), format='%Y-%m-%d %H:%M:%S.%f').date() + datetime.timedelta(days=1),
                               freq="100L"))
    sampled_day_100ms.drop(index=sampled_day_100ms.index[-1],axis=0,inplace=True)
    source_day_100ms = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f').dt.round('100ms')
    df_sampled = df.set_index(source_day_100ms)    
    df_true = pd.DataFrame(index = sampled_day_100ms)
    df_final = pd.DataFrame.from_dict(df_true)
    df_final = df_final.append(pd.DataFrame.from_dict(df_sampled))    
    df_final = df_final.groupby(level=0).mean()
    df_final.replace(0, np.nan, inplace=True)
    df_final['Exness'] = plateform   
    df_final['Symbol'] = symbol    
    
    return df_final


def folder_selection():
    
    # global df
    global folder_selected
    global symbol_selected
    global date_selected
    
    if folder_selected == "":
        #open a foler to retrieve the content and path
        folder_selected = filedialog.askdirectory()  
        combo_selection("<<ButtonClick>>")
        
    file_path = folder_selected + '/' + symbol_selected + '/' + date_selected[:4] + '/' + symbol_selected + '_' + date_selected + '.csv'
    messagebox.showinfo("File Path", f"You selected: {file_path}")
    get_data(file_path)


def combo_selection(event):
    global date_selected
    global symbol_selected
    
    # Obtenir l'élément sélectionné
    date_selected = combo_date.get()
    symbol_selected = combo_symbol.get()
    file_path = folder_selected + '/' + symbol_selected.upper() + '/' + date_selected[:4] + '/' + symbol_selected + '_' + date_selected + '.csv'
    print(f"Date : {date_selected}\nSymbol : {symbol_selected}\nResulting file : {file_path}\n")
  
    
def Merge_Symbol():
    global df_entire_selection
    global df_merged
    global date_selected
    global symbol_selected
    
    try:
        df_merged = pd.DataFrame(index=df_entire_selection[symbol_selected+"_"+date_selected].index)
        for key in df_entire_selection.keys():
            for value in ['Mid']:
                print(f"key : {key}, value : {value}")
                df_merged[key[:6]+"_"+value] = np.nan
                df_merged[key[:6]+"_"+value] = df_entire_selection[key][value]
                
        print('\nSuccessfully merged all symbols !\n')
    except NameError:
        pass
        
def Plot():
    global df_merged
    from datetime import datetime
    try:
        for key in df_merged.keys():   
            plt.plot(df_merged.index, df_merged[key])
            plt.xlabel('Date')
            plt.ylabel(key)
            plt.title(f'{key} plot')
            
            # set x-axis tick marks to show every 15 minutes
            plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
            
            # format x-axis labels as 'hour:minute'
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            
            # rotate x-axis tick labels by 45 degrees
            plt.gca().xaxis.set_tick_params(rotation=45)
            
            # set x-axis limits to start at 0:00 and end at 23:59
            plt.gca().set_xlim([mdates.date2num(df_merged.index[0].replace(hour=0, minute=0)),
                     mdates.date2num(df_merged.index[-1].replace(hour=23, minute=59))])
            plt.show()
    except NameError:
        print('Try importing data first\n')
        
        
def ema():
    """
    Compute the different analytics 

    """
    global df_merged
    try:
        ema_1min = df_merged.ewm(span=60, adjust=False, ignore_na=True).mean()
        ema_3min = df_merged.ewm(span=180, adjust=False, ignore_na=True).mean()
        ema_10min = df_merged.ewm(span=600, adjust=False, ignore_na=True).mean()
        list_column_money = df_merged.columns
        for col in list_column_money:
            if col != "Timestamp":
                df_merged[f"{col}_EMA_1min"] = (df_merged[col] / ema_1min[col])*10000
                df_merged[f"{col}_EMA_3min"] = (df_merged[col] / ema_3min[col])*10000
                df_merged[f"{col}_EMA_10min"] = (df_merged[col] / ema_10min[col])*10000
        for col in list_column_money:
            if col != "Timestamp":  
                df_merged[f"{col}_EMA_1min_ret"] = 0
                df_merged[f"{col}_EMA_1min_ret"] = (df_merged[col]/df_merged[f"{col}_EMA_1min"] - 1 ) * 10000
                df_merged[f"{col}_EMA_3min_ret"] = 0
                df_merged[f"{col}_EMA_3min_ret"] = (df_merged[col]/df_merged[f"{col}_EMA_3min"] - 1 ) * 10000
                df_merged[f"{col}_EMA_10min_ret"] = 0
                df_merged[f"{col}_EMA_10min_ret"] = (df_merged[col]/df_merged[f"{col}_EMA_10min"] - 1 ) * 10000

        print('Successfully computed the metrics')
    except NameError:
        print('Merge de Data first')
        


def mat_cov_compute():
    global df_merged
    global mat_cov
    global mat_corr
    mat_cov = df_merged.cov()
    mat_corr = df_merged.corr()
    print(mat_cov)
    print(mat_corr)
    
    f_cov = plt.figure(figsize=(19, 15))
    plt.matshow(mat_cov, fignum=f_cov.number)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title('Covariance Matrix', fontsize=16);
    plt.show()
    
    f_corr = plt.figure(figsize=(19, 15))
    plt.matshow(mat_corr, fignum=f_corr.number)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title('Correlation Matrix', fontsize=16);
    plt.show()


def export_data():
    global df_merged
    global folder_selected
    global date_selected
    global mat_cov
    global mat_corr
    
    try:
        file_path_export_merged = folder_selected + r"/merged-data-" + date_selected + ".csv"
        df_merged.to_csv(file_path_export_merged, sep=";", index=True)
        file_path_export_cov = folder_selected + r"/cov-" + date_selected + ".csv"
        mat_cov.to_csv(file_path_export_cov, sep=";", index=True)
        file_path_export_corr = folder_selected + r"/corr-" + date_selected + ".csv"
        mat_corr.to_csv(file_path_export_corr, sep=";", index=True)
        
        print(f'\nSuccessfully exported merged data, covariance and correlation to {folder_selected}\n')
    except NameError:
        print("Cannot export data, import data first\n")


root = tk.Tk()
root.title("Input, File, and Date Range Retrieval")
root.geometry("250x250")
liste_dates = pd.date_range("2018-01-01", "2018-12-28", freq = '1D').date.tolist()
liste_symbols = ['EURGBP', 'EurUSD', 'EURJPY']

combo_date = ttk.Combobox(root, values=liste_dates)
combo_date.current(1)
combo_date.bind("<<ComboboxSelected>>", combo_selection)

combo_symbol = ttk.Combobox(root, values=liste_symbols)
combo_symbol.current(0)
combo_symbol.bind("<<ComboboxSelected>>", combo_selection)

file_button = tk.Button(root, text="Import Data", command=folder_selection)
quit_button = tk.Button(root, text="Quit application", command=root.destroy)
merge_button = tk.Button(root, text = "Merge", command=Merge_Symbol)
ema_button = tk.Button(root, text="Compute Metrics", command=ema)

plot_button = tk.Button(root, text="Plot data", command=Plot)
cov_button = tk.Button(root, text="Covariance matrice", command=mat_cov_compute)

export_button = tk.Button(root, text="Export Merged Data", command=export_data)
start_date_combo = Combobox(root, values = ['start'])
end_date_combo = Combobox(root, values = ['end'])

#Packing of the widgets
combo_date.pack()
combo_symbol.pack()

file_button.pack()
merge_button.pack()
ema_button.pack()
plot_button.pack()
cov_button.pack()
export_button.pack() 
quit_button.pack()

#RUN APPLICATION
root.mainloop()
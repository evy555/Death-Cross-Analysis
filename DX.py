import pandas as pd 
import pandas.io.data 
from pandas import Series, DataFrame
import datetime
from pandas import ExcelWriter 
import os 
import matplotlib.pyplot as plt 
import math
import numpy as np 
from numpy import *
now = datetime.datetime.now()
Start_Date = input("What is the start year? ")
End_Date = input("What is the end year? ")

start_of_interval = datetime.datetime(int(Start_Date), now.month, now.day)
end_of_interval = datetime.datetime(int(End_Date), now.month, now.day)       
df = pd.io.data.get_data_yahoo("^GSPC", start = start_of_interval, end = end_of_interval, interval = "d")['Adj Close']

df = DataFrame(df) 
df['Returns'] = df.pct_change()
df['Average_200'] = pd.rolling_mean(df['Adj Close'],200)
df['Average_50'] = pd.rolling_mean(df['Adj Close'],50) 
df['Date'] = df.index 

df['Average_Diff'] = df['Average_50'] - df['Average_200']  
df['Average_Diff'] = df['Average_Diff'].fillna(0) 

l = df.index.values 
for i in range(1, len(l)):
    if df.loc[l[i], 'Average_Diff']== int(0):
        df.loc[l[i], "Signal"] = "Hold"
        df.loc[l[i], "Market"] = 1
    elif df.loc[l[i-1], 'Average_Diff']> 0 and df.loc[l[i], 'Average_Diff'] < 0:
        df.loc[l[i], "Signal"] = "Sell"
        df.loc[l[i], "Market"] = 1 
        df.loc[l[i+1], 'Market'] = 0
    elif df.loc[l[i-1],'Average_Diff'] < 0 and df.loc[l[i], 'Average_Diff'] > 0:
        df.loc[l[i],"Signal"] = "Buy"
        df.loc[l[i+1],"Market"] = 1 
        if df.loc[l[i-1], "Market"] == 0:
            df.loc[l[i], "Market"] = 0 
        else:
            df.loc[l[i], "Market"] = 1 
    else:
        df.loc[l[i], "Signal"] = "Hold" 
        if df.loc[l[i-1], "Signal"] == "Buy":
            df.loc[l[i], "Market"] = df.loc[l[i], "Market"] 
        elif df.loc[l[i-1], "Signal"] == "Sell":
            df.loc[l[i], "Market"] = df.loc[l[i], "Market"]
        else:
            df.loc[l[i], "Market"] = df.loc[l[i-1], "Market"]
df['Investment'] = ""
df['S&P500 Investment'] = ''
df['Investment'][0] = 10000
df['S&P500 Investment'][0] = 10000 

for i in range(1,len(l)):
    df.loc[l[i], 'S&P500 Investment'] = df.loc[l[i-1], 'S&P500 Investment'] * (1 + df.loc[l[i], 'Returns']) 
    if df.loc[l[i-1], "Signal"] == "Buy":
        df.loc[l[i], 'Investment'] = df.loc[l[i-1], 'Investment'] 
    elif df.loc[l[i-1], "Signal"] == "Sell" and df.loc[l[i-1], "Market"] == 1:
        df.loc[l[i], 'Investment'] = df.loc[l[i-1], 'Investment'] * (1 + df.loc[l[i], "Returns"])  
    elif df.loc[l[i], "Signal"] == "Hold":
        df.loc[l[i], 'Investment'] = df.loc[l[i-1], 'Investment'] * (1 + df.loc[l[i], "Returns"]) 
    else:
        df.loc[l[i], 'Investment'] = df.loc[l[i-1], 'Investment']  
        
for i in range(1,len(l)):
    df.loc[l[i], "Total Return"] = (df.loc[l[i], "Investment"] / df['Investment'][0]) - 1 
    df.loc[l[i], "S&P Return"] = (df.loc[l[i], "S&P500 Investment"] / df['S&P500 Investment'][0]) - 1 

#df['5YearReturn'] = ""

#for i in range(0, len(l)):
#    df.loc[l[i], '5YearReturn'] = df.cumsum(df.loc[l[i], "Returns"]:df.loc[l[i+1824], "Returns"])
    

file = ExcelWriter('DX.xlsx')
df.to_excel(file, "Data") 
file.close() 
os.startfile('DX.xlsx') 

df.plot(y = ['Adj Close', 'Average_200', 'Average_50'])
df.plot(y = ['Investment', 'S&P500 Investment'])
plt.show() 
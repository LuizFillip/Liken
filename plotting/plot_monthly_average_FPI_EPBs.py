import pandas as pd
import matplotlib.pyplot as plt
from FabryPerot.utils import time2float
import numpy as np
import setup as s
from build import paths as p

def load_FPI(n):
    files = p("FabryPerot").get_files_in_dir("avg")
    infile = [f for f in files if "zon" in f][0]
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.columns = pd.to_datetime(df.columns)
    
    return df.loc[:, df.columns.month == n]


def load_EPB(n, lat = -5):
    infile = "EPBs_DRIFT.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    if lat is None:
        df = df.loc[(df.index.month == n)]
    else:
        df = df.loc[(df.index.month == n) &
                (df["lat"] == lat)]
    
    df["time"] = time2float(df.index.time, sum24 = True)

    return pd.pivot_table(df, 
                         columns = df.index.date, 
                         index = "time", 
                         values = "vel")
    
def load_HWM(n):
    infile = "database/HWM/car_250_2013.txt"

    df = pd.read_csv(infile, index_col = "time")
    df.index = pd.to_datetime(df.index)
    
    df = df.loc[(df.index.month == n)]
    
    df["time2"] = time2float(df.index.time, sum24 = True)
    
    return pd.pivot_table(df, 
                         columns = df.index.date, 
                         index = "time2", 
                         values = "zon")




def plot_monthly_averages():
    
    fig, ax = plt.subplots(figsize = (12, 10), 
                           nrows = 3, 
                           ncols = 2, 
                           sharey = True, 
                           sharex = True)
    s.config_labels()
    
    months = [1, 2, 3, 10, 11, 12]
    
    plt.subplots_adjust(wspace = 0.05)
    
    for m, ax in zip(months, ax.flatten("F")):
    
        EPB = load_EPB(m, lat = None)
        FPI = load_FPI(m)
        HWM = load_HWM(m)
        
        FPI = FPI.reindex(np.arange(21, 30, 0.5), 
                          method = "nearest")
        
        dn = EPB.columns[0].strftime("%B")
                
        ax.set(title = dn, 
               xticks = np.arange(21, 30, 1),
               xlim = [21, 30], 
               ylim = [0, 200])
        
        ax.plot(EPB.mean(axis = 1),
                marker = "o",
                markersize = 3, 
                color = "r", 
                linestyle = "none", 
                label = "EPBs")
        
        ax.plot(HWM.mean(axis = 1),
                color = "blue",
                lw = 2,
                label = "HWM-14")
        
        ax.errorbar(FPI.index, 
                    FPI.mean(axis = 1), 
                    yerr = FPI.std(axis = 1),
                    color = "k", 
                    marker = "s", 
                    markersize = 3,
                    capsize = 3, 
                    label = "FPI")
        
    ax.legend()
        
    fontsize = 20
    
    fig.text(0.04, 0.35, "Velocidade zonal (m/s)",
             rotation = "vertical", 
             fontsize = fontsize)
    
    fig.text(0.4, 0.08, "Hora universal (UT)", 
             rotation = "horizontal", 
             fontsize = fontsize)
    
    fig.suptitle("M??dia hor??ria mensal - 2013", 
                 fontsize = fontsize, 
                 y = 0.95)
plot_monthly_averages()
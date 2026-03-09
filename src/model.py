import statistics
import numpy as np
import pandas as pd


def stats_model_by_season(df, tower):

    subset = df[df["site_mapped"] == tower].copy()
    subset["month"] = subset["datetime"].dt.month
    
    stds = []

    for cell, cell_df in subset.groupby("cell_mapped"):
        feature= "dl_avg_active_ues"
        
        monthly_avg = cell_df.groupby("month")[feature].mean()  # mean per month
        monthly_std_across_months = monthly_avg.std()            # std across months
        
        stds.append(monthly_std_across_months)
        print("Std across months:", monthly_std_across_months)

    avg_std_across_cells = sum(stds) / len(stds) if stds else 0
    print("Average std across cells:", statistics.median(stds))






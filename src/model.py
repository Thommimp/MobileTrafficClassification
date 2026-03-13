import statistics
import pandas as pd

def stats_model_by_season(df, tower):

    subset = df[df["site_mapped"] == tower].copy()
    subset["month"] = subset["datetime"].dt.month

    summer_months = [6, 7, 8]
    diffs = []

    for cell, cell_df in subset.groupby("cell_mapped"):
        feature = "nr_dl_avg_active_ues"

        monthly_avg = cell_df.groupby("month")[feature].mean()
        
        summer_avg = monthly_avg[monthly_avg.index.isin(summer_months)].mean()
        
        other_avg = monthly_avg[~monthly_avg.index.isin(summer_months)].mean()
        
        diff = summer_avg - other_avg

        if pd.notna(diff):
            diffs.append(diff)
            print(f"{cell} difference in summer vs other months:", diff)



    







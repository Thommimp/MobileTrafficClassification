import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA

def plot_feature_on_time(df, tower, cell, feature):
    subset = df[(df["site_mapped"] == tower) & (df["cell_mapped"] == cell)].copy()
    
    x = subset["datetime"]
    y = subset[feature]

    plt.plot(x, y, label=f"{tower} - {cell}")
    plt.xlabel("Time")
    plt.ylabel(feature)
    plt.title(f"Cell Data for {tower} - {cell}")
    plt.legend()

    # format x-axis to show months
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    plt.show()


def plot_two_cells(df, tower1, cell1, tower2, cell2, feature):
    subset1 = df[(df["site_mapped"] == tower1) & (df["cell_mapped"] == cell1)].copy()
    
    subset2 = df[(df["site_mapped"] == tower2) & (df["cell_mapped"] == cell2)].copy()
    
    plt.plot(subset1["datetime"], subset1[feature], label=f"{tower1} - {cell1}", color="blue")
    plt.plot(subset2["datetime"], subset2[feature], label=f"{tower2} - {cell2}", color="red")

    plt.xlabel("Time")
    plt.ylabel(feature)
    plt.title(f"Comparison of {feature} for two cells")
    plt.legend()

    # format x-axis to show months
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    plt.show()

def average_feature_across_tower(df, tower, feature):
    subset = df[df["site_mapped"] == tower].copy()
    
    pivot = subset.pivot_table(
            index = "datetime",
            columns = "cell_mapped",
            values = feature,
            aggfunc = "mean"
            )
    y = pivot.mean(axis=1, skipna=True)
    x = pivot.index
    
    plt.plot(x, y, label=f"{tower}")
    plt.xlabel("Time")
    plt.ylabel(feature)
    plt.title(f"Cell Data for {tower}")
    plt.legend()

    # format x-axis to show months
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    plt.show()

def plot_heat_map(df):
    # columns we dont want to normalize
    drop_cols = ["site_mapped", "cell_mapped", "datetime"]

    # drop columns
    df_feats = df.drop(columns=drop_cols)
    # correlation matrix
    corr = df_feats.corr()
        
    # visualize
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.show()


def box_plot_STD(df, feature, freq="W"):
    agg = (
        df.set_index("datetime")
        .groupby("site_mapped")[feature]
        .resample(freq)
        .mean()
        .reset_index()
    )

    std = agg.groupby("site_mapped")[feature].std().reset_index()

    plt.bar(std["site_mapped"], std[feature])
    plt.ylabel(f"Std of {freq} averages")
    plt.title(f"Variation of {feature} per site ({freq})")
    plt.show()

def box_plot_summer_vs_other(df, feature, freq = "ME"):
    summer_months = [6, 7, 8]

    monthly_avg = (
        df.set_index("datetime")
        .groupby("site_mapped")[feature]
        .resample(freq)
        .mean()
        .reset_index()
    )

    monthly_avg["season"] = monthly_avg["datetime"].dt.month.isin(summer_months)
    monthly_avg["season"] = monthly_avg["season"].map({True: "Summer", False: "Other"})

    # boxplot
    sns.boxplot(data=monthly_avg, x="site_mapped", y=feature, hue="season")
    plt.title(f"{feature}: Summer vs Other months per site")
    plt.show()


def box_plot_weekday_vs_weekend(df, feature):

    daily_avg = (
        df.set_index("datetime")
        .groupby("site_mapped")[feature]
        .resample("D")
        .mean()
        .reset_index()
    )

    # create weekday/weekend column
    daily_avg["day_type"] = daily_avg["datetime"].dt.weekday > 4
    daily_avg["day_type"] = daily_avg["day_type"].map({True: "Weekend", False: "Weekday"})

    # boxplot
    sns.boxplot(data=daily_avg, x="site_mapped", y=feature, hue="day_type")
    plt.title(f"{feature}: Weekday vs Weekend per site")
    plt.show()

def correlation_matrix(df):
    import numpy as np
    
    drop_cols = ["site_mapped", "cell_mapped", "datetime"]
    
    # keep only features
    df_feats = df.drop(columns=drop_cols)
    
    # correlation matrix
    corr = df_feats.corr()
    
    # keep only upper triangle to avoid duplicates
    corr_pairs = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .unstack()
        .dropna()
        .sort_values(key=abs, ascending=False)
    )
    
    print(corr_pairs.to_string())

def PCA_analysis(df):
    drop_cols = ["site_mapped", "cell_mapped", "datetime"]

    # drop columns
    df_feats = df.drop(columns=drop_cols)
    
    pca = PCA()

    df_pca = pca.fit_transform(df_feats)
    explained = pca.explained_variance_ratio_
    plt.plot(np.cumsum(explained))
    plt.axhline(0.9, color = "r", linestyle ='- -')




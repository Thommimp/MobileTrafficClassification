import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

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
    # drop non-numeric / ID columns if they exist
    drop_cols = ["site_mapped", "cell_mapped", "datetime", "tech"]
    df_feats = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    # correlation matrix
    corr = df_feats.corr()
    
    # visualize
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.show()

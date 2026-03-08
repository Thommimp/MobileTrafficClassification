import matplotlib.pyplot as plt

def plot_feature_on_time(df, tower, cell, feature):
    subset = df[(df["site_mapped"] == tower) & (df["cell_mapped"] == cell)]
    x = subset["datetime"]
    y = subset[feature]

    plt.plot(x, y, label=f"{tower} - {cell}")
    plt.xlabel("Time")
    plt.ylabel(feature)
    plt.title(f"Cell Data for {tower} - {cell}")
    plt.legend()
    plt.show()

 

    

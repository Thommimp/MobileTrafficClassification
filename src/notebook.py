import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from tdcnet_mtc.constants import data_root
    import matplotlib.pyplot as plt
    from data_pro import remove_small_length, normalize_values
    from plot_functions import plot_feature_on_time, plot_two_cells, average_feature_across_tower, plot_heat_map
    from model import stats_model_by_season

    return (
        average_feature_across_tower,
        data_root,
        normalize_values,
        pd,
        plot_feature_on_time,
        plot_heat_map,
        plot_two_cells,
        plt,
        remove_small_length,
        stats_model_by_season,
    )


@app.cell
def _(data_root, pd):
    df = pd.read_parquet(data_root / "dataset_25022026.parquet")
    df_cells = pd.read_parquet(data_root / "cells_14032026.parquet")
    df_cells
    return (df,)


@app.cell
def _(df, normalize_values, remove_small_length):
    df_processed = (
    remove_small_length(df, 15000)
    .pipe(normalize_values)
     )
    return (df_processed,)


@app.cell
def _(box_plot_per_week, df_processed):
    box_plot_per_week(df_processed, "nr_dl_avg_active_ues") 
    return


@app.cell
def _(box_plot_summer_vs_other, df_processed):
    box_plot_summer_vs_other(df_processed, "lte_pmpdcp_ps_data_volume_dl_mb")
    return


@app.cell
def _(df_processed, plt):
    import seaborn as sns
    feature = "nr_dl_avg_active_ues"

    monthly_avg = (
        df_processed.set_index("datetime")
        .groupby("site_mapped")[feature]
        .resample("D")  # Month End
        .mean()
        .reset_index()
    )
    # 2. compute std of monthly averages per site
    std = monthly_avg.groupby("site_mapped")[feature].std().reset_index()
    print(std)
    # 3. for visualization, turn it into a single-column DataFrame for boxplot
    sns.boxplot(data=std, x="site_mapped", y=feature)
    plt.title(f"Month-to-month variation of {feature} per site")
    plt.show()
    return


@app.cell
def _(df_processed):
    from plot_functions import box_plot_summer_vs_other
    box_plot_summer_vs_other(df_processed, "nr_dl_avg_active_ues")
    return (box_plot_summer_vs_other,)


@app.cell
def _():
    return


@app.cell
def _(df_processed):
    tower_map = (
        df_processed.groupby("site_mapped")["cell_mapped"]
        .unique()
        .apply(list)
        .to_dict()
    )

    for tower, cells in tower_map.items():
        print(f"{tower}: {cells}\n")
    return


@app.cell
def _(df_processed, plot_feature_on_time):
    plot_feature_on_time(df_processed, "R1", "1C", "nr_dl_avg_active_ues")
    return


@app.cell
def _(df_processed, plot_two_cells):
    plot_two_cells(df_processed, "R1", "3C", "U1", "3C", "nr_dl_avg_active_ues")
    return


@app.cell
def _(df_processed, plot_two_cells):
    plot_two_cells(df_processed, "R1", "1F", "U1", "1H", "lte_dl_avg_active_ues")
    return


@app.cell
def _(df_processed, plot_heat_map):
    plot_heat_map(df_processed)
    return


@app.cell
def _(average_feature_across_tower, df_processed):
    #4g doesnt seem to share the same patterns as 5g?
    average_feature_across_tower(df_processed, "R1", "lte_dl_avg_active_ues")
    return


@app.cell
def _(df_processed, stats_model_by_season):
    stats_model_by_season(df_processed, "U1") 
    stats_model_by_season(df_processed, "U2") 
    return


@app.cell
def _(df_processed, stats_model_by_season):
    stats_model_by_season(df_processed, "R1") 
    stats_model_by_season(df_processed, "R2") 
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

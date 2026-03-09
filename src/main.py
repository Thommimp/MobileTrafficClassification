import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from tdcnet_mtc.constants import data_root
    import matplotlib.pyplot as plt
    from data_pro import remove_small_length, remove_cell_no_data, combine_columns, normalize_values
    from plot_functions import plot_feature_on_time, plot_two_cells, average_feature_across_tower, plot_heat_map
    from model import stats_model_by_season

    return (
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
    return (df,)


@app.cell
def _(df, pd):
    pd.set_option("display.max_rows", None)  # show all rows

    print(df.head(1))
    return


@app.cell
def _(df, normalize_values, remove_small_length):
    print(df.columns)
    df_processed = (
    remove_small_length(df, 15000)
    .pipe(normalize_values)
    #.pipe(combine_columns)
    #.pipe(normalize_values)
    )
    return (df_processed,)


@app.cell
def _(df_processed, pd):
    pd.set_option("display.max_rows", None)  # show all rows
    print(df_processed.dtypes.reset_index().rename(columns={"index": "column", 0: "dtype"}))
    return


@app.cell
def _(df_processed, plot_heat_map):
    plot_heat_map(df_processed)
    return


@app.cell
def _(df_processed, plt):
    import seaborn as sns

    # select only the numeric features you care about
    features = [
        "pm_radio_sinr_pusch_avg",
        "pm_sinr_pusch_avg", 
        "pm_radio_sinr_pusch_max",
        "pm_sinr_pusch_max",
        "pmmac_ps_data_volume_dl_mb",
        "pmmac_ps_data_volume_ul_mb",
        "avg_dl_utilisation_prb",
        "avg_ul_utilisation_prb",
        "dl_avg_active_ues",
        "ul_avg_active_ues",
        "dl_peak_active_ues",
        "ul_peak_active_ues",
        "avg_dl_mac_ue_thput_mbps",
        "avg_ul_mac_ue_thput_mbps",
        "pmpdcp_ps_data_volume_dl_mb",
        "pmpdcp_ps_data_volume_ul_mb",
        "avg_prb_utilisation_ul",
        "avg_prb_utilisation_dl",
        "avg_ul_pdcp_ue_thput_mbps",
        "avg_dl_pdcp_ue_thput_mbps"
    ]

    df_feats = df_processed[features]

    # correlation matrix
    corr = df_feats.corr()

    # visualize
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.show()
    return


@app.cell
def _(df_processed, extract_cell_behavior_features):
    extract_cell_behavior_features(df_processed)
    return


@app.cell
def _(df_processed):

    print(df_processed.columns)
    # select columns
    towers = {"R1", "U1", "R2", "U2"}
    tower_df = {}
    for tower in towers:
        tower_df[tower] = df_processed[df_processed["site_mapped"] == tower]
        list_of_cell_names =  tower_df[tower]["cell_mapped"].unique().tolist()
        print(tower)
        print(list_of_cell_names)
    return


@app.cell
def _(df_processed, stats_model_by_season):
    stats_model_by_season(df_processed, "R1") 
    return


@app.cell
def _(df, stats_model_by_season):
    subset = df[df["cell_mapped"] != "4A"]   # remove 4A
    subset = subset[subset["cell_mapped"] != "5A"]   # remove 4A
    subset = subset[subset["cell_mapped"] != "6A"]   # remove 4A

    #subset = subset[subset["cell_mapped"] != "1S"]   # remove 4A
    #subset = subset[subset["cell_mapped"] != "2S"]   # remove 4A
    #subset = subset[subset["cell_mapped"] != "3S"]   # remove 4A

    stats_model_by_season(subset, "U2") 
    return


@app.cell
def _(df, plot_feature_on_time):
    plot_feature_on_time(df, "R1", "1C", "nr_dl_avg_active_ues")
    return


@app.cell
def _(df, plot_two_cells):
    plot_two_cells(df, "R1", "3C", "U1", "3C", "nr_dl_avg_active_ues")
    plot_two_cells(df, "R1", "3C", "U1", "3C", "pm_sinr_pusch_max")
    return


@app.cell
def _(df, plot_feature_on_time):
    plot_feature_on_time(df, "R1", "1C", "lte_avg_prb_utilisation_ul")
    return


@app.cell
def _(ex):
    ex
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

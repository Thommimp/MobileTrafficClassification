import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from tdcnet_mtc.constants import data_root
    import matplotlib.pyplot as plt

    from plot_functions import plot_feature_on_time, plot_two_cells, average_feature_across_tower 
    from model import stats_model_by_season  
    return (
        average_feature_across_tower,
        data_root,
        pd,
        plot_feature_on_time,
        plot_two_cells,
    )


@app.cell
def _(data_root, pd):
    df = pd.read_parquet(data_root / "dataset_25022026.parquet")
    print(df.columns)
    return (df,)


@app.cell
def _(df):
    # select columns
    towers = {"R1", "U1", "R2", "U2"}
    tower_df = {}
    for tower in towers:
        tower_df[tower] = df[df["site_mapped"] == tower]
        list_of_cell_names =  tower_df[tower]["cell_mapped"].unique().tolist()
        print(tower)
        print(list_of_cell_names)
    return


@app.cell
def _(df, plot_feature_on_time):
    stats_model_by_season(df, "R1") 
    return


@app.cell
def _(average_feature_across_tower, df):
    average_feature_across_tower(df, "R1", "nr_dl_avg_active_ues")
    return

@app.cell
def _(average_feature_across_tower, df):
    average_feature_across_tower(df, "U1", "nr_dl_avg_active_ues")
    return

@app.cell
def _(df, plot_two_cells):
    plot_two_cells(df, "R1", "3C", "U1", "3C", "nr_dl_avg_active_ues")
    plot_two_cells(df, "R1", "3C", "U1", "3C", "pm_sinr_pusch_max")
    return


if __name__ == "__main__":
    app.run()

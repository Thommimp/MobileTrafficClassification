import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from tdcnet_mtc.constants import data_root

    return data_root, pl


@app.cell
def _(data_root, pl):
    df = pl.scan_parquet(data_root / "dataset_25022026.parquet")
    return (df,)


@app.cell
def _(df, pl):
    df.select(pl.col("site_mapped"), pl.col("cell_mapped")).unique().sort(pl.col("site_mapped"), pl.col("cell_mapped")).collect()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

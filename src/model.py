def stats_model_by_season(df, tower):
    

    subset = df[df["site_mapped"] == tower].copy()
    subset["month"] = subset["datetime"].dt.month
    
    
    cell_feature_map = {}
    for cell, cell_df in subset.groupby("cell_mapped"):
        print(f"running {cell}")
        feature_col = pick_feature(cell_df, cell_name=cell)
        cell_feature_map[cell] = feature_col

            # print whether it's 4G or 5G
        tech = "5G" if feature_col.startswith("nr") else "4G"
        print(f"Cell {cell} is {tech}")

    monthly_avg = subset.groupby(["cell_mapped", "month"])[feature_col].mean().unstack(fill_value=0)


def pick_feature(cell_df, cell_name=None):
    feature_cols = ["nr_dl_avg_active_ues", "lte_dl_avg_active_ues"]
    non_empty_cols = [col for col in feature_cols if cell_df[col].notna().any()]
    
    if len(non_empty_cols) == 1:
        print("good")
        return non_empty_cols[0]
    elif len(non_empty_cols) == 0:
        raise ValueError(f"Cell {cell_name} has no data in any feature column.")
    else:  # more than one
        raise ValueError(f"Cell {cell_name} has values in multiple feature columns: {non_empty_cols}")

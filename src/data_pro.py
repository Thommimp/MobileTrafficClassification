
def remove_small_length(df, threshold):
    for site, site_df in df.groupby("site_mapped"):
        print(site)
        for cell, cell_df in site_df.groupby("cell_mapped"):
            if threshold > len(cell_df):
                #remove cell from DF
                df = df[df["cell_mapped"] != cell]
                print(f"removed {cell} from site {site}, had {len(cell_df)} rows") 
    return df

def remove_cell_no_data(df):
    # get all columns that start with "lte_"
    lte_cols = [col for col in df.columns if col.startswith("lte_")]

    # generate feature pairs
    feature_pairs = []
    for col in lte_cols:
        nr_col = col.replace("lte_", "nr_")
        

        # special cases for pmpdcp → pmmac
        if col == "lte_pmpdcp_ps_data_volume_ul_mb":
            nr_col = "nr_pmmac_ps_data_volume_ul_mb"
            feature_pairs.append([col, nr_col])
        elif col == "lte_pmpdcp_ps_data_volume_dl_mb":
            nr_col = "nr_pmmac_ps_data_volume_dl_mb"
            feature_pairs.append([col, nr_col])
        # PDCP throughput → NR MAC throughput (directions swap)
        elif col == "lte_avg_ul_pdcp_ue_thput_mbps":
            nr_col = "nr_avg_ul_mac_ue_thput_mbps"
            #neutral_name = "avg_ue_throughput_mbps_ul"
            feature_pairs.append([col, nr_col])
        elif col == "lte_avg_dl_pdcp_ue_thput_mbps":
            nr_col = "nr_avg_dl_mac_ue_thput_mbps"
            feature_pairs.append([col, nr_col])
            #neutral_name = "avg_ue_throughput_mbps_dl"
        else:
            feature_pairs.append([col, nr_col])  

    for feature_cols in feature_pairs:
        # compute per-cell whether LTE/NR has any data
        cell_has_data = (
            df.groupby(["site_mapped", "cell_mapped"])[feature_cols]
            .apply(lambda x: x.notna().any())
            .reset_index()
        )
         # check for cells that have data in both LTE and NR columns
        both_data_mask = cell_has_data[feature_cols[0]] & cell_has_data[feature_cols[1]]
        if both_data_mask.any():
            both_cells = cell_has_data[both_data_mask]
            for _, row in both_cells.iterrows():
                print(f"Warning: Cell ({row['site_mapped']}, {row['cell_mapped']}) "
                      f"has values in both features {feature_cols[0]} and {feature_cols[1]}") 
            
        # drop cells with no data in either feature
        mask_no_data = ~(cell_has_data[feature_cols[0]] | cell_has_data[feature_cols[1]])
        if mask_no_data.any():
            print(f"Dropping {mask_no_data.sum()} cells with no data")
        cell_has_data = cell_has_data[~mask_no_data]

        # assign tech column
        cell_has_data["tech"] = cell_has_data[feature_cols[0]].map({True: "4G", False: "5G"})

        # merge back to original dataframe
        df = df.merge(cell_has_data[["site_mapped", "cell_mapped", "tech"]],
                      on=["site_mapped", "cell_mapped"],
                      how="inner")

    return df
def combine_columns(df):
    # define LTE and NR metric columns
    lte_cols = [c for c in df.columns if c.startswith('lte_')]
    nr_cols = [c for c in df.columns if c.startswith('nr_')]

    # for 5G rows, copy NR columns to unified names
    df_5g = df['tech'] == '5G'
    for c in nr_cols:
        df.loc[df_5g, c.replace('nr_', '')] = df.loc[df_5g, c]

    # for 4G rows, copy LTE columns to unified names
    df_4g = df['tech'] == '4G'
    for c in lte_cols:
        df.loc[df_4g, c.replace('lte_', '')] = df.loc[df_4g, c]

    # drop original LTE/NR columns
    df = df.drop(columns=lte_cols + nr_cols)

    return df

def normalize_values(df):
    cols_to_skip = ["cell_mapped", "site_mapped", "datetime"]
    cols_to_normalize = df.columns.difference(cols_to_skip)

    for col in cols_to_normalize:
        mean = df.groupby(["site_mapped", "cell_mapped"])[col].transform("mean")
        std = df.groupby(["site_mapped", "cell_mapped"])[col].transform("std")
        df[col] = (df[col] - mean) / std

    return df


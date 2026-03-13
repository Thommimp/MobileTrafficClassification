def remove_small_length(df, threshold):
    for site, site_df in df.groupby("site_mapped"):
        print(site)
        for cell, cell_df in site_df.groupby("cell_mapped"):
            if threshold > len(cell_df):
                #remove cell from DF
                df = df[df["cell_mapped"] != cell]
                print(f"removed {cell} from site {site}, had {len(cell_df)} rows") 
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
        #df[col] = df.groupby(["site_mapped", "cell_mapped"])[col].transform(zscore, ddof=1)
    return df


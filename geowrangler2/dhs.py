# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_dhs.ipynb.

# %% auto 0
__all__ = ['load_column_config', 'load_dhs_file', 'apply_threshold', 'assign_wealth_index']

# %% ../nbs/04_dhs.ipynb 4
from typing import List

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.decomposition import PCA

# %% ../nbs/04_dhs.ipynb 5
PH_COLUMN_CONFIG = {
    "cluster number": "DHSCLUST",
    "wealth index factor score combined (5 decimals)": "Wealth Index",
    "country code and phase": "country code and phase",
    "number of rooms used for sleeping": "rooms",
    "has electricity": "electric",
    "has mobile telephone": "mobile telephone",
    "has radio": "radio",
    "has television": "television",
    "has car/truck": "car/truck",
    "has refrigerator": "refrigerator",
    "has motorcycle/scooter": "motorcycle",
    "main floor material": "floor",
    "type of toilet facility": "toilet",
    "source of drinking water": "drinking water",
}

KH_COLUMN_CONFIG = {
    "cluster number": "DHSCLUST",
    "wealth index factor score (5 decimals)": "Wealth Index",
    "country code and phase": "country code and phase",
    "number of rooms used for sleeping": "rooms",
    "has electricity": "electric",
    "has mobile telephone": "mobile telephone",
    "has radio": "radio",
    "has television": "television",
    "has car/truck": "car/truck",
    "has refrigerator": "refrigerator",
    "has motorcycle/scooter": "motorcycle",
    "main floor material": "floor",
    "type of toilet facility": "toilet",
    "na - source of drinking water": "drinking water",
}
MM_COLUMN_CONFIG = {
    "cluster number": "DHSCLUST",
    "wealth index factor score combined (5 decimals)": "Wealth Index",
    "country code and phase": "country code and phase",
    "number of rooms used for sleeping": "rooms",
    "has electricity": "electric",
    "has mobile telephone": "mobile telephone",
    "has radio": "radio",
    "has television": "television",
    "has car/truck": "car/truck",
    "has refrigerator": "refrigerator",
    "has motorcycle/scooter": "motorcycle",
    "main floor material": "floor",
    "type of toilet facility": "toilet",
    "source of drinking water": "drinking water",
}
TL_COLUMN_CONFIG = {
    "cluster number": "DHSCLUST",
    "wealth index factor score combined (5 decimals)": "Wealth Index",
    "country code and phase": "country code and phase",
    "number of rooms used for sleeping": "rooms",
    "has electricity": "electric",
    "has mobile telephone": "mobile telephone",
    "has radio": "radio",
    "has television": "television",
    "has car/truck": "car/truck",
    "has refrigerator": "refrigerator",
    "has motorcycle/scooter": "motorcycle",
    "main floor material": "floor",
    "type of toilet facility": "toilet",
    "source of drinking water": "drinking water",
}

COLUMN_CONFIG = {
    "ph": PH_COLUMN_CONFIG,
    "kh": KH_COLUMN_CONFIG,
    "mm": MM_COLUMN_CONFIG,
    "tl": TL_COLUMN_CONFIG,
}

# %% ../nbs/04_dhs.ipynb 6
def load_column_config(
    country: str,  # 2 letter character representing the country
) -> dict:
    """Get predined column mapping for some countries.
    The following countries area supported:
    - `ph` Philippines
    - `tl` East Timor
    - `mm` Myanmar
    - `kh` Cambodia
    """
    if country in COLUMN_CONFIG:
        return COLUMN_CONFIG[country]
    else:
        raise ValueError(
            f"Not a valid country. Valid countries are {list(COLUMN_CONFIG.keys())}"
        )

# %% ../nbs/04_dhs.ipynb 7
def load_dhs_file(
    household_data: str,  # str or pathlike object to the household data
) -> DataFrame:
    """Loads household data and renames columns based on variable labels of the file"""
    dhs_reader = pd.read_stata(
        household_data, convert_categoricals=False, iterator=True
    )
    dhs_dict = dhs_reader.variable_labels()
    with dhs_reader:
        dhs_df = dhs_reader.read()
    dhs_df.rename(columns=dhs_dict, inplace=True)
    return dhs_df

# %% ../nbs/04_dhs.ipynb 8
def apply_threshold(
    df: DataFrame,  # Dataframe
    columns: List[str],  # List of columns to apply the threshold
    config: dict,  # Config containing the min and max of each columns
) -> DataFrame:
    """Applies a threshold to a list of columns"""
    copied = df.copy()
    for col in columns:
        if col in config:
            copied[col] = copied[col].clip(*config[col])
        elif "_default" in config:
            copied[col] = copied[col].clip(*config["_default"])
    return copied

# %% ../nbs/04_dhs.ipynb 9
def assign_wealth_index(
    asset_df: DataFrame,  # Dataframe containg only the features to apply wealth index
    use_pca=True,  # if calculating wealth index should be done via PCA or via Sigular Value Decomposition
):
    if use_pca:
        pca = PCA(1)
        pca.fit(asset_df.values)

        first_comp_vec_scaled = np.matmul(asset_df, pca.components_.T).squeeze()

    else:
        asset_df = asset_df.apply(lambda x: x - x.mean(), axis=1)
        u, s, _ = np.linalg.svd(asset_df.values.T, full_matrices=False)
        orthog_pc1_proj = np.matmul(asset_df, u[0])
        first_comp_vec_scaled = s[0] * orthog_pc1_proj
    return first_comp_vec_scaled
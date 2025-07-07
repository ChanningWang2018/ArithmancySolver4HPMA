import json

import numpy as np
import pandas as pd


def load_data_from_csv(file_path: str, name_col: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    df = pd.read_csv(
        filepath_or_buffer=file_path,
        dtype={
            "gold": np.int16,
            "gems": np.int16,
            "name": str,
            "tier": str,
        },
    ).fillna("")
    df["name"] = pd.Categorical(df[name_col])
    df["tier"] = pd.Categorical(df["tier"])
    return df


PLANTS_DF = load_data_from_csv("plants.csv", "name")
DISHES_DF = load_data_from_csv("dishes.csv", "name")


def load_labels_from_json() -> dict:
    with open("ui/labels.json", "r", encoding="utf-8") as f:
        labels = json.load(f)
    return labels


LABELS = load_labels_from_json()
PLANTS_LABELS = LABELS["en"]["plants"]
DISHES_LABELS = LABELS["en"]["dishes"]
TIERS_LABELS = LABELS["en"]["tiers"]

PLANTS_LABELS_CN = LABELS["cn"]["plants"]
DISHES_LABELS_CN = LABELS["cn"]["dishes"]
TIERS_LABELS_CN = LABELS["cn"]["tiers"]

GOLD_PLANTS_DF = PLANTS_DF[
    PLANTS_DF["gold"] > 1
]  # Filter out plants with price greater than 1 gold
GEMS_PLANTS_DF = PLANTS_DF[PLANTS_DF["gems"] > 0]

GOLD_DISHES_DF = DISHES_DF[DISHES_DF["gold"] > 0]
GEMS_DISHES_DF = DISHES_DF[DISHES_DF["gems"] > 0]

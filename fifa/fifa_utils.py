import numpy as np
import seaborn as sns
import sys
import pandas as pd

sys.path.append("..")
data = pd.read_csv("../data/players_22.csv", low_memory=False)

def keep_first_pos(string):
    """
    Garde la 1ere position du joueur pour un élément *series* de la data Series 
    """
    return string.split(",")[0]


def set_global_position(position):
    """
    A partir d'une *position* précise, renvoie la position globale (ex: RW -> FWD)
    """
    if position == "GK":
        return "GK"
    positions = { "DEF" : ["CB", "LB", "RB", "LWB", "RWB"],
                "MID" : ["CM", "CDM", "LM", "CAM", "RM"],
                "FWD" : ["RW", "ST", "LW", "CF", "LF", "RF"] }
    for glob in positions:
        if position in positions[glob]:
            return glob


def classify_age(age):
    if age < 20:
        return "-20"
    if age < 25:
        return "20-25"
    if age < 30:
        return "25-30"
    if age < 35:
        return "30-35"
    else:
        return "+35"


def format_stat(string):
    """
    Convertit les entrées du type "<n1>+<n2>" et "<n1>-<n2>" en entier <n1>
    """
    sep = "+"
    if "-" in string:
        sep = "-"
    return int(string.split(sep)[0])


def convert_cm_to_m(height_cm):
    return float(height_cm) / 100


def metric_category_from_std_reference(metric_std):
    """
    Retourne une fonction qui à partir d'une valeur de métrique, renvoie la catégorie à laquelle cette valeur correspond parmi "low", "moderate"
    ou "high". Cette fonction de catégorisation dépend de la valeur de référence *metric_std* qui est l'écart-type de la distribution des valeurs
    """
    def metric_category(metric):
        if metric < metric_std:
            cat = "low"
        elif metric < 2*metric_std:
            cat = "moderate"
        elif metric >= 2*metric_std:
            cat = "high"
        else:
            cat = "unknown" #NaN
        return cat

    return metric_category


def print_nan_count_in_columns(df):
    for column in df.columns:
        nb_nan = df[column].isna().sum()
        if nb_nan > 0:
            print(f"{column} : {nb_nan}")


def nb_not_nan_in_column(df, column):
    return np.logical_not(df["goalkeeping_speed"].isna()).sum()


def get_two_correlated_features(df, threshold=0.9):
    """
    Retourne une feature de *df* corrélées positivement ou négativement avec une autre au delà de *threshold*
    """
    corr_matrix = np.logical_or(df.corr() > threshold, df.corr() < -threshold)
    for column in df.columns:
        for column2 in df.columns:
            if corr_matrix[column][column2] and column != column2:
                return (column, column2)
    return None
    

def drop_correlated_features(df, threshold=0.9):
    df_decorr = df.copy()
    corr_features = get_two_correlated_features(df_decorr, threshold)
    while corr_features is not None:
        df_decorr = df_decorr.drop(corr_features[0], axis=1)
        corr_features = get_two_correlated_features(df_decorr, threshold)
    return df_decorr


def find_k_max_in_column(k, df, column)->list:
    """
    Retourne les sofifa_id des *k* plus grandes valeurs de la colonne *column* de *df* (dans l'ordre)
    /!\ df doit contenir la colonne "sofifa_id"
    """
    df = df.dropna(axis=0, subset=column) #supprime les valeurs nulles de "column"
    column_np = df[column].to_numpy()
    indices = np.flip(np.argsort(column_np))[:k]
    return df.iloc[indices]["sofifa_id"]


def get_player_name_from_sofifa_id(sofifa_id):
    return data[data["sofifa_id"] == sofifa_id]["long_name"].item()
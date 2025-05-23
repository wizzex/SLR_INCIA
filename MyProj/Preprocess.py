import pandas as pd
from tkinter import filedialog
from tkinter import Tk


def supprimer_avant_virgule(valeur):
    if isinstance(valeur, str):
        return valeur.split(", ")[1]
    else:
        return valeur


def preprocess_data(file_path):
    print("Is this raw data from AnimatLab? 1 for yes 0 for no")
    Raw = pd.read_excel(file_path)
    a = int(input())
    if a == 1:
        Raw = pd.DataFrame(Raw)
        Raw = Raw.rename(columns={Raw.columns[0]: "Temps(s)"})
        # Raw = Raw.iloc[::50, :]
        Raw.iloc[:, 0] = Raw.iloc[:, 0] * 0.0002 - 1.0002

        # Appliquer les transformations aux valeurs du DataFrame
        Raw = Raw.map(supprimer_avant_virgule)
        Raw = Raw.map(lambda x: str(x).replace(",", "."))
        Raw = Raw.apply(pd.to_numeric, errors="coerce")
        Raw.replace(-99999, 0, inplace=True)
        Raw.iloc[:, 1:] = Raw.iloc[:, 1:] * 1000

    return Raw

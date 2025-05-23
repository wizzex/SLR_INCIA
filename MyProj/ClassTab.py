# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:56:37 2024

@author: llemarchand
"""

import pandas as pd
from tkinter import filedialog
from tkinter import Tk
from Preprocess import preprocess_data
from tkinter import Tk, Label, Listbox, Button, filedialog, MULTIPLE
import os


class ExcelProcessor:
    def __init__(self):
        self.file_path = self.get_file_path()
        self.dir_path = self.get_dir_path()
        self.data_table = self.load_excel_data()
        self.file_name = self.get_file_name()

    def get_file_path(self):
        Tk().withdraw()
        file_path = filedialog.askopenfilename(
            title="Sélectionnez un fichier Excel",
            filetypes=[("Fichiers Excel", "*.xlsx;*.xls")],
        )
        return file_path

    def get_dir_path(self):
        root_path = os.path.dirname(self.file_path)
        return root_path

    def get_file_name(self):
        return self.file_path.split("/")[-1].split(".")[0]

    def load_excel_data(self):
        # Charger les données Excel
        df = preprocess_data(self.file_path)
        return df

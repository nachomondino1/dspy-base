# Importo librerias
import pandas as pd
import string
import requests
from nltk.stem import SnowballStemmer


class TextPreparation:
    """Techniques to prepare text"""

    def __init__(self, textos, l_col_to_except=None):
        self.df = pd.DataFrame(textos)  # Convertir a DataFrame
        self.l_col_to_except = l_col_to_except if l_col_to_except is not None else []
        self.set_columns_to_process()

    def set_columns_to_process(self):
        """Define las columnas a procesar"""
        cols_object = self.df.select_dtypes(include='object').columns
        cols_to_process = [col for col in cols_object if col not in self.l_col_to_except]
        self.columns_to_process = cols_to_process

    def to_lower(self):
        """Convierte a minúscula los textos"""
        for col in self.columns_to_process:
            self.df[col] = self.df[col].str.lower()

    def delete_accent(self):
        """Remueve acentos de los textos"""
        d = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
        for col in self.columns_to_process:
            self.df[col] = self.df[col].replace(d, regex=True)

    def delete_special_characters(self):
        """Remueve caracteres especiales de los textos"""
        d = {'ã': 'a', 'â': 'a', 'ä': 'a', 'ê': 'e', 'ë': 'e', 'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'ø': 'o',
             'û': 'u', 'ü': 'u', 'ñ': 'n', 'č': 'c', 'ć': 'c', 'ğ': 'g', 'ß': 'ss', 'ń': 'n', 'š': 's'}
        for col in self.columns_to_process:
            self.df[col] = self.df[col].replace(d, regex=True)

    def delete_punctuation(self):
        """Elimina signos de puntuación de los textos"""
        for col in self.columns_to_process:
            self.df[col] = self.df[col].str.replace(f'[{string.punctuation}]', ' ', regex=True) # self.df[col] = self.df[col].str.replace(f'[{string.punctuation}]', ' ')

    def tokenize(self):
        """Tokeniza los textos"""
        for col in self.columns_to_process:
            self.df[col] = self.df[col].str.split()

    def stop_word_removal(self):
        """Elimina palabras vacías de los textos"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        palabras_vacias = pd.read_csv(url, squeeze=True)
        for col in self.columns_to_process:
            self.df[col] = self.df[col].apply(lambda x: [word for word in x if word not in palabras_vacias])

    def download_stop_word_removal_file(self):
        """Descarga el archivo de palabras vacías"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        r = requests.get(url, allow_redirects=True)
        open('vacias.txt', 'wb').write(r.content)

    def stemming(self):
        """Aplica stemming a los textos"""
        spanish_stemmer = SnowballStemmer('spanish')
        for col in self.columns_to_process:
            self.df[col] = self.df[col].apply(lambda x: [spanish_stemmer.stem(word) for word in x])
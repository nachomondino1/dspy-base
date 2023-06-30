# Importo librerias
import pandas as pd
import string
import requests
from nltk.stem import SnowballStemmer


class TextPreparation:
    """Techniques to prepare text"""

    def __init__(self):  # no defino df como atributo puesto que es muy importante que el usuario reciba el df de cada funcion.
        pass

    def to_lower(self, df, columns):
        """Convierte a minúscula los textos"""
        for col in columns:
            df[col] = df[col].str.lower()
        return df

    def delete_accent(self, df, columns):
        """Remueve acentos de los textos"""
        d = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
        for col in columns:
            df[col] = df[col].replace(d, regex=True)
        return df

    def delete_special_characters(self, df, columns):
        """Remueve caracteres especiales de los textos"""
        d = {'ã': 'a', 'â': 'a', 'ä': 'a', 'ê': 'e', 'ë': 'e', 'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'ø': 'o',
             'û': 'u', 'ü': 'u', 'ñ': 'n', 'č': 'c', 'ć': 'c', 'ğ': 'g', 'ß': 'ss', 'ń': 'n', 'š': 's'}
        for col in columns:
            df[col] = df[col].replace(d, regex=True)
        return df

    def delete_punctuation(self, df, columns):
        """Elimina signos de puntuación de los textos"""
        for col in columns:
            df[col] = df[col].str.replace(f'[{string.punctuation}]', ' ', regex=True)
        return df

    def tokenize(self, df, columns):
        """Tokeniza los textos"""
        for col in columns:
            df[col] = df[col].str.split()
        return df

    def stop_word_removal(self, df, columns):
        """Elimina palabras vacías de los textos"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        palabras_vacias = pd.read_csv(url, squeeze=True)
        for col in columns:
            df[col] = df[col].apply(lambda x: [word for word in x if word not in palabras_vacias])
        return df

    def download_stop_word_removal_file(self):
        """Descarga el archivo de palabras vacías"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        r = requests.get(url, allow_redirects=True)
        open('vacias.txt', 'wb').write(r.content)

    def stemming(self, df, columns):
        """Aplica stemming a los textos"""
        spanish_stemmer = SnowballStemmer('spanish')
        for col in columns:
            df[col] = df[col].apply(lambda x: [spanish_stemmer.stem(word) for word in x])
        return df
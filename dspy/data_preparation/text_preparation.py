# Importo librerias
import pandas as pd
from nltk.stem import SnowballStemmer
import requests
import string


class TextPreparation:
    """Techniques to prepare text"""

    def __init__(self, df, column):
        self.textos = df[column]

    def to_lower(self):
        """Convierte a minúscula los textos"""
        self.textos = self.textos.str.lower()
        return self.textos

    def delete_accent(self):
        """Remueve acentos de los textos"""
        d = {'á': "a", 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
        self.textos = self.textos.replace(d, regex=True)
        return self.textos

    def delete_special_characters(self):
        """Remueve caracteres especiales de los textos"""
        d = {'ã': 'a', 'â': 'a', 'ä': 'a', 'ê': 'e', 'ë': 'e', 'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'ø': 'o',
             'û': 'u', 'ü': 'u', 'ñ': "n", 'č': 'c', 'ć': 'c', 'ğ': 'g'}
        self.textos = self.textos.replace(d, regex=True)
        return self.textos

    def delete_punctuation(self):
        """Elimina signos de puntuación de los textos"""
        self.textos = self.textos.str.replace(f'[{string.punctuation}]', ' ')  # self.textos = self.textos.str.replace('[{}]'.format(string.punctuation), '')
        return self.textos

    def tokenize(self):
        """Tokeniza los textos"""
        self.textos = self.textos.str.split()
        return self.textos

    def stop_word_removal(self):
        """Elimina palabras vacías de los textos"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        palabras_vacias = pd.read_csv(url, squeeze=True)
        self.textos = self.textos.apply(lambda x: [word for word in x if word not in palabras_vacias])
        return self.textos

    def download_stop_word_removal_file(self):
        """Descarga el archivo de palabras vacías"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        r = requests.get(url, allow_redirects=True)
        open('vacias.txt', 'wb').write(r.content)

    def stemming(self):
        """Aplica stemming a los textos"""
        spanish_stemmer = SnowballStemmer('spanish')
        self.textos = self.textos.apply(lambda x: [spanish_stemmer.stem(word) for word in x])
        return self.textos
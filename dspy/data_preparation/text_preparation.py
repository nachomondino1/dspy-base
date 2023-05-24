# Importo librerias
# import pandas as pd
# import string
# import requests
# from nltk.stem import SnowballStemmer

import pandas as pd
from nltk.stem import SnowballStemmer
import requests
import string

class TextPreparation:
    """Techniques to prepare text"""

    def __init__(self, textos):
        # self.textos = textos.astype(str)  # Convertir a cadena de texto
        self.textos = textos.copy()

    def to_lower(self):
        """Convierte a minúscula los textos"""
        self.textos = self.textos.str.lower()

    def delete_accent(self):
        """Remueve acentos de los textos"""
        d = {'á': "a", 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
        self.textos = self.textos.replace(d, regex=True)

    def delete_special_characters(self):
        """Remueve caracteres especiales de los textos"""
        d = {'ñ': "n", 'ã': 'a'}
        self.textos = self.textos.replace(d, regex=True)

    def delete_punctuation(self):
        """Elimina signos de puntuación de los textos"""
        self.textos = self.textos.str.replace('[{}]'.format(string.punctuation), '')

    def tokenize(self):
        """Tokeniza los textos"""
        self.textos = self.textos.str.split()

    def stop_word_removal(self):
        """Elimina palabras vacías de los textos"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        palabras_vacias = pd.read_csv(url, squeeze=True)
        self.textos = self.textos.apply(lambda x: [word for word in x if word not in palabras_vacias])

    def download_stop_word_removal_file(self):
        """Descarga el archivo de palabras vacías"""
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        r = requests.get(url, allow_redirects=True)
        open('vacias.txt', 'wb').write(r.content)

    def stemming(self):
        """Aplica stemming a los textos"""
        spanish_stemmer = SnowballStemmer('spanish')
        self.textos = self.textos.apply(lambda x: [spanish_stemmer.stem(word) for word in x])

'''
class TextPreparation:
    """Techniques to prepare text"""

    def __init__(self, textos):
        self.textos = textos  # debe ser una serie de pandas y no una frase suelta

    def to_lower(self):
        """
        Convierte a miniscula los textos de la Serie de texto
        :return: Serie del texto en miniscula
        """
        # Defino variables
        l_new_texts = []

        # Por text
        for text in self.textos:

            # Convierto a minuscula si no es nan
            l_new_texts.append(text.lower() if isinstance(text, str) else text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(l_new_texts)
        # return self.textos

    def delete_accent(self):
        """
        Remueve acentos de textos de una Serie de texto
        :return: Serie del texto sin acentos
        """
        # Defino variables
        d = {'á': "a", 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}  # diccionario, letra con acento en key y sin en value
        l_new_texts = []

        # Por texto
        for text in self.textos:

            # Verificar si el elemento es un string
            if isinstance(text, str):

                new_text = str()

                # Por caracter del texto
                for char in text:

                    # Si es una letra con tilde la reemplazo
                    new_text += d[char] if char in d.keys() else char

                # Guardo texto procesado
                l_new_texts.append(new_text)

            # Si es nan, lo guardo sin procesar
            else:
                l_new_texts.append(text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(l_new_texts)

    def delete_special_characters(self):
        """
        Remueve acentos de textos de una Serie de texto
        :return: Serie del texto sin acentos
        """
        # Defino variables
        d = {'ñ': "n", 'ã': 'a'}  # diccionario, letra con acento en key y sin en value
        l_new_texts = []

        # Por texto
        for text in self.textos:

            # Verificar si el elemento es un string
            if isinstance(text, str):

                new_text = str()

                # Por caracter del texto
                for char in text:

                    # Si es una letra con tilde la reemplazo
                    new_text += d[char] if char in d.keys() else char

                # Guardo texto procesado
                l_new_texts.append(new_text)

            # Si es nan, lo guardo sin procesar
            else:
                l_new_texts.append(text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(l_new_texts)

    def delete_punctuation(self):
        """
        Elimina cualquier signo de puntuacion de textos de una Serie de texto
        :return: Serie del texto sin puntuacion
        """
        # Defino variables
        l_new_texts = []

        # Por text
        for text in self.textos:

            # Verificar si el elemento es un string
            if isinstance(text, str):

                new_text = str()

                # Por caracter del texto
                for char in text:

                    # si es un signo de puntuacion, la reemplazo por ""
                    new_text += "" if char in string.punctuation else char

                # Guardo texto procesado
                l_new_texts.append(new_text)

            # Si es nan, lo guardo sin procesar
            else:
                l_new_texts.append(text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(l_new_texts)

    def tokenize(self):
        """
        Tokeniza textos de una Serie de texto, es decir, convierte cada texto en una lista cuyos elementos es cada
        palabra de este.
        :return: Serie del texto tokenizado
        """
        # Defino variables
        new_texts = []

        # Por text
        for text in self.textos:

            # Hago split
            new_text = text.split()

            # Guardo texto procesado
            new_texts.append(new_text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(new_texts)

    def stop_word_removal(self):
        """
        Elimina palabras vacias de textos de una Serie de texto
        :return: Serie del texto sin palabras vacias
        """
        # Read lista de palabras a remover (vacias.txt)
        path = '/Users/nachomondino/Documents/GitHub/evaluacion-compra-automatica/p2_data_preparation/utils/vacias.txt'
        palabras_vacias = pd.read_csv(path)
        palabras_vacias = list(palabras_vacias['palabra'])  # ['palabra'] hace que acceda a la columna y lo convierto en lista para poder hacer la comparacion if token in palabras vacias

        # Defino variable
        new_texts = []

        # Por text
        for text in self.textos:

            new_text = []  # Lista de tokens nuevos sin las palabras vacias

            # Por palabra del texto
            for word in text:

                # Si la palabra es una palabra vacia
                if word in palabras_vacias:

                    # No guardo la palabra
                    pass

                # Si la palabra no es una palabra vacia
                else:
                    # Guardo palabra
                    new_text.append(word)

            # Guardo texto procesado
            new_texts.append(new_text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(new_texts)

    def download_stop_word_removal_file(self):
        """
        Descarga archivo que contiene todas las palabras vacias
        :return:
        """
        url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
        r = requests.get(url, allow_redirects=True)
        return open('vacias.txt', 'wb').write(r.content)

    def steamming(self):
        """
        Aplica steamming de textos de una Serie de texto
        :return: Serie del texto con palabras steam
        """
        # Defino variables
        new_text = []
        new_texts = []
        spanish_stemmer = SnowballStemmer('spanish')

        # Por token
        for token in self.textos:

            # Por palabra
            for word in token:

                # Le hago steam a la palabra
                new_text.append(spanish_stemmer.stem(word))

            # Guardo texto procesado
            new_texts.append(new_text)

        # Reemplazo textos por textos procesados
        self.textos = pd.Series(new_texts)
'''

'''
# Importo librerias
import pandas as pd
import string
import requests
from nltk.stem import SnowballStemmer


def to_lower(textos):
    """
    Convierte a miniscula los textos de la Serie de texto
    :return: Serie de pandas. Cada elemento siendo un texto en minuscula
    """
    # Defino variables
    new_texts = []

    # Por text
    for text in textos:

        # Obtengo texto en miniscula
        new_text = text.lower()

        # Guardo texto procesado
        new_texts.append(new_text)

    # Reemplazo textos por textos procesados
    textos = pd.Series(new_texts)
    return textos

def delete_accent(textos):
    """
    Remueve acentos de textos de una Serie de texto
    :return: Serie de pandas. Cada elemento siendo un texto sin acentos
    """
    # Defino variables
    d = {'á': "a", 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}  # diccionario, letra con acento en key y sin en value
    new_texts = []

    # Por texto
    for text in textos:
        new_text = str()

        # Recorro cada letra del texto
        for i in range(len(text)):

            # Si la letra tiene acento
            if text[i] in d.keys():

                # Reemplazo letra con acento por letra sin acento
                new_text += d[text[i]]

            # Si la letra no tiene acento
            else:
                # no reemplazo nada
                new_text += text[i]

        # Guardo texto procesado
        new_texts.append(new_text)

    # Reemplazo textos por textos procesados
    textos = pd.Series(new_texts)
    return textos

def delete_punctuation(textos):
    """
    Elimina cualquier signo de puntuacion de textos de una Serie de texto
    :return: Serie de pandas. Cada elemento siendo un texto sin puntuación
    """
    # Defino variables
    new_texts = []

    # Por text
    for text in textos:
        new_text = str()  # nuevo texto sin acentos

        # Recorro cada letra del texto
        for i in range(len(text)):

            # si es un signo de puntuacion
            if text[i] in string.punctuation:
                # guardar string vacio
                new_text += ""

            # no es un signo de puntuacion
            else:
                # guardo string
                new_text += text[i]

        # Guardo texto procesado
        new_texts.append(new_text)

    # Reemplazo textos por textos procesados
    textos = pd.Series(new_texts)
    return textos

def tokenize(textos):
    """
    Tokeniza textos de una Serie de texto, es decir, convierte cada texto en una lista cuyos elementos es cada
    palabra de este.
    :return: Serie de pandas. Cada elemento siendo un texto tokenizado.
    """
    # Defino variables
    new_texts = []

    # Por text
    for text in textos:

        # Hago split
        new_text = text.split()

        # Guardo texto procesado
        new_texts.append(new_text)

    # Reemplazo textos por textos procesados
    textos = pd.Series(new_texts)

    return textos

def stop_word_removal(textos):
    """
    Elimina palabras vacias de textos de una Serie de texto
    :return: Serie de pandas. Cada elemento siendo un texto sin palabras vacias
    """
    # Read lista de palabras a remover (vacias.txt)
    path = '/Users/nachomondino/Documents/GitHub/evaluacion-compra-automatica/p2_data_preparation/utils/vacias.txt'
    palabras_vacias = pd.read_csv(path)
    palabras_vacias = list(palabras_vacias['palabra'])  # ['palabra'] hace que acceda a la columna y lo convierto en lista para poder hacer la comparacion if token in palabras vacias

    # Defino variable
    new_texts = []

    # Por text
    for text in textos:

        new_text = []  # Lista de tokens nuevos sin las palabras vacias

        # Por palabra del texto
        for word in text:

            # Si la palabra es una palabra vacia
            if word in palabras_vacias:

                # No guardo la palabra
                pass

            # Si la palabra no es una palabra vacia
            else:
                # Guardo palabra
                new_text.append(word)

        # Guardo texto procesado
        new_texts.append(new_text)

    # Reemplazo textos por textos procesados
    textos = pd.Series(new_texts)

    return textos

def download_stop_word_removal_file():
    """
    Descarga archivo que contiene todas las palabras vacias
    :return:
    """
    url = 'https://raw.githubusercontent.com/7PartidasDigital/AnaText/master/datos/diccionarios/vacias.txt'
    r = requests.get(url, allow_redirects=True)
    return open('vacias.txt', 'wb').write(r.content)

def steamming(textos):
    """
    Aplica steamming de textos de una Serie de texto
    :return: Serie de pandas. Cada elemento siendo un texto steam.
    """
    # Defino variables
    new_text = []
    new_texts = []
    spanish_stemmer = SnowballStemmer('spanish')

    # Por token
    for token in textos:

        # Por palabra
        for word in token:

            # Le hago steam a la palabra
            new_text.append(spanish_stemmer.stem(word))

        # Guardo texto procesado
        new_texts.append(new_text)

    # Reemplazo textos por textos procesados
    textos = pd.Series(new_texts)

    return textos
'''
# instrucciones para poder instalar nuestra librería, como por ejemplo, requisitos previos de instalación de otras librerías
import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'  # Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'dsmlpy'  # Debe coincidir con el nombre de la carpeta
AUTHOR = 'Ignacio Fabian Mondino'
AUTHOR_EMAIL = 'nachomondino1@gmail.com'
URL = 'https://github.com/nachomondino1/dspy-base'
LICENSE = 'MIT'  # Tipo de licencia
DESCRIPTION = 'Librería para desarrollar proyectos de Ciencia de datos (data science)'  # Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')  # Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [
      'pandas'
      ]  #Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
import pandas as pd
import datetime
import re

# Importo librerias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
from time import sleep


# COLLECT INITIAL DATA
def inicialize_chrome_driver(headless=False, path=None):
    """
    Inicializa un chrome driver automatico
    :param headless: Boolean. True para evitar que se abra web browser, en caso contrario, False.
    :return: Chrome driver automatico
    """
    # Defino opciones del webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")

    # Si el usuario quiere que no se abra un web browser
    if headless:
        options.add_argument("--headless")  # Hace que no se abra un web browser en tu compu

    # Si el usuario no paso un path para ejecutar el driver ejecutable (.exe)
    if path is None:
        # Inicializo el webdriver (Defino a Chrome como Web Browser)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        driver = webdriver.Chrome(executable_path=path, options=options)
    return driver

# ACCEPT COOKIES
# Forma 1: Boton aceptar cookies VISIBLE en el codigo html
def accept_cookies(driver, xpath_boton):
    """
    Click en aceptar cookies
    :param xpath: String. Ubica
    """
    # Ubico el botón "Aceptar cookies" y lo clikeo
    try:
        boton_aceptar_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_boton)))
        boton_aceptar_cookies.click()
    except:
        print("Fallo click en boton aceptar cookies")

# Forma 2: Boton aceptar cookies OCULT0 en tag #shadow-root
def accept_cookies_in_shadow_tag(driver, xpath_shadow_parent, xpath_boton):
    """
    Click en aceptar cookies
    """
    # Ubico el padre del "shadow root"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_shadow_parent)))
    shadow_parent = driver.find_element(By.XPATH, xpath_shadow_parent)

    # Obtengo el shadow root
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)

    # Ubico el botón "Aceptar cookies" y lo clikeo
    boton_aceptar_cookies = shadow_root.find_element(By.XPATH, xpath_boton)
    boton_aceptar_cookies.click()

# Forma 3: Boton aceptar cookies OCULT0 en tag #document
def accept_cookies_in_document_tag(driver, xpath_document_parent, xpath_boton):
    """
    Click en aceptar cookies
    """
    # Obtengo tag padre de #document
    iframe = driver.find_element(By.XPATH, xpath_document_parent)

    # Switcheo frame al padre de #document
    driver.switch_to.frame(iframe)

    # Ubico el botón "Aceptar cookies" y lo clikeo
    boton_aceptar_cookies = driver.find_element(By.XPATH, xpath_boton)
    boton_aceptar_cookies.click()

# LOGIN WEBSITE
def login_website(driver, user, password, xpath_user, xpath_pass, xpath_boton_login, with_user_validation=False, xpath_boton_validate_user=None):
    """
    Login website
    """
    # Busco tag input para el usuario y escribo el usuario
    user_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_user)))
    user_input.send_keys(user)

    # Si hay que validar el usuario
    if with_user_validation:

        # Localizo el boton que valida el usuario y lo clickeo
        boton_siguiente = driver.find_element(By.XPATH, xpath_boton_validate_user)
        boton_siguiente.click()

    # Busco tag input para la pass y escribo la pass
    pass_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_pass)))
    pass_input.send_keys(password)

    # Localizo el boton "Iniciar sesion" y lo clickeo
    boton_iniciar_sesion = driver.find_element(By.XPATH, xpath_boton_login)
    boton_iniciar_sesion.click()

# BOTON CARGAR MAS
def click_load_more_button(self):
    """
    Click en boton cargar mas canales
    """
    # Definicion de variables
    cant_clicks = 0

    while True:
        # Intento hacer click en boton "Cargar mas canales"
        try:
            boton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, 'XPATH_button')))
            boton.click()
            cant_clicks += 1
        except:
            print("Se hicieron {} clicks en boton 'cargar mas canales'".format(cant_clicks))
            break

class Field():

    def __init__(self, name, xpath):
        self.name = name
        self.xpath = xpath

    def extract_field(self, item):
        """
        Extrae field
        :param <param_name>: <param description>
        :return: String con field, en caso contrario, None
        """
        # Intento extraer el campo
        try:
            # Extraigo campo
            field = item.find_element(By.XPATH, self.xpath).text
            return field

        # Si falla la extraccion del campo, retorno None
        except:
            print("Fallo la extraccion del campo {}".format(self.name))
            return None


# PAGINATION
# Tipo 1:
def get_pagination_url(self):
    """
    Obtiene url de siguiente pagina si la pagina tiene link asociado
    """
    try:
        url = self.driver.find_element(By.XPATH, '<XPATH>').get_attribute('href')
        return url
    except:
        print("No pudo hacer el click en la siguiente pagina")
        return None

# Tipo 2:
def get_pagination_zocalo_button(self):
    """
    Obtiene url de siguiente pagina si la pagina no tiene link asociado y es solo un boton
    """
    try:
        boton_siguiente_pagina = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'<XPATH_boton>')))
        return boton_siguiente_pagina
    except:
        print("No pudo hacer el click en la siguiente pagina")
        return None

# Tipo 3:
def get_pagination_drop_down_list_button(self):
    """
    Obtiene url de siguiente pagina si la pagina no tiene link asociado y es solo un boton
    """
    # Click en flechita para desplegar dias (paginas de paginacion)
    self.driver.find_element(By.XPATH, '<XPATH_desplegar_flechita>').click()  # boton_desplegar

    try:
        # Obtengo tag de siguiente dia
        boton_siguiente_pagina = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'<XPATH_boton>')))
        return boton_siguiente_pagina
    except:
        print("No hay mas paginas")
        return None

def ScrollDown(self):
    """
    Carga todos los elementos en una pagina al deslizar el driver hacia abajo hasta el final
    :return:
    """
    # Defino tiempo de pausa aleatorio entre 1 y 2 segundos para evitar banneo de IP
    SCROLL_PAUSE_TIME = random.uniform(1, 2)

    # Get scroll height
    last_height = self.driver.execute_script("return document.body.scrollHeight")
    print("Last: ", last_height)
    while True:
        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        print("New: ", new_height)

        if new_height == last_height:
            break
        last_height = new_height





# DESCRIBE DATA
def getting_to_know_data(df):
    """
    Describe dataframe pasado como parametro
    :param df: Dataframe
    :return: funcion sin retorno
    """
    print("DESCRIPCION DE DATAFRAME:".center(120))

    # Data frame's dimensionality
    print("\nDataframe shape: ", df.shape)

    # See firsts 5 Dataframe's rows
    print("\nPrimeras 5 filas del dataframe:")
    pd.set_option("display.max.columns", None)  # para ver todas las columnas del df y no que las colapse
    pd.set_option("display.precision", 2)  # mostrar maximo dos decimales
    print(df.head())  # y .tail es para ver las ultimas filas

    # Displaying Data Types
    print("\nDataframe info:")
    df.info()

    # Showing Basics Statistics
    print("\nDataframe basic statistics:")
    print(df.describe(include=object))  # basic descriptive statistics for all columns


# FORMAT DATA
def format_date(df):  # Aun no la probe pues deberia hice el format de la fecha junto con la extraccion pero bueno
    """
    Convierte fecha del formato "14.02.2023 00:00" a formato "dd/mm/yyyy hh:mm", es decir, "14/02/2023 20:00"
    :param df: Dataframe. Fecha en formato "14.02.2023 20:00"
    :return: String. Fecha y hora con formato "dd/mm/yyyy", por ejemplo, "14/02/2023 20:00"
    """
    # Por registro (partido)
    for i in range(len(df)):

        # PASO 1: SPLIT FECHA (STRING) EN ELEMENTOS (DIA, MES, AÑO, HORA Y MIN)
        n_dia, n_mes, n_año, hora, min = re.split(r':|.', df.loc[i, 'fecha'])

        # Paso 2: convierto string a datetime
        fecha_datetime = datetime.datetime(int(n_año), int(n_mes), int(n_dia), int(hora), int(min))  # Convierto variable de clase 'str' a clase 'datetime.datetime'
        fecha_form = fecha_datetime.strftime("%Y/%m/%d %H:%M")  # Convierto el formato de datetime del default al formato deseado

        # Guardo fecha formateada
        df.loc[i, 'Fecha'] = fecha_form

    return df


def convert_fecha_to_datetime(df):
    # Ordeno dataframe por fecha (de mas reciente a mas viejo)
    print(type(df.fecha[0]))

    # convert to date
    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)

    # verify datatype
    print(type(df.fecha[0]))
    return df


# Utils formatting que tenia en web_scraping_projects...
def format_date(fecha_string, hora_string):
    """
    Convierte fecha del formato "Jan 14" y hora "8:00 PM" a formato "dd/mm/yyyy hh:mm", es decir,
    "14/01/2023 19:30"
    :param fecha_string: String. Fecha en formato "Jan 14"
    :param hora_string: String. Hora en formato "8:00 PM"
    :return: String. Fecha y hora con formato "dd/mm/yyyy hh:mm", por ejemplo, "14/01/2023 20:00"
    """
    # PASO 1: SPLIT FECHA (STRING) EN ELEMENTOS (DIA, MES, AÑO, HORA Y MIN)
    hora, min = split_hour_string(hora_string)  # Paso de string a un integer para la hora y otro para el min
    n_año, n_mes, n_dia = split_date_string(fecha_string)  # Paso de string a un integer para el mes y otro para el dia

    # PASO 2: FORMATEO FECHA
    # Si la fecha tiene hora o minutos
    try:
        fecha_datetime = datetime.datetime(n_año, n_mes, n_dia, hora, min) # Convierto variable de clase 'str' a clase 'datetime.datetime'
        return fecha_datetime.strftime("%d/%m/%Y %H:%M")  # Convierto el formato de datetime del default al formato deseado
    # Si la fecha no tiene hora o minutos
    except:
        fecha_datetime = datetime.datetime(n_año, n_mes, n_dia)  # Convierto variable de clase 'str' a clase 'datetime.datetime'
        return fecha_datetime.strftime("%d/%m/%Y")  # Convierto el formato de datetime del default al formato deseado

# Funciones auxiliares de format_date()
def convert_hour_AM_PM_to_24hs(hora_string):
    """
    Transforma la hora desde AM/PM (e.g. 08:30 PM) a 24 hs (e.g. 20:30)
    :param hora_string: String. Hora en formato AM/PM (e.g. 08:30 PM)
    :return: String. Hora en formato 24 hs (e.g. 20:30), o bien, mensaje de aviso
    """
    try:
        in_time = datetime.datetime.strptime(hora_string, "%I:%M %p")  # Formato hh:mm AM/PM
        out_time = datetime.datetime.strftime(in_time, "%H:%M")  # Convierto hora de AM/PM a 24 hs
        return out_time
    except:
        print("\t No se pudo convertir la hora {} de AM/PM a 24 hs. Es posible que la hora ya es en formato 24 hs".format(hora_string))
        return hora_string

def split_hour_string(hora_string):
    """
    A partir de la hora en string (e.g. 08:30 AM, 20:30), se obtiene hora y minuto (por separado) en formato entero
    :param hora_string: String. Hora en formato (e.g. 08:30 AM, 15:50, ecc)
    :return: Integer & Integer. Hora y minuto en formato entero. En caso de que falla la obtencion, None & None
    """
    # Transforma (solo si es necesario) la hora desde AM/PM (e.g. 08:30 PM) a 24 hs (e.g. 20:30)
    hora_string = convert_hour_AM_PM_to_24hs(hora_string)

    # Intento extraer hora y minuto del string
    try:
        hora, min = hora_string.split(":")  # Obtengo hora y min por separado
        return int(hora), int(min)
    # Si falla la extraccion de hora y minuto del string
    except:
        print("La hora {} no tiene el formato %I:%M".format(hora_string))
        return None, None

def split_date_string(fecha_string):
    """
    A partir de fecha en formato string, se obtiene los elementos (dia, mes y año) de la fecha por separado en formato
    entero
    :param fecha_string: String. Fecha en formato "Jan 14"
    :return: Integer & Integer & Integer. Dia, mes y año.
    """
    # Definicion de variables
    d = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, 'nov': 11, 'dec': 12}
    deduct_year = lambda mes, dia: datetime.datetime.today().year if datetime.datetime.today() <= datetime.datetime(datetime.datetime.today().year, mes, dia, 23, 59) else datetime.datetime.today().year+1

    # intento extraer dia, mes y año de string
    try:
        mes, n_dia = fecha_string.split()  # Separo string original segun espacios para obtener elementos (mes y dia)
        n_mes, n_dia = d[mes.lower()], int(n_dia)  # Convierto strings a integer
        n_año = deduct_year(n_mes, n_dia)  # Deduzco año de la fecha segun mes y dia
        return n_año, n_mes, n_dia
    # Si falla extraccion de dia, mes y año de string
    except:
        print("Fallo la conversion de la fecha {} de string a integer".format(fecha_string))  # Mensaje de aviso
        return None, None, None





def convert_hour_into_min(hora_string):  # Funcion auxiliar de get_duracion()
    """
    Calcula cantidad de minutos equivalentes a una hora en formato hh:mm. Por ejemplo, 05:30 es equivalente a 330
    minutos (5h * 60min/1h + 30 min = 330 min)
    :param hora_string: String. Hora en formato hh:mm
    :return: Integer. Hora pasada como parametro en minutos
    """
    # Descompongo hora en cantidad de horas y cantidad de minutos
    n_horas, n_min = hora_string.split(".")

    # Calculo cantidad de minutos sabiendo que 1 hora = 60 min
    n_min_total = int(n_horas) * 60 + int(n_min)
    return n_min_total

def get_date_from_actual(fecha_act, delta_days):
    """
    Obtiene una fecha unos dias posterior a partir de la fecha actual
    :param fecha_act: Datetime class, fecha actual
    :param delta_days: Integer, numero de dias posteriores a la fecha actual
    :return: String, fecha producto de la adicion de delta dias a la fecha actual
    """
    # Obtencion de siguiente fecha a partir de la actual
    next_fecha = fecha_act + datetime.timedelta(days=delta_days)

    # Formateo siguiente fecha tal que sea igual que en el XPATH de la pagina web
    next_fecha = next_fecha.strftime("%d/%m/%Y")
    return next_fecha
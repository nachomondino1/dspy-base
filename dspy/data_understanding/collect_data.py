from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
from time import sleep


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

def extract_items(driver, xpath_items):
    """
    Extrae items de una pagina
    :return:
    """
    try:
        l_items = driver.find_elements(By.XPATH, xpath_items)
        print("Cantidad de items: {}".format(len(l_items)))
    except:
        l_items = []
        print("Fallo extraccion de items")
    return l_items

def extract_field(item, xpath):
    """
    Extrae field
    :param <param_name>: <param description>
    :return: String con field, en caso contrario, None
    """
    # Intento extraer el campo
    try:
        # Extraigo campo
        field = item.find_element(By.XPATH, xpath).text
        return field

    # Si falla la extraccion del campo, retorno None
    except:
        print("Fallo la extraccion del campo")
        return None

def click_boton(driver, xpath_boton):
    """
    Obtiene url de siguiente pagina si la pagina no tiene link asociado y es solo un boton
    """
    try:
        boton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_boton)))

        try:
            boton.click()
        except:
            driver.execute_script("arguments[0].click()", boton)
    except:
        print("No se encontro el xpath del boton")
        return None

# PAGINATION
# Tipo 1:
def get_pagination_url(driver, xpath_url):
    """
    Obtiene url de siguiente pagina si la pagina tiene link asociado
    """
    try:
        url = driver.find_element(By.XPATH, xpath_url).get_attribute('href')
        return url
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

def scroll_down(driver):
    """
    Carga todos los elementos en una pagina al deslizar el driver hacia abajo hasta el final
    :return:
    """
    # Defino tiempo de pausa aleatorio entre 1 y 2 segundos para evitar banneo de IP
    SCROLL_PAUSE_TIME = random.uniform(1, 2)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Last: ", last_height)
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("New: ", new_height)

        if new_height == last_height:
            break
        last_height = new_height


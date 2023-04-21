from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import random
from time import sleep

class Crawler():
    """ It contains all the actions that the bot can perform from accepting cookies to clicking on the next one. """

    def __init__(self, headless, path):
        """Initialize attributes of the parent class."""
        self.driver = self.inicialize_chrome_driver(headless, path)

    def inicialize_chrome_driver(self, headless=True, path=None):
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

    def extract_tags(self, xpath, tag=None):
        """
        Encuentra todos los tags segun el xpath
        :return: Lista de tags
        """
        tag_inic = self.driver if tag is None else tag  # Tag desde el que buscar el xpath
        # Intento extraer el campo
        try:
            return tag_inic.find_elements(By.XPATH, xpath)
        except NoSuchElementException:
            print("Fallo la extraccion de los tags")

    def extract_text_from_tag(self, xpath, tag=None):  # Le falta 1) la posibilidad de no extraer texto, 2) la posibilidad de haya mas de un xpath posible, 3) el webdriverwait...
        """
        Extrae texto de un tag
        :param tag: Selenium Web Element del cual extraer datos. None = extraer de tutto el xpath de la pagina.
        :return: String. En caso que falle la extraccion, None
        """
        tag_inic = self.driver if tag is None else tag  # Tag desde el que buscar el xpath
        # Intento extraer el campo
        try:
            return tag_inic.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            print("Fallo la extraccion del campo")
            return None

    def click_boton(self, xpath, tag=None):
        """
        Hace click en boton. Se puede utilizar, por ejemplo, para aceptar cookies.
        :param xpath: XPATH del boton
        :param tag: Selenium WebElement desde el cual buscar el xpath
        """
        # Definicion de variables
        tag_inic = self.driver if tag is None else tag
        try:
            boton = WebDriverWait(tag_inic, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            boton.click()

        except NoSuchElementException:
            print("No se pudo encontrar el elemento utilizando el XPath proporcionado.")

        except ElementClickInterceptedException:
            try:
                self.driver.execute_script("arguments[0].click()", boton)  # Intento con execute_script por si es con JS
            except:
                print("Fallo click en boton")


    # Forma 2: Boton aceptar cookies OCULT0 en tag #shadow-root
    def accept_cookies_in_shadow_tag(self, xpath_shadow_parent, xpath_boton):
        """
        Click en aceptar cookies
        """
        # Ubico el padre del "shadow root"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_shadow_parent)))
        shadow_parent = self.driver.find_element(By.XPATH, xpath_shadow_parent)

        # Obtengo el shadow root
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_parent)

        # Ubico el botón "Aceptar cookies" y lo clikeo
        self.click_boton(tag=shadow_root, xpath=xpath_boton)

    # Forma 3: Boton aceptar cookies OCULT0 en tag #document
    def accept_cookies_in_document_tag(self, xpath_document_parent, xpath_boton):
        """
        Click en aceptar cookies
        """
        # Obtengo tag padre de #document
        iframe = self.driver.find_element(By.XPATH, xpath_document_parent)

        # Switcheo frame al padre de #document
        self.driver.switch_to.frame(iframe)

        # Ubico el botón "Aceptar cookies" y lo clikeo
        self.click_boton(xpath=xpath_boton)

    # LOGIN WEBSITE
    def login_website(self, user, password, xpath_user, xpath_pass, xpath_boton_login, with_user_validation=False, xpath_boton_validate_user=None):
        """
        Login website
        """
        # Busco tag input para el usuario y escribo el usuario
        user_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_user)))
        user_input.send_keys(user)

        # Si hay que validar el usuario
        if with_user_validation:

            # Localizo el boton que valida el usuario y lo clickeo
            boton_siguiente = self.driver.find_element(By.XPATH, xpath_boton_validate_user)
            boton_siguiente.click()

        # Busco tag input para la pass y escribo la pass
        pass_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_pass)))
        pass_input.send_keys(password)

        # Localizo el boton "Iniciar sesion" y lo clickeo
        boton_iniciar_sesion = self.driver.find_element(By.XPATH, xpath_boton_login)
        boton_iniciar_sesion.click()



    # PAGINATION
    # Tipo 1:
    def get_pagination_url(self, xpath_url):  # deberia llamarse get_url_from_tag
        """
        Obtiene url de siguiente pagina si la pagina tiene link asociado
        """
        try:
            url = self.driver.find_element(By.XPATH, xpath_url).get_attribute('href')
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

    def scroll_down(self):
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
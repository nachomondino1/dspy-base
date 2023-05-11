from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import random
from time import sleep
from googletrans import Translator


class Crawler:
    """ It contains all the actions that the bot can perform from accepting cookies to clicking on the next one. """

    def __init__(self, headless, path):
        """Initialize attributes of the parent class."""
        self.driver = self.inicialize_chrome_driver(headless, path)

    def inicialize_chrome_driver(self, headless=True, path=None):
        """
        Inicializa un chrome driver automático
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

    def click_boton(self, xpath, tag_inicial=None):
        """
        Hace click en boton. Se puede utilizar, por ejemplo, para aceptar cookies.
        :param xpath: XPATH del boton
        :param tag_inicial: Selenium WebElement desde el cual buscar el xpath
        """
        tag_inic = self.driver if tag_inicial is None else tag_inicial

        try:
            # Busco tag del boton segun el XPATH
            boton = WebDriverWait(tag_inic, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Intento hacer click en boton
            try:
                boton.click()

            # Si falla el click convencional
            except ElementClickInterceptedException:

                # Intento hacer click en boton suponiendo que esta desarrollado en JavaScript
                try:
                    self.driver.execute_script("arguments[0].click()", boton)  # Intento con execute_script por si es con JS
                except:
                    return f"Fallo el click en el boton {xpath}"

        except TimeoutException:  # Saque NoSuchElementException puesto que es cuando no hay WebDriverWait
            return f"No se encontro el boton en {xpath}"


    def extract_tag(self, xpath, tag_inicial=None, attribute=None, text=False, sec_wait=5):  # Le falta 1) la posibilidad de haya mas de un xpath posible
        """
        Extrae texto de un tag
        :param xpath: XPATH del tag del cual extraer datos
        :param tag_inicial: Selenium Web Element desde el cual se busca el xpath
        :param attribute: String con el nombre del atributo a extraer del tag
        :param text: True para extraer texto del tag
        :return: String. En caso que falle la extraccion, None
        """
        tag_inic = self.driver if tag_inicial is None else tag_inicial  # Tag desde el que buscar el xpath

        try:
            tag_res = WebDriverWait(tag_inic, sec_wait).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return tag_res.text if text is True else tag_res.get_attribute(attribute) if attribute is not None else tag_res

        except TimeoutException:  # NoSuchElementException se usa cuando no hay WebDriverWait
            print(f"Fallo la extraccion del campo. Probablemente no exista el xpath {xpath}")
            return None

    def extract_tags(self, xpath, tag_inicial=None, sec_wait=5):
        """
        Encuentra todos los tags segun el xpath
        :param xpath: XPATH de los tags
        :return: Lista de tags, en caso contrario, None
        """
        tag_inic = self.driver if tag_inicial is None else tag_inicial  # Tag desde el que buscar el xpath

        try:
            return WebDriverWait(tag_inic, sec_wait).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        except TimeoutException:
            print(f"Fallo la extraccion de tags. Probablemente no exista el xpath {xpath}")
            return None

    # Forma 1: Boton aceptar cookies OCULT0 en tag #shadow-root
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
        self.click_boton(tag_inicial=shadow_root, xpath=xpath_boton)

    # Forma 2: Boton aceptar cookies OCULT0 en tag #document
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

    def login_website(self, user, password, xpath_user, xpath_pass, xpath_boton_login, xpath_boton_validate_user=None):
        """
        Login website
        """
        # Busco tag input para el usuario y escribo el usuario
        user_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_user)))
        user_input.send_keys(user)

        # Si hay que validar el usuario
        if xpath_boton_validate_user is not None:

            # Localizo el boton que valida el usuario y lo clickeo
            self.click_boton(xpath=xpath_boton_validate_user)

        # Busco tag input para la pass y escribo la pass
        pass_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_pass)))
        pass_input.send_keys(password)

        # Localizo el boton "Iniciar sesion" y lo clickeo
        self.click_boton(xpath=xpath_boton_login)

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

    def translate_text(self, text, source, destin):
        """
        Traduce el texto pasado como parametro del lenguaje de entrada al de salida.
        :param text: String. Texto a traducir
        :param source: String. Lenguaje de entrada.
        :param destin: String. Lenguaje de salida.
        :return: String. Texto traducido
        """
        # Definicion de variables
        translator = Translator()
        CANT_FALLAS_MAX = 10

        # Hago x intentos de traduccion (a veces falla a la primera y lo hace bien despues)
        for i in range(CANT_FALLAS_MAX):

            # Intento traducir
            try:
                return translator.translate(text, src=source, dest=destin).text
            except:
                print(f"Falló traducción Nº{i + 1}")
                sleep(random.uniform(0.5, 1.5))
        return text
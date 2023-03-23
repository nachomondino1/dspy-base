# Importo librerias
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule  # CrawlSpider --> crawling horizontal y vertical. Spider --> sin paginacion
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose  # Para poder editar lo que extraje del XPATH


# SE CORRE POR TERMINAL...
# 1) Vas al cd donde esta el .py
# 2) 'scrapy runspider <nombre_archivo>.py - o <nombre_archivo_de_salida>.xlsx -t xlsx

class NameItem(Item):

    # Campos a extraer del item
    field1 = Field()
    field2 = Field()

class SiteSpider(CrawlSpider):

    name = "spider"  # nombre del spider
    l_start_url = ["<site_url>"]  # Lista de url semilla
    l_allowed_domains = ["(e.g. airbnb.com)"]  # evitar que spider se vaya a otros dominios (e.g. publicidades)

    rules = (
        # Crawling Horizontal
        Rule(LinkExtractor(allow=r'<reg_expression>')),  # Definir expresion regular para visitar los links de las paginas de paginacion

        # Crawling Vertical
        Rule(LinkExtractor(allow=r'<reg_expression>'), callback='parse_items')  # Definir expresion regular para visitar los links de los items
    )

    def parse_items(self, response):
        """
        :param response: respuesta del sitio en formato XML
        :return:
        """
        # Lo convierto en objeto de clase Item loader
        item = ItemLoader(NameItem(), response)

        # Extraigo fields
        item.add_xpath('field1', 'XPATH_field1')  # el texto se obtiene al final del XPATH con '/text()'
        item.add_xpath('field2', 'XPATH_field2')  # puedo usar MapCompose() como argumento con una lambda function

        # Escribe en salida cada uno de los campos del item
        yield item.load_item()
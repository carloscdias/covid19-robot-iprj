# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from RISparser import read
from ..items import WebPostItem
from langdetect import detect

class WhoIntSpider(scrapy.Spider):
    name = 'WhoInt'
    allowed_domains = ['www.who.int', 'search.bvsalud.org']
    start_urls = ['https://www.who.int/emergencies/diseases/novel-coronavirus-2019/global-research-on-novel-coronavirus-2019-ncov/']
    
    def parse(self, response):
        # link para a página de busca
        search_page = response.css('a[aria-label="Search WHO COVID-19 Database"]::attr(href)').get()

        # parâmetros para baixar os resultados da pesquisa num formato simplificado
        # optou-se por ris ao invés de csv porque em csv os dados são entregues incompletos
        params = {
                'output': 'ris',
                'count': -1,
        }
        download_url = '{}?{}'.format(search_page, urlencode(params))
        self.logger.info('Assembled download url: ' + download_url)

        yield response.follow(download_url, callback = self.parse_file)

    def parse_file(self, response):
        data = self.fix_ris_data(response.text.splitlines())

        for entry in read(data):
            items = WebPostItem()

            titulo = entry.get('title')
            
            if titulo != '':
                items['titulo'] = titulo
            else:
                continue

            if entry.get('language') == '':
                idioma = detect(titulo)
            else:
                idioma = entry.get('language')

            if idioma == 'en' or idioma == 'es' or idioma == 'pt':
                items['idioma'] = idioma
            else:
                continue

            if entry.get('abstract') == None:
                items['resumo'] = ''
            else:
                items['resumo'] = entry.get('abstract')

            items['fonte'] = 'https://search.bvsalud.org/global-literature-on-novel-coronavirus-2019-ncov/resource/en/' + entry.get('id')

            if entry.get('authors') == None:
                items['autores'] = ''
            else:
                items['autores'] = entry.get('authors')

            if entry.get('url') == None:
                items['link_externo'] = ''
            else:
                items['link_externo'] = entry.get('url')

            if entry.get('journal_name') == None: 
                items['jornal'] = ''
            else:
                items['jornal'] = entry.get('journal_name')           

            yield items


    # o leitor de ris precisa que a entrada que finaliza a saída
    # contenha um espaço depois do caracter '-', caso contrário, o
    # arquivo é recusado esta função corrige o output do site
    def fix_ris_data(self, text_lines):
        return list(map(lambda x: x if x != 'ER  -' else 'ER  - ', text_lines))


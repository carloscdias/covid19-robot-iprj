import scrapy
import json
from csv import DictReader
from app.models import Novidade, PortalBusca, Credibilidade 
from scrapping.items import WebPostItem
from langdetect import detect

class CovidSearchDoctorEvidenceSpider(scrapy.Spider):
    name = 'CovidSearchDoctorEvidence'
    allowed_domains = ['covid-search.doctorevidence.com']
    start_urls = ['https://covid-search.doctorevidence.com/']
    download_timeout = 999999999999

    def parse(self, response):
        # variável que armazena os dados do usuário
        auth_pattern = r'\bvar\s+userProfile\s*=\s*(\{.*?\})\s*;\n'
        # variável que armazena os dados de busca exibidos na página
        signals_pattern = r'\bvar\s+signals\s*=\s*(\[\{.*?\}\])\s*;'
        
        # Para fazer o download do conteúdo, precisamos passar um cookie com o
        # token dessa variável
        auth = response.css('script[type="text/javascript"]').re_first(auth_pattern)
        auth_token = json.loads(auth)['auth-token']

        json_data = response.css('script[type="text/javascript"]').re_first(signals_pattern)
        for el in json.loads(json_data):
            query = el['query']['query/normalized-blunt']
            # Download dos dados em csv da query obtida na página de busca
            yield scrapy.Request(
                    url = 'https://covid-search.doctorevidence.com/api/articles/export',
                    method = 'post',
                    body = '["^ ","~:blunt","{}","~:format","csv","~:order","new","~:order-direction","desc","~:limit",{}]'.format(query, self.limit if hasattr(self, 'limit') else 1048576),
                    cookies = { '.ASPXAUTHSSO': auth_token },
                    callback = self.parse_file,
                    headers = { 'content-type': 'application/transit+json' },
            )

    def parse_file(self, response):
        for item in DictReader(response.text.splitlines()):
            items = WebPostItem()
            dic = dict(item)

            titulo = dic['Title']
            if titulo != '':
                items['titulo'] = titulo
            else:
                continue

            idioma = detect(dic['Title'])
            if idioma == 'en' or idioma == 'es' or idioma == 'pt':
                items['idioma'] = idioma
            else:
                continue     

            items['resumo'] = dic['Abstract']
            items['fonte'] = dic['DocSearch url']
            items['autores'] = dic['All Authors']
            items['link_externo'] = dic['Url']
            items['categoria'] = dic['Category']
            items['data_publicacao'] = dic['Published date']
           
            yield items

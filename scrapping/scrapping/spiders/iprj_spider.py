import scrapy

from app.models import WebPost
from scrapping.items import WebPostItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from urllib.parse import urljoin

class WebPanelSpider(scrapy.Spider):
    """
    Esta classe define um spider para realizar os scrapes dos posts do site do IPRJ
    """
    name = "iprj"
    allowed_domains = ["iprj.uerj.br"]
    start_urls = (
        "http://www.iprj.uerj.br/",
        )

    Rules = (
        Rule(
            LinkExtractor(
                allow=(),
                restrict_xpaths=('//a[@title="Próximo"]',)
                ),
            callback="parse",
            follow= True
            ),
        )

    def parse(self, response):
        for idx, article in enumerate(response.xpath('//article')):
            item = WebPostItem()
            title = article.xpath('.//header/h2/a/text()').extract_first()
            item['title'] = title
            
            yield item
            
        # Verifica se possui mais páginas
        next_page = response.xpath('//a[@title="Próximo"]/@href').extract_first()
        next_page = urljoin(self.start_urls[0], next_page)
        # Verifica se é a última página (evita entradas repetidas)
        is_disabled = response.xpath('//li[@class="disabled"]/a/text()').extract_first()
        if next_page and not(is_disabled == 'Próximo'):
            request = scrapy.Request(next_page)
            yield request
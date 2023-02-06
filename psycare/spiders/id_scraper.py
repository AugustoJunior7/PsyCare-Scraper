# -*- coding: utf-8 -*-

# Scraper responsável por coletar o link da página de todos os psicólogos
import scrapy


class spider(scrapy.Spider):
    name = 'psy_id_spider'
    allowed_domains = ['www.psych.on.ca']
    start_urls = ['https://www.psych.on.ca/Public/Find-a-Psychologist']

    def parse(self, response):
        psy_ids = response.css(
            '.fap-desktop-view ::attr(href)').extract()  # Coleta os ids de todos os psicólogos da página atual

        for id in psy_ids:
            yield {
                # Monta o link da página de cada psicólogo a partir do id
                'page': "https://www.psych.on.ca/Public/" + str(id)
            }

        next_page = response.css(
            '.events_listing_pager_container_inner a ::attr(href)').extract()[-1]  # Coleta o link da próxima página
        if next_page:
            yield scrapy.Request(response.urljoin(next_page),
                                 callback=self.parse)

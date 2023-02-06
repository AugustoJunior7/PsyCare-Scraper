# -*- coding: utf-8 -*-

# Scraper responsável por coletar os dados de cada psicólogo
import scrapy
import csv


class spider(scrapy.Spider):
    name = 'psy_info_spider2'
    allowed_domains = ['www.psych.on.ca/']

    # Faz a leitura do arquivo com o link da página de cada psicólogo
    csvfile = open('PsychologistsID.csv', mode='r')
    csvreader = csv.reader(csvfile)
    start_urls = []

    # Define as urls que serão percorridas
    for i in csvreader:
        start_urls.append(i[0])
    del start_urls[0]

    def parse(self, response):

        # Coleta de informações básica como nome, contato e endereço
        psy_name = response.css('.name::text').extract()

        psy_contact = response.css(
            '.contact-information > .address_container > .info::text').extract()[-1]

        psy_address = response.css(
            '.contact-information > .address_container > .info::text').extract()[0]

        counter = 0

        # Coleta e modelagem dos dados dos psicólogos (como área de atuação e linguagem do serviço ofertado)
        # Nesse modelo são selecionados todos os psicólogos, inclusive os que não preencheram todos os campos
        # No caso do não preenchemento, os dados são deixados como 'Null'
        try:
            psy_sliding_scale = response.css(
                '.professional-information > .info::text').extract()[counter]
            if psy_sliding_scale == 'Yes' or psy_sliding_scale == 'No':
                counter += 1
            else:
                psy_sliding_scale = None
        except:
            psy_sliding_scale = None

        try:
            psy_age_group = response.css(
                '.professional-information > .info::text').extract()[counter]
            if psy_age_group == 'Yes' or psy_age_group == 'No':
                psy_age_group = None
            else:
                counter += 1
        except:
            psy_age_group = None

        try:
            psy_remote_assessment = response.css(
                '.professional-information > .info::text').extract()[counter]
            if psy_remote_assessment == 'Yes' or psy_remote_assessment == 'No':
                counter += 1
            else:
                psy_remote_assessment = None
        except:
            psy_remote_assessment = None

        try:
            psy_area_practice = response.css(
                '.professional-information > .info::text').extract()[counter]
            counter += 1
        except:
            psy_area_practice = None

        try:
            psy_service_language = response.css(
                '.professional-information > .info::text').extract()[counter]
            if ('English' in psy_service_language) or ('French' in psy_service_language):
                counter += 1
            else:
                psy_service_language = None
                counter += 1
        except:
            psy_service_language = None

        try:
            psy_problem_area = response.css(
                '.professional-information > .info::text').extract()[counter]
            counter += 1
        except:
            psy_problem_area = None

        yield {
            'name': psy_name,
            'contact': psy_contact,
            'address': psy_address,
            'sliding scale': psy_sliding_scale,
            'age group': psy_age_group,
            'remote assessment': psy_remote_assessment,
            'area of practice': psy_area_practice,
            'service language': psy_service_language,
            'problema area': psy_problem_area
        }

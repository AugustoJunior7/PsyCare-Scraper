# -*- coding: utf-8 -*-

# Scraper responsável por coletar os dados de cada psicólogo
import scrapy
import csv


class spider(scrapy.Spider):
    name = 'psy_info_spider'
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

        # Coleta e modelagem dos dados dos psicólogos (como área de atuação e linguagem do serviço ofertado)
        # Nesse modelo são selecionados apenas os psicólogos que preencheram todas as informações
        try:
            psy_sliding_scale = response.css(
                '.professional-information > .info::text').extract()[0]
        except:
            print('Erro: Psicólogo não preencheu este campo')

        try:
            psy_age_group = response.css(
                '.professional-information > .info::text').extract()[1]
        except:
            print('Erro: Psicólogo não preencheu este campo')

        try:
            psy_remote_assessment = response.css(
                '.professional-information > .info::text').extract()[2]
        except:
            print('Erro: Psicólogo não preencheu este campo')

        try:
            psy_area_practice = response.css(
                '.professional-information > .info::text').extract()[3]
        except:
            print('Erro: Psicólogo não preencheu este campo')

        try:
            psy_service_language = response.css(
                '.professional-information > .info::text').extract()[4]
        except:
            print('Erro: Psicólogo não preencheu este campo')

        try:
            psy_problem_area = response.css(
                '.professional-information > .info::text').extract()[5]
        except:
            print('Erro: Psicólogo não preencheu este campo')

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

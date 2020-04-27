# -*- coding: utf-8 -*-
import scrapy
import re
from getResults import GetResults
import json



class KompasSpider(scrapy.Spider):
    name = 'kompas'
    start_urls = ['https://www.kompas.com/']
    custom_settings = {
        'LOG_ENABLED': False,
    }

    def parse(self, response):
        for title in response.css("a.article__link"):
            original_title = str(title.css("a.article__link::text").getall())
            new_title = "".join(re.findall("[A-Za-z0-9/-]+|[0-9]*\s", original_title))
            link = str(title.css("a.article__link::attr(href)").getall())
            new_link = re.sub("\['|'\]", "", link)

            # Find that damned newline and newtab character
            empty_title = re.match("nt+\s", new_title)
            if not empty_title:
                parsed = {
                    'source': 'Kompas',
                    'title': new_title,
                    'link': new_link
                }
                covid_related = re.search("COVID-19|Covid-19|Corona|Pandemi|Virus", new_title)
                GetResults.get_covid_news(parsed) if covid_related else GetResults.get_general_news(parsed)
                splitted_words = re.split('\s+', new_title)
                GetResults.append_temp(splitted_words)


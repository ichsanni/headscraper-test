# -*- coding: utf-8 -*-
import scrapy
import re
from getResults import GetResults


class CNBCSpider(scrapy.Spider):
    name = 'cnbc'
    start_urls = ['https://www.cnbcindonesia.com/indeks']
    custom_settings = {
        'LOG_ENABLED': False,
    }

    def parse(self, response):
        for title in response.css("li article"):
            original_title = str(title.css("a div.box_text h2::text").getall())
            new_title = "".join(re.findall("[A-Za-z0-9/-]+|[0-9]*\s", original_title))
            link = str(title.css("a::attr(href)").getall())
            new_link = re.sub("\['|'\]", "", link)

            if new_title:
                parsed = {
                    'source': 'CNBC Indonesia',
                    'title': new_title,
                    'link': new_link
                }
                GetResults.get_news(parsed)
                splitted_words = re.split('\s+', new_title)
                GetResults.append_temp(splitted_words)

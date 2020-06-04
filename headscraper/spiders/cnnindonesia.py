# -*- coding: utf-8 -*-
import scrapy
import re
from getResults import GetResults


class CNNSpider(scrapy.Spider):
    name = 'cnn'
    start_urls = ['https://www.cnnindonesia.com/']
    custom_settings = {
        'LOG_ENABLED': False,
    }

    def parse(self, response):
        for title in response.css("article"):
            original_title = str(title.css("a span.box_text h2.title::text").getall())
            new_title = "".join(re.findall("[A-Za-z0-9/-]+|[0-9]*\s", original_title))
            link = str(title.css("a::attr(href)").getall())
            new_link = re.sub("\['|'\]", "", link)

            if new_title:
                parsed = {
                    'source': 'CNN Indonesia',
                    'title': new_title,
                    'link': new_link
                }
                GetResults.get_news(parsed)
                splitted_words = re.split('\s+', new_title)
                GetResults.append_temp(splitted_words)

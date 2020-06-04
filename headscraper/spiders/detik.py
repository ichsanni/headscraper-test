# -*- coding: utf-8 -*-
import scrapy
import re
import json
from getResults import GetResults


class DetikSpider(scrapy.Spider):
    name = 'detik'
    start_urls = ['https://www.detik.com/']
    custom_settings = {
        'LOG_ENABLED': False,
    }

    def parse(self, response):
        for title in response.css("article.ph_newsfeed_d"):
            original_title = str(title.css("div.ai_replace_title::text").getall())
            new_title = "".join(re.findall("\s[A-Za-z0-9-]+|[0-9]*", original_title))
            link = str(title.css("article.ph_newsfeed_d::attr(i-link)").getall())
            new_link = re.sub("\['|'\]", "", link)

            parsed = {
                'source': 'Detik',
                'title': new_title,
                'link': new_link
            }
            GetResults.get_news(parsed)
            splitted_words = re.split('\s+', new_title)
            GetResults.append_temp(splitted_words)

import datetime, time
from spiders import kompas, detik, cnnindonesia, cnbc
from scrapy.crawler import CrawlerProcess
import shutil, os.path, json
from getResults import GetResults



class CrawlTheWebsite():
    def __init__(self):
        # terminal query : scrapy crawl detik
        d = datetime.datetime.today()
        dir_date = str(d.year) + "-" + str(d.month) + "-" + str(d.day)
        file_name = dir_date + "-" + str(d.hour) + str(d.minute)
        self.check_file(file_name, dir_date)

    def start_scraping(self):
        gr = GetResults()
        process = CrawlerProcess()
        process.crawl(kompas.KompasSpider)
        process.crawl(cnnindonesia.CNNSpider)
        process.crawl(cnbc.CNBCSpider)
        process.crawl(detik.DetikSpider)
        process.start()
        gr.count_words()
        gr.dump_json()

    def check_file(self, file_name, dir_date):
        file_name += ".json"
        latest = "latest.json"
        # check if day has changed
        if not os.path.isdir(dir_date):
            os.mkdir(dir_date)
            try:
                shutil.copy(latest, dir_date + "/" + file_name)
                os.remove(latest)
            except FileNotFoundError:
                with open(latest, 'w') as first_json:
                    dummy = {'title': 'none'}
                    json.dump(dummy, first_json)
                    first_json.close()

        if os.path.isfile(latest):
            shutil.copy(latest, dir_date + "/" + file_name)

        self.start_scraping()

CrawlTheWebsite()

# to run the crawler:
# python3 crawlTheWebsite.py

# to run a local server:
# 1. enter the wanted directory
# 2. python -m http.server

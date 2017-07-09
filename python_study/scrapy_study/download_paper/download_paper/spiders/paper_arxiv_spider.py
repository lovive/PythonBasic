# -*- coding: utf-8 -*-
import scrapy


class PaperArxivSpiderSpider(scrapy.Spider):
    name = "paper_arxiv_spider"
    allowed_domains = ["https://arxiv.org/"]
    start_urls = ['http://https://arxiv.org//']

    def parse(self, response):
        pass

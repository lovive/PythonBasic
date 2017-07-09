# -*- coding: utf-8 -*-

"""
    Author: zmgao
    version: 1.0
    date: 2017/07/07
    name: obtaining the air quality of china city

"""

import scrapy
from air_quality.items import AirQualityItem
from urllib import parse

base_url = "https://www.aqistudy.cn/historydata/"


class AqiHistorySpider(scrapy.Spider):
    name = "aqi_history_spider"
    allowed_domains = ["aqistudy.cn"]
    start_urls = ['https://www.aqistudy.cn/historydata/index.php/']

    def parse(self, response):
        """
            解析初始的页面

        """

        # 获取所有城市的URL
        city_url_list = response.xpath('//div[@class="all"]//div[@class="bottom"]//a//@href')

        for city_url in city_url_list:
            # 依次遍历城市的URL
            city_month_url = base_url + city_url.extract()
            # 解析每个城市的月份数据
            request = scrapy.Request(city_month_url, callback=self.parse_city_month)
            yield request

    def parse_city_month(self, response):
        """
            解析该城市的月份数据

        """
        # 获取该城市的所有月份URL
        month_url_list = response.xpath('//table[@class="table table-condensed table-bordered table-striped '
                                        'table-hover table-responsive"]//tr//a//@href')

        for month_url in month_url_list:
            # 依次遍历月份的URL
            city_day_url = base_url + month_url.extract()
            # 解析该城市的每日数据
            request = scrapy.Request(city_day_url, callback=self.parse_city_day)
            yield request

    def parse_city_day(self, response):
        """
            解析该城市每日的数据

        """

        url = response.url
        item = AirQualityItem()
        city_url_name = url[url.find('=')+1:url.find('&')]

        # 解析url中中文
        item['city_name'] = parse.unquote(city_url_name)

        # 获取每日记录
        day_record_list = response.xpath('//table[@class="table table-condensed table-bordered table-striped '
                                         'table-hover table-responsive"]//tr')
        for i,day_record in enumerate(day_record_list):
            if i == 0:  # 跳过表头
                continue

            td_list = day_record.xpath('.//td')
            item['record_date'] = td_list[0].xpath('text()').extract_first()             # 检测日期
            item['aqi_val'] = td_list[1].xpath('text()').extract_first()                 # AQI
            item['quality_level'] = td_list[2].xpath('.//div/text()').extract_first()    # 质量等级
            item['pm2_5_val'] = td_list[3].xpath('text()').extract_first()               # PM2.5
            item['pm10_val'] = td_list[4].xpath('text()').extract_first()                # PM10
            item['so2_val'] = td_list[5].xpath('text()').extract_first()                 # SO2
            item['co_val'] = td_list[6].xpath('text()').extract_first()                  # CO
            item['no2_val'] = td_list[7].xpath('text()').extract_first()                  # NO2
            item['o3_val'] = td_list[8].xpath('text()').extract_first()                  # O3
            item['rank'] = td_list[9].xpath('text()').extract_first()                   # 排名

            yield item

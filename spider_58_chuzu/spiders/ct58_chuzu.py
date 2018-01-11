# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from traceback import format_exc
from ..items import XiaoquInfoItem, ZufangInfoItem
from ..utils.parser import (parse, parse_xiaoqu_info, parse_ershou_price_list,
                            parse_zufang_detail_url, parse_zufang_info)


class Ct58ChuzuSpider(Spider):
    name = 'ct58_chuzu'
    allowed_domains = ['58.com']
    xiaoqu_url_format = 'http://{0}/xiaoqu/{1}/'
    host = 'cd.58.com'
    codes = [115, 116, 117]
    # codes = list()

    def start_requests(self):  # 重写start_urls, start_requests
        start_urls = [self.xiaoqu_url_format.format(self.host, code) for code in self.codes]

        for url in start_urls:
            yield Request(url)

    def parse(self, response):
        url_list = parse(response)

        for url in url_list:
            yield Request(url,
                          callback=self.parse_xiaoqu_info,
                          errback=self.err_back,
                          priority=4)

    def parse_xiaoqu_info(self, response):
        _ = self
        data = parse_xiaoqu_info(response)
        item = XiaoquInfoItem()
        item.update(data)
        yield item

        # 二手房
        url = 'http://{}/xiaoqu/{}/ershoufang/pn_1/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.parse_ershou_price_list,
                      errback=self.err_back,
                      mata={'id': item['id']},
                      priority=3)

        # 出租房
        url_ = 'http://{}/xiaoqu/{}/chuzu/pn_1/'.format(self.host, item['id'])
        yield Request(url_,
                      callback=self.parse_zufang_detail_url,
                      errback=self.err_back,
                      mata={'id': item['id']},
                      priority=2)

    def parse_ershou_price_list(self, response):
        _ = self
        price_list = parse_ershou_price_list(response)
        yield {'id': response.meta['id'],
               'price_list': price_list}

    def parse_zufang_detail_url(self, response):
        _ = self
        url_list = parse_zufang_detail_url(response)

        for url in url_list:
            yield response.request.replace(url=url,
                                           callback=self.parse_zufang_info,
                                           priority=1)

    def parse_zufang_info(self, response):
        _ = self
        data = parse_zufang_info(response)
        item = ZufangInfoItem()
        item.update(data)
        item['id'] = response.mata['id']
        item['url'] = response.url
        yield item

    def err_back(self, e):
        _ = e
        self.logger.error(format_exc())  # 打出报错信息

# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..utils.parser import (parse, xiaoqu_parse,
                            get_ershou_price_list,
                            get_chuzu_house_info,
                            chuzu_list_pag_get_detail_url)
from ..items import (City58Item,
                     City58ItemXiaoqu,
                     City58ItemXiaoquChuzuInfo)
from traceback import format_exc


class SpiderCity58Spider(scrapy.Spider):
    name = 'ct58_chuzu'
    allowed_domains = ['58.com']
    host = 'cd.58.com'
    xiaoqu_url_format = 'http://{}/xiaoqu/{}/'
    # xiaoqu_code = list()
    xiaoqu_code = list(range(103, 118))
    xiaoqu_code.append(21611)

    def start_requests(self):  # 重写start_requests函数
        start_url = [self.xiaoqu_url_format.format(self.host, code) for code in self.xiaoqu_code]
        for url in start_url:
            yield Request(url)

    def parse(self, response):
        """
        第一步抓取所有小区
        http://cd.58.com/xiaoqu/21611/
        :param response:
        :return:
        """

        url_list = parse(response)  # 调用utils.parse中的parse方法，得到所有小区的url

        for url in url_list:
            yield Request(url,
                          callback=self.xiaoqqu_detail_pag,
                          errback=self.error_back,
                          priority=4)

    def xiaoqqu_detail_pag(self, response):
        """
        第二步抓取小区详情页信息
        http://cd.58.com/xiaoqu/shenxianshudayuan/
        :param response:
        :return:
        """
        _ = self
        data = xiaoqu_parse(response)
        item = City58Item()
        item.update(data)
        item['id'] = response.url.split('/')[4]
        yield item

        # 二手房
        url = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.ershoufang_list_pag,
                      errback=self.error_back,
                      mata={'id': item['id']},
                      priority=3)

        # 出租房
        url_ = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host, item['id'])
        yield Request(url_,
                      callback=self.chuzu_list_pag,
                      errback=self.error_back,
                      mata={'id': item['id']},
                      priority=2)

    def ershoufang_list_pag(self, response):
        """
        第三步抓取二手房详情页信息
        http://cd.58.com/xiaoqu/shenxianshudayuan/ershoufang/
        :param response:
        :return:
        """

        _ = self
        price_list = get_ershou_price_list(response)
        yield {'id': response.meta['id'], 'price_list': price_list}

    def chuzu_list_pag(self, response):
        """
        第四步抓取出租房详情页url
        http://cd.58.com/xiaoqu/shenxianshudayuan/chuzu/
        :param response:
        :return:
        """

        _ = self
        url_list = chuzu_list_pag_get_detail_url(response)

        for url in url_list:
            yield response.request.replace(url=url,
                                           callback=self.chuzu_detail_pag,
                                           priority=1)
            # yield Request(url, callback=)

    def chuzu_detail_pag(self, response):
        """
        第五步抓取出租房详情页信息
        :param response:
        :return:
        """

        _ = self
        data = get_chuzu_house_info(response)
        item = City58ItemXiaoquChuzuInfo()
        item.update(data)
        item['id'] = response.mata['id']
        item['url'] = response.url
        yield item

    def error_back(self, e):
        _ = e
        self.logger.error(format_exc())  # 打出报错信息

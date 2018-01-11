# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq


def parse(response):
    """
    url_ = 'http://cd.58.com/xiaoqu/115/'
    返回列表页所有的小区urls
    :param response:
    :return:
    """

    doc = pq(response.text)
    a_list = doc('tr > td.info > ul > li.tli1 > a.t').items()
    result = [a.attr('href') for a in a_list]
    result = set(result)  # 去重
    return result


def parse_xiaoqu_info(response):
    """
    url_ = 'http://cd.58.com/xiaoqu/jinhaiantianfuhuayuanshuicheng/'
    返回这个小区的详细信息的dict字典
    主要信息包括小区名称，小区参考房价，小区地址，小区建筑年代
    :param response:
    :return:
    """

    result = dict()
    doc = pq(response.text)
    result['id'] = response.url.split('/')[4]
    result['name'] = doc('.xiaoquh1').text()
    result['reference_price'] = doc('.moneyColor').text()
    result['address'] = doc('.bhrInfo > dd:nth-child(3) > span:nth-child(3)').text().split()[0]
    result['times'] = doc('.bhrInfo > dd:nth-child(5)').text().split()[2]
    return result


def parse_ershou_price_list(response):
    """
    url_ = 'http://cd.58.com/xiaoqu/jinhaiantianfuhuayuanshuicheng/ershoufang/pn_1/'
    匹配二手房列表页面的所有房价信息
    返回一个价格的列表list
    :param response:
    :return:
    """

    doc = pq(response.text)
    price_tag = doc('td.tc > span:nth-child(3)').text().split()
    price_list = [i[:-3] for i in price_tag]
    return price_list


def parse_zufang_detail_url(response):
    """
    url_ = 'http://cd.58.com/xiaoqu/jinhaiantianfuhuayuanshuicheng/chuzu/'
    获取出租列表页所有详情页url
    返回一个url的列表list
    :param response:
    :return:
    """

    doc = pq(response.text)
    a_list = doc(' tr > td.t > a.t').items()
    url_list = [a.attr('href') for a in a_list]
    return url_list


def parse_zufang_info(response):
    """
    url_ = 'http://cd.58.com/zufang/32699406202930x.shtml'
    返回一个dict包含：出租页标题，出租价格，房屋面积，房屋类型（几室几厅）
    :param response:
    :return:
    """

    result = dict()
    doc = pq(response.text)
    result['name'] = doc('h1.c_333').text()
    result['zu_price'] = doc('.f36').text()
    result['type'] = doc('ul.f14 > li:nth-child(2) > span:nth-child(2)').text().split()
    result['type'], result['area'], *_ = result['type']
    return result


if __name__ == '__main__':
    import requests
    from pprint import pprint

    url_ = 'http://cd.58.com/xiaoqu/jinhaiantianfuhuayuanshuicheng/'
    response_ = requests.get(url_)
    result_ = parse_xiaoqu_info(response_)
    pprint(result_)

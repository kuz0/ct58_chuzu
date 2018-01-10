# -*- coding: utf-8 -*-
from pyquery import PyQuery


def parse(response):
    """
    抓取小区列表页面: http://cd.58.com/xiaoqu/11487/
    返回列表页所有的小区url
    :param:response
    :return
    """

    result = set()  # result为set集合（不允许重复元素）
    d = PyQuery(response.text)
    tr_list = d('#infolist div.listwrap table.tbimg tbody tr').items()

    for tr in tr_list:
        url = tr('td.info ul li.tli1 a.t').attr('href')  # 爬取各个小区的url
        result.add(url)

    return result


def xiaoqu_parse(response):
    """
    小区详情页匹配代码的样例url: http://cd.58.com/xiaoqu/shenxianshudayuan/
    返回这个小区的详细信息的dict字典，主要信息包括小区名称，小区参考房价，小区地址，小区建筑年代
    :param:response
    :return:
    """

    result = dict()
    d = PyQuery(response.text)
    result['name'] = d('html body div.bodyItem.bheader div.fr.bhright h1.xiaoquh1').text()
    result['reference_price'] = d('html body div.bodyItem.bheader div.fr.bhright dl.bhrInfo dd span.moneyColor').text()
    result['address'] = (d('html body div.bodyItem.bheader div.fr.bhright dl.bhrInfo'
                           ' dd span.ddinfo').text())
    result['times'] = d('html body div.bodyItem.bheader div.fr.bhright dl.bhrInfo dd').eq(4).text().split()
    result['times'] = result['times'][2]  # 取出建筑年代
    return result


def get_ershou_price_list(response):
    """
    页面链接样例: http://cd.58.com/xiaoqu/shenxianshudayuan/ershoufang/
    匹配二手房列表页面的所有房价信息
    返回一个价格的列表list
    :param:response
    :return:
    """

    d = PyQuery(response.text)
    price_tag = d('td.tc > span:nth-child(3)').text().split()
    price_tag = [i[:-3] for i in price_tag]   # 遍历price_tag截取到倒数第三个元素
    return price_tag


def chuzu_list_pag_get_detail_url(response):
    """
    页面链接样例: http://cd.58.com/xiaoqu/shenxianshudayuan/chuzu/
    获取出租列表页所有详情页url
    返回一个url的列表list
    :param:response
    :return:
    """
    d = PyQuery(response.text)
    a_list = d('tr > td.t > a.t').items()
    url_list = [a.attr('href') for a in a_list]  # 遍历a_list
    return url_list


def get_chuzu_house_info(response):
    """
    获取出租详情页的相关信息: http://cd.58.com/zufang/32457743416625x.shtml
    返回一个dict包含：出租页标题，出租价格，房屋面积，房屋类型（几室几厅）
    :param:response
    :return:
    """

    result = dict()
    d = PyQuery(response.text)
    result['name'] = d('html body div.main-wrap div.house-title h1.c_333.f20').text()
    result['zu_price'] = (d('html body div.main-wrap div.house-basic-info div.house-basic-right.fr div.house-basic-desc'
                            ' div.house-desc-item.fl.c_333 div.house-pay-way.f16 span.c_ff552e b.f36').text())
    result['type'] = (d('html body div.main-wrap div.house-basic-info div.house-basic-right.fr div.house-basic-desc'
                        ' div.house-desc-item.fl.c_333 ul.f14 li:nth-child(2) span:nth-child(2)').text()).split()
    result['type'], result['mianji'], *_ = result['type']
    return result


if __name__ == '__main__':
    import requests
    from pprint import pprint
    r = requests.get('http://cd.58.com/xiaoqu/shenxianshudayuan/')
    s = xiaoqu_parse(r)
    pprint(s)

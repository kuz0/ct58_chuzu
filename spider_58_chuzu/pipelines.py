# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from traceback import format_exc
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import DropItem
from spider_58_chuzu.items import XiaoquInfoItem, ZufangInfoItem


class Ct58Pipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @ classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.setting.get('MONGO_URI'),
                   mongo_db=crawler.setting.get('MONGO_DB'))

    def open_spider(self, spider):
        _ = spider
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['xiaoqu_info'].ensure_index('id', unique=True)  #
        self.db['zufang_info'].ensure_index('url', unique=True)

    def close_spider(self, spider):
        _ = spider
        self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, XiaoquInfoItem):
                self.db['xiaoqu_info'].update({'id': item['id']}, {'$set': item}, upsert=True)
            elif isinstance(item, ZufangInfoItem):
                try:
                    fangjia = HandleFangjiaPipeline.price_per_square_meter_dict[item['id']]
                    item['price_per'] = fangjia
                    self.db['zufang_info'].update({'url': item['url']}, {'$set': item}, upsert=True)
                except Exception as e:
                    print(e)
        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')
        except Exception as e:
            _ = e
            spider.logger.error(format_exc())
        return item


class HandleZuFangPipeline(object):

    def process_item(self, item, spider):
        _ = spider, self
        # self.db[self.collection_name].insert_one(dict(item))
        if isinstance(item, ZufangInfoItem) and 'area' in item:  # 判断进来的item是否是City58ItemXiaoChuZuQuInfo，是否含有面积参数
            item['zu_price_per'] = int(item['zu_price']) / int(item['mianji'])   # 租金除以面积得到平均价格
        return item  # 继续传递item


class HandleFangjiaPipeline(object):

    price_per_square_meter_dict = dict()  # 声明一个dict()

    def process_item(self, item, spider):
        _ = spider

        if isinstance(item, dict) and 'price_list' in item:  # 判断传进来的item是否是个字典，并且是否含有price_list
            item['price_list'] = [int(i) for i in item['price_list']]  #遍历price_list
            if item['price_list']:
                self.price_per_square_meter_dict[item['id']] = sum(item['price_list']) / len(item['price_list'])  #得到每个小区的平均价格
            else:
                self.price_per_square_meter_dict[item['id']] = 0
            raise DropItem()
        return item  # 继续传递item

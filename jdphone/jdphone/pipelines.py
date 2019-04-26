# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymysql.cursors
import json

class JdphonePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",
                                    user="yyb",
                                    passwd="123123",
                                    db="xrj",
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        name = item['title']
        price = item['price']
        url = item['url']

        sql = "INSERT INTO douban_jd(name,price,url) VALUES ('%s','%s','%s')"%(name, price,url)
        self.cur.execute(sql)
        self.conn.commit()

        print(item)

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

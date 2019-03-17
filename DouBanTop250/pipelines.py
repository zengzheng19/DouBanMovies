# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings

class Doubantop250Pipeline(object):
    '''
    将数据插入本地数据库
    '''
    def __init__(self):
        settings = get_project_settings()
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    def insert(self,item):
        sql = "insert into doubanmovies250(title,score,rank) values(%s,%s,%s)"
        query = self.dbpool.runInteraction(self._conditional_insert,sql,item)
        query.addErrback(self,self._handle_error,item,spider)
        return  item

    def _conditional_insert(self,tx,sql,item):
        tx.excute(sql,item)

    def _handle_error(self,failue,item,spider):
        print(failue)


class Pipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host='127.0.0.1',port=3306,user='root', password='zeng',charset='utf8',db='learn')

    def process_item(self, item, spider):
        select_sql = """SELECT * FROM learn"""
        usable_proxy=self.cursor.execute(select_sql)
        # 用commit（）才会提交到数据库
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


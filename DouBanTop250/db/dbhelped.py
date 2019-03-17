import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings


class DBHelper():

    def __init__(self, dbpool):
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
        sql = "insert into doubanmovies250(title,score,rank) valuse(%s,%s,%s)"
        query = self.dbpool.runInteraction(self._conditional_insert,sql,item)
        query.addErrback(self,self._handle_error,item,spider)
        return  item

    def _conditional_insert(self,tx,sql,item):
        tx.excute(sql,item)

    def _handle_error(self,failue,item,spider):
        print(failue)
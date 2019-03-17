import pymysql

class GetIP(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', port=3306, password='zeng', db='learn',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def get_random_ip(self):
        # 从数据库随机取一个可用ip
        random_sql = """
        select * from ProxyList order by rand() limit 1
        """
        result = self.cursor.execute(random_sql)
        for ip_info in self.cursor.fetchall():
            url = ip_info[0]
        print('url middleware',url)
        return url
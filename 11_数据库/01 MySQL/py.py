
import pymysql

# 连接 mysql, 并进如数据库 db1 中
db1 = pymysql.connect(
    host='127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '000',
    charset = 'utf8',
    db= 'db1'  # 链接 db1 数据库
)

c = db1.cursor() # 获取游标


#创建表
str_sql命令 = """
create table tb3(
name char(20) not null,
age int,
sex enum('male','female'),
income float
)  # 注意: python中, 写sql语句, 最后这里没有加分号
"""

c.execute(str_sql命令)















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


# #创建表
# str_sql命令 = """
# create table tb3(
# name char(20) not null,
# age int,
# sex enum('male','female'),
# income float
# )  # 注意: python中, 写sql语句, 最后这里没有加分号
# """
#
# c.execute(str_sql命令)

# # 新增数据, 必须执行 数据库(而非游标)的commit()方法. 才能增加数据成功.
# c.execute("insert into tb3 (name, age, sex, income) values('zrx',47, 'male', 5000),('wyy',22,'female',3000)")
# db1.commit()


# # 删除数据, 必须执行 commit方法
# c.execute("delete from tb3 where name='zrx'") # 删除name字段的值是'zrx'的所有数据行
# db1.commit()

# # 插入列
# #下面为现有表格tb3, 增加一列id, 作为主列, 放在第一列的位置上. 注意, 这里不需要 commit方法也能成功.
# c.execute("alter table tb3    add column   id int primary key    auto_increment     first") #FIRST表示将该列放在第一位置。AUTO_INCREMENT使该列自增。PRIMARY KEY设置为主键。
# # # 注意:某些 MySQL 版本可能要求 PRIMARY KEY在前面, 而不是写在 auto_increment 后面.
# db1.commit()

# 修改数据, 必须执行 commit方法
# c.execute("update tb3 set income = 6000 where id=2")  # 将 id=2 这一行的 income值, 改为6000
# db1.commit()

# 查询
c.execute("select * from tb3 where id>=2") #查询tb3表中, id>=2的所有行的数据
# data = c.fetchone() # 对这些数据只取出第一行
# print (data) # (2, 'wyy', 22, 'female', 6000.0)

dataAll = c.fetchall()
print(dataAll) # ((2, 'wyy', 22, 'female', 6000.0), (3, 'wyy', 22, 'female', 3000.0), (4, 'wyy', 22, 'female', 3000.0))


















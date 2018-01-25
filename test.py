import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.cursor()
data = [{"name": "binggao@cn.com", "password": "1234567"}, {"name": "bingga@cn.com", "password": "12345"},{"name": "bingao@cn.com", "password": "123567"},{"name": "bingo@cn.com", "password": "1234567"},{"name": "ggao@cn.com", "password": "1234567"},{"name": "ao@cn.com", "password": "1234567"},{"name": "bingggggao@cn.com", "password": "1234567"},{"name": "zzzzgao@cn.com", "password": "1234567"}]

for item in data:
    cursor.execute('insert into user (name,password) values (\''+item['name']+'\',\''+item['password']+'\')')
    values = cursor.fetchall()

cursor.close()

conn.commit()

conn.close()
import pandas
import csv, sqlite3
#连接数据库名称，不存在可自动生成
conn= sqlite3.connect("patients_consult.db")
#csv文件路径
df = pandas.read_csv('C:\\Users\\IBM_ADMIN\\Desktop\\sql\\description\\patients.csv')
#表名，连接，存在即追加数据，是否生成索引，默认主键字段名：rowid
df.to_sql('patients', conn, if_exists='append', index=True)
df1 = pandas.read_csv('C:\\Users\\IBM_ADMIN\\Desktop\\sql\\description\\patients_consult.csv')
df1.to_sql('patients_consult', conn, if_exists='append', index=True)
#csv同级目录生产数据库文件
print('ok')
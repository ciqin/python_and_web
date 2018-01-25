import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import sqlite3
import json
#1：首页跳转
class TestGetHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index-cohort.html")
#2：处理请求年龄和男女总人数的请求
class GenderHandler(tornado.web.RequestHandler):
	def get(self):
		connect = sqlite3.connect('patients_consult.db')
		sql_1="SELECT count(1) from patients group by gender"
		cursor=connect.execute(sql_1)
		rows=cursor.fetchall()
		boy_count=(rows[0])[0]
		girl_count=(rows[1])[0]
		#2.1:查询出男女各自总数
		#2.2:查询出年龄集合
		sql_2="SELECT age from patients"
		cursor.execute(sql_2)
		rows2=cursor.fetchall()
		list_age=[]
		for age in rows2:
			list_age.append(age[0])
		#2.3：封装成json响应请求
		result_json={}
		result_json["boy_count"] = boy_count
		result_json["girl_count"] = girl_count
		result_json["list_age"] = list_age
		self.write(json.dumps(result_json))
		#2.4:关闭数据库连接
		cursor.close()
		connect.close()
#3:请求病人总数
class CountHandler(tornado.web.RequestHandler):
	def get(self):
		#3.1:连接database
		connect = sqlite3.connect('patients_consult.db')
		#3.2:根据sql查询结果
		sql="SELECT count(1) FROM patients"
		cursor=connect.execute(sql)
		rows=cursor.fetchall()
		#3.3：响应请求
		self.write(str((rows[0])[0]))
		#3.4：关闭连接
		cursor.close()
		connect.close()	
#4：分页请求查询病人问诊记录
class PageHandler(tornado.web.RequestHandler):
	def get(self):
		pages = self.get_argument('pages')
		count = self.get_argument('count')
		#4.1：连接数据库
		connect = sqlite3.connect('patients_consult.db')
		#4.2: 执行sql查询
		sql_1="SELECT rowid FROM patients_consult GROUP BY patient_number"
		cursor=connect.execute(sql_1)
		rows=cursor.fetchall()
		list_id=[]
		list_user_count=len(rows)
		for row in rows:
			list_id.append(row[0])
		begain=list_id[(int(pages))*(int(count))]
		end=list_id[(int(pages)+1)*(int(count))]
		sql_2 = "SELECT rowid,patient_number,consult_date,category,disease_name  FROM patients_consult WHERE patient_number IN(SELECT DISTINCT patient_number FROM patients_consult WHERE rowid>=%d and rowid<%d)"
		data=(int(begain),int(end))
		cursor.execute(sql_2 % data)
		rows1=cursor.fetchall()
		#4.3 将结果转成json输出
		all_result={}
		all_result["total_count"]=list_user_count
		all_result["total_cords"]=rows1
		self.write(json.dumps(all_result))
		#4.4：关闭连接
		cursor.close()
		connect.close()
#5：配置路由
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',TestGetHandler),
			(r'/piegender',GenderHandler),
			(r'/count',CountHandler),
			(r'/page',PageHandler)
		]
		settings = {
			'template_path': 'pages',
			'static_path': 'static'
		}

		tornado.web.Application.__init__(self, handlers, **settings)        
#6：默认端口号设置：8001
if __name__ == '__main__':
	tornado.options.parse_command_line()

	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8001)
	tornado.ioloop.IOLoop.instance().start()        
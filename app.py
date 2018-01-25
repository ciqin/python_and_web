# coding=utf-8
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
#3:请求病人总数,top20_events
class CountHandler(tornado.web.RequestHandler):
	def get(self):
		#3.1:连接database
		connect = sqlite3.connect('patients_consult.db')
		#3.2:根据sql查询病人总数，top_20events,最大最小年龄
		sql="SELECT count(1) FROM patients"
		cursor=connect.execute(sql)
		rows=cursor.fetchall()
		total_patients=(rows[0])[0]
		#sql2="select distinct disease_name ,count(disease_name) as c from patients_consult group by disease_name order by c desc limit 20"
		sql2="select distinct disease_name ,count(disease_name) as c from patients_consult group by disease_name order by c desc limit 20"
		cursor=connect.execute(sql2)
		rows=cursor.fetchall()
		result={}
		list_event=[]
		for row in  rows :
			list_event.append(row[0])
		max_age=0
		min_age=0
		sql3="select max(age),min(age) from patients"
		cursor=connect.execute(sql3)
		rows=cursor.fetchall()
		print(rows)
		#3.3：处理数据响应请求
		result["total_count"]=total_patients
		result["top20_events"]=list_event
		result["max_age"]=(rows[0])[0]
		result["min_age"]=(rows[0])[1]
		self.write(json.dumps(result))
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
#7:条件查询请求
class FilterHander(tornado.web.RequestHandler):
	def get(self):
		try:
			#1:获取所有的查询条件,判断处理返回结果
			#:最小年龄,最大年龄,性别,病人就诊事件类型
			minAge=self.get_argument("minAge")
			maxAge=self.get_argument("maxAge")
			gender=self.get_argument("gender")
			eventa=self.get_argument("eventa")
			eventb=self.get_argument("eventb")
			eventc=self.get_argument("eventc")
			#连接数据库
			connect = sqlite3.connect('patients_consult.db')
			#满足年龄条件的病人总数
			sql_1="select distinct patient_number from patients  "
			if minAge =="unlimit":
				if maxAge=="unlimit":
					#查询结果没有年龄限制
					sql_1=sql_1
				else:
					sql_1=sql_1+"  where age <= "+maxAge
			else:
				if maxAge=="unlimit":
					#查询结果有最小年龄限制
					sql_1=sql_1+"  where age >= "+minAge
				else:
					#查询结果有最大最小年龄限制
					sql_1=sql_1+"  where age >= "+minAge +" and age <="+maxAge
			#查询出当前年龄段范围的病人总数
			cursor=connect.execute(sql_1)
			result1=cursor.fetchall()
			total_rangeAge=len(result1)
			#满足性别条件的病人总数
			print(maxAge)
			print(minAge)
			print(eventa)
			print(eventb)
			print(eventc)
			if gender=="unlimit":
				sql_1=sql_1
			else:
				if maxAge=="unlimit" and  minAge=="unlimit" :
					sql_1=sql_1+" where gender ="+gender
				else:
					sql_1=sql_1+" and gender="+gender
			#查询出当前年龄段,性别符合范围的病人总数
			cursor=connect.execute(sql_1)
			result2=cursor.fetchall()
			total_rangeAgeAndGender=len(result2)
			#就诊事件条件判断
			#1:没有事件类型限制
			if eventa =="unlimit" and  eventb=="unlimit" and  eventc=="unlimit":
				sql_1=sql_1
			#2:有一种事件类型限制eventa,eventb,eventc有一个不为空,三种情况
			#eventa不为空,eventb,eventc为空
			sql_2="select distinct patient_number from patients_consult "
			if eventa !="unlimit" and  eventb=="unlimit" and  eventc=="unlimit":
				sql_2=sql_2+" where disease_name ="+eventa
					
			if eventa =="unlimit" and  eventb!="unlimit" and  eventc=="unlimit":
				sql_2=sql_2+" where disease_name ="+eventb
				
			if eventa =="unlimit" and  eventb=="unlimit" and  eventc!="unlimit":
				sql_2=sql_2+" where disease_name ="+eventc
				
			#3:有两种种事件类型限制eventa,eventb,eventc有两个不为空,三种情况
			#ab ,bc,ac
			if eventa !="unlimit" and  eventb!="unlimit" and  eventc=="unlimit":
				print("哈哈")
				sql_2=sql_2+" where disease_name ="+eventa +" intersect " + sql_2+" where disease_name ="+eventb
			print(sql_2)	
			if eventa !="unlimit" and  eventb=="unlimit" and  eventc!="unlimit":
				sql_2=sql_2+" where disease_name ="+eventa +" intersect " + sql_2+" where disease_name ="+eventc
				
			if eventa =="unlimit" and  eventb!="unlimit" and  eventc!="unlimit":
				sql_2=sql_2+" where disease_name ="+eventb +" intersect " + sql_2+" where disease_name ="+eventc
			#4:3个event限制条件都不为空
			if eventa !="unlimit" and  eventb!="unlimit" and  eventc!="unlimit":
				sql_2=(sql_2+" where disease_name ="+eventb +" intersect " + sql_2+" where disease_name ="+eventc )+" intersect "+sql_2+" where disease_name ="+eventa
			
			print(sql_2)
			sql=sql_1+" intersect "+sql_2
			print(sql)
			
			cursor=connect.execute(sql)
			rows1=cursor.fetchall()
			#符合条件的病人总数
			in_count=len(rows1)
			#不符条件的病人总数
			sql_total_count="select count(patient_number) from patients"
			cursor=connect.execute(sql_total_count)
			rows2=cursor.fetchall()
			total_count=(rows2[0])[0]
			print(rows2)
			out_count=total_count-in_count
			result={}
			result["in_count"]=in_count
			result["out_count"]=out_count
			result["total_count"]=total_count
			#符合条件的就诊记录
			sql_3="select pc.patient_number,pc.consult_date,pc.disease_name,pc.category ,ps.age from patients_consult pc,patients ps where pc.patient_number in ("+sql+") and pc.patient_number= ps.patient_number order by ps.age"
			cursor=connect.execute(sql_3)
			rows3=cursor.fetchall()
			result["total_rangeAge"]=total_rangeAge
			result["total_rangeAgeAndGender"]=total_rangeAgeAndGender
			result["total_data"]=rows3
		#	sql_4="select patient_number,age from patients where patient_number in ("+sql+") order by age ASC"
		#	cursor=connect.execute(sql_4)
		#	print(rows4)
		#	result["patient_data"]=rows4
			self.write(json.dumps(result))
			cursor.close()
			connect.close()
		except:
			print("the request contains wrong arguments")
		finally:
			print("the request contains wrong arguments")

#5：配置路由
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',TestGetHandler),
			(r'/piegender',GenderHandler),
			(r'/count',CountHandler),
			(r'/page',PageHandler),
			(r'/select',FilterHander),
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
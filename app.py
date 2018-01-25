# coding=utf-8
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import sqlite3
import json
class TestGetHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
class LoginGetHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")    
# 自动载入               
class LoadGetHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('select * from message')
        values = cursor.fetchall()
        result_data = {}
        result_arr = []
        for value in values:
            result_arr.append([value[0],value[1],value[2],value[3],value[4]])
        result_data['data'] = result_arr
        self.write(result_data)
        cursor.close()
        conn.close()
# 表格添加内容        
class AddGetHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')
        blog = self.get_argument('blog')
        email = self.get_argument('email')
        address = self.get_argument('address')
        qq = self.get_argument('qq')
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('insert into message (name,blog,email,address,QQ) values (\''+name+'\',\''+blog+'\',\''+email+'\',\''+address +'\',\''+qq+'\')')
        cursor.close()
        conn.commit()
        conn.close()
# 表格数据删除        
class DeleteGetHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('delete from message where name =\''+name+'\'')
        cursor.close()
        conn.commit()
        conn.close()    
# 数据修改配置           
class ReviseGetHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')
        blog = self.get_argument('blog')
        email = self.get_argument('email')
        address = self.get_argument('address')
        qq = self.get_argument('qq')
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('update message set email=\''+email+'\', blog=\''+blog+'\', address=\''+address+'\', QQ=\''+qq+'\' where  name=\''+name+'\'')
        cursor.close()
        conn.commit()
        conn.close()          
# 检查登录路由          
class InspectgetHandler(tornado.web.RequestHandler):
    def get(self):
        email = self.get_argument('email')
        password = self.get_argument('password')   
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('select * from user where name=\''+email+'\' and password=\''+password+'\'')
        values = cursor.fetchall()
        if values:
            self.write('ok')
        else:
            self.write('err')    
        cursor.close()
        conn.close()

# 配置路由
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',LoginGetHandler),
            (r'/login',TestGetHandler),
            (r'/load',LoadGetHandler),
            (r'/add',AddGetHandler),
            (r'/delete',DeleteGetHandler),
            (r'/revise',ReviseGetHandler),
            (r'/inspect',InspectgetHandler)
		]
		settings = {
			'template_path': 'pages',
			'static_path': 'static'
		}

		tornado.web.Application.__init__(self, handlers, **settings)      
if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8001)
	tornado.ioloop.IOLoop.instance().start()             

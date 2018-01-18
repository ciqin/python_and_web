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
class DeleteGetHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('delete from message where name =\''+name+'\'')
        cursor.close()
        conn.commit()
        conn.close()       
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
# 配置路由
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',TestGetHandler),
            (r'/load',LoadGetHandler),
            (r'/add',AddGetHandler),
            (r'/delete',DeleteGetHandler),
            (r'/revise',ReviseGetHandler)
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

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.websocket
import tornado.web


class LedHandler(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
		return True


	def open(self):
		print "connection opened"
		self.write_message("connection opened")


	def om_close(self):
		print "connection closed"

	def on_message(self, message):
		print "Message received: {}".format(message)
		#aqui metes as condicoes conforme a mensagem
		self.write_message("message received")




if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/", LedHandler)])
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()

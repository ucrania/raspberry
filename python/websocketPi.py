import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'New connection was opened'
    self.write_message("Welcome to my websocket!")

  def on_message(self, message):
    print 'Incoming message:', message
    self.write_message("You said: " + message)

  def on_close(self):
    print 'Connection was closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()

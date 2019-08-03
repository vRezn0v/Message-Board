from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

#Messages are stored here
memory = []

form='''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
  {}
  </pre>'''


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        #reads length of content from POST header
        length = int(self.headers.get('Content-Length',0))
        #reads the data from POST request and stores it
        data = self.rfile.read(length).decode()
        #parses data and extracts message
        message = parse_qs(data)["message"][0]
        #formats message
        message = message.replace("<", "&lt;")
        #adds message to memory
        memory.append(message)
        #sends a redirect to MessageBoard home
        self.send_response(303)
        self.send_header("Location", '/')
        self.end_headers()

    def do_GET(self):
        #Sends OK response
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        #prints messages from memory to screen
        mes=form.format("\n".join(memory))
        self.wfile.write(mes.encode())

if __name__=='__main__':
    server_address=('',8000)
    httpd=HTTPServer(server_address,MessageHandler)
    httpd.serve_forever()

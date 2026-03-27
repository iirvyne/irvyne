from http.server import SimpleHTTPRequestHandler, HTTPServer
import cgi
import os

UPLOAD_DIR = "assets"
FILENAME = "current.jpg"  # always overwrite

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            fileitem = form['file']
            if fileitem.filename:
                filepath = os.path.join(UPLOAD_DIR, FILENAME)
                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'File uploaded successfully!')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No file uploaded!')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid request.')

def run():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Handler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

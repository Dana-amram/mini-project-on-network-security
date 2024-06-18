import http.server
import socketserver
import json
import os

# HTTPRequestHandler class
class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        http.server.SimpleHTTPRequestHandler.end_headers(self)
    
    # POST handler
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Assuming the received data is JSON with a 'number' field
            data = json.loads(post_data)
            number = data.get('number')
            if number is not None:
                print(f"Received number: {number}")
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Number received and printed.".encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Invalid request format: Missing 'number' field.".encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Invalid JSON format.".encode('utf-8'))

    # GET handler
    def do_GET(self):
        if self.path == '/get_exe':
            try:
                exe_file = os.path.join(os.path.dirname(__file__), 'voucher.exe')  # Path to your executable file
                with open(exe_file, 'rb') as f:
                    exe_data = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', 'attachment; filename="http_server.exe"')
                self.end_headers()
                self.wfile.write(exe_data)
                
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Executable file not found.".encode('utf-8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not found.".encode('utf-8'))

# Function to start the HTTP server
def run(server_class=http.server.HTTPServer, handler_class=HTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

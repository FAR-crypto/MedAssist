import http.server
import socketserver
import os

PORT = 8080
os.chdir(r'c:\Users\A1\hackathon PW')

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f'Frontend server running on http://localhost:{PORT}')
    print('Press Ctrl+C to stop')
    httpd.serve_forever()
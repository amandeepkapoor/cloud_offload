#!/usr/bin/python3
print("Content-Type: text/html\r\n\r\n")     # HTML is following
print("<html>")
print("<head><title>CGI script</title></head>")

print("<body>")
print("<p> It works </p>")

for i in range(5):
	print("<h1> It works </h1>")

print("</body>")
print("</html>")


import sys
import traceback

try:
    sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n")
    sys.stdout.write("\r\n")
    sys.stdout.write("<!doctype html><html><body>")
    sys.stdout.write("<h1>Python CGI läuft</h1>")
    sys.stdout.write("<p>Hallo vom IIS CGI</p>")
    sys.stdout.write("</body></html>")
    sys.stdout.flush()

except Exception:
    sys.stdout.write("Content-Type: text/plain; charset=utf-8\r\n\r\n")
    sys.stdout.write(traceback.format_exc())

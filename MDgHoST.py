import http.server
import socketserver
import os
from time import sleep

PORT=input("Enter Port#>>>...")
if len(PORT)>=5:
    PORT=80
else:
    PORT=int(PORT)

def show():
    print("""
***************************************************************************************************
@@@@@ @@@@@ @@@@@@@@@@@@@ @@              @@       @@  @@@@@@@@@@@  @@@@@@@@@@@@@  @@@@@@@@@@@@@@@@
@@@@@ @@@@@ @@@@@@@@@@@@@ @@              @@       @@  @@@@@@@@@@@  @@@@@@@@@@@@@  @@@@@@@@@@@@@@@@
@@ @@ @@ @@      @     @@ @@              @@       @@  @@       @@  @@                    @@
@@ @@@@@ @@      @     @@ @@    @@@@@@@@  @@@@@@@@@@@  @@       @@  @@@@@@@@@@@@@         @@
@@       @@      @     @@ @@    @@@@@@@@  @@#######@@  @@       @@  @@@@@@@@@@@@@         @@
@@       @@      @     @@ @@    @@    @@  @@       @@  @@       @@             @@         @@
@@       @@ @@@@@@@@@@@@@ @@@@@@@@    @@  @@       @@  @@@@@@@@@@@  @@@@@@@@@@@@@         @@
***************************************************************************************************
connecting to MDGHOST....
""")


def color():
    os.system("color A")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color B")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color C")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color D")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color E")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color F")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color EC")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color 1A")
    os.system("cls")
    show()
    sleep(0.5)
    os.system("color A")
    os.system("cls")
    show()
    os.system("color E")
    os.system("cls")
    show()
    


color()

#*****************************************#
#create http server
def httpserver():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("you are connected sucessfully with MDGHOST at PORT",PORT)
        dir=os.getcwd()
        print(f"your directory {dir} behaves as LOCAL SERVER at port {PORT}")
        print("\n")
        print(f"Serving at {PORT}...")
        httpd.serve_forever()




httpserver()

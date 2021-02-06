import threading
import time
import random
import socket

import sys

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    #Inputs
    rsHostname, rsListenPort = sys.argv[1], sys.argv[2]

    # connect to the server on local machine
    server_binding = (rsHostname, rsListenPort)
    cs.connect(server_binding)

    file = open('PROJI-HNS.txt', 'r')
    contents = file.read().splitlines()
    file.close()
    for hname in contents:
        #Send
        localhost_addr = socket.gethostbyname(socket.gethostname())

        # Receive data from the server
        data_from_server=cs.recv(100)
        print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))
        

    # close the client socket
    cs.close()
    exit()


   
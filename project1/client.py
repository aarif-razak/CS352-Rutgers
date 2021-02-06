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
    rsHostname, rsListenPort, tsListenPort = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

    # connect to the server on local machine
    server_binding = (rsHostname, rsListenPort)
    cs.connect(server_binding)

    file = open('PROJI-HNS.txt', 'r')
    outputFile = open("output.txt", "w")
    contents = file.read().splitlines()
    file.close()

    for hname in contents:
        #Connect to the new server, send a line                
        msg = hname
        cs.send(msg.encode('utf-8'))
        #Get the response and write it to the output file
        # Receive data from the server
        data_from_server = cs.recv(100).decode('utf-8')
        data = data_from_server.split(' ')
        if(data[2] == 'A'):
            outputFile.write("{}".format(data_from_server))
        elif(data[2] == 'NS'):
            #Connect to TS (new socket)
            try:
                tsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[C]: TSClient socket created")
            except socket.error as err:
                print('TSsocket open error: {} \n'.format(err))
                exit()
            tsConnect = (data, tsListenPort)
            tsSocket.connect(tsConnect)
            tsSocket.send(msg.encode('utf-8'))

            data_from_server = tsSocket.recv(100)

            outputFile.write("{}".format(data_from_server))

            tsSocket.close()
            
    #Close client socket
    cs.close()
    exit()

client()
   
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

    #Inputs
    rsHostname, rsListenPort, tsListenPort = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rs_ip = socket.gethostbyname(rsHostname)
    tsSocket = None
    ts_ip = None

    # connect to the server on local machine
    server_binding = (rs_ip, rsListenPort)
    cs.connect(server_binding)

    file = open('PROJI-HNS.txt', 'r')
    outputFile = open("RESOLVED.txt", "w")
    contents = file.read().splitlines()
    file.close()

    for hname in contents:
        #Connect to the new server, send a line                
        msg = hname
        cs.send(msg.encode('utf-8'))
        print('Sent {} to RS'.format(msg))
        #Get the response and write it to the output file
        # Receive data from the server
        data_from_server = cs.recv(100).decode('utf-8')
        data = data_from_server.split(' ')
        print('Received {} from RS'.format(data_from_server))
        if(data[2] == 'A'):
            outputFile.write("{}\n".format(data_from_server))
        elif(data[2] == 'NS'):
            try:
                # Connect to TS (new socket)
                if tsSocket is None:
                    tsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ts_ip = socket.gethostbyname(data[0])
                    tsConnect = (ts_ip, tsListenPort)
                    tsSocket.connect(tsConnect)
                    print("[C]: TSClient socket created")
            except socket.error as err:
                print('TSsocket open error: {} \n'.format(err))
                exit()

            tsSocket.send(msg.encode('utf-8'))
            print('Sent {} to TS'.format(msg))
            data_from_server = tsSocket.recv(100).decode()
            print('Received {} from TS'.format(data_from_server))
            outputFile.write("{}\n".format(data_from_server))
            
    #Close client socket
    cs.close()
    tsSocket.close()
    exit()

client()
   
import socket

import sys
import os

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Inputs
    ls_host, ls_port = sys.argv[1], int(sys.argv[2])
    ls_ip = socket.gethostbyname(ls_host)

    # connect to the server on local machine
    server_binding = (ls_ip, ls_port)
    cs.connect(server_binding)

    input_file = open('PROJ2-HNS.txt', 'r')
    contents = input_file.read().splitlines()
    input_file.close()
    output_file = open("RESOLVED.txt", "w")

    for hname in contents:
        # Connect to the new server, send a line
        msg = hname
        cs.send(msg.encode('utf-8'))
        print('Sent {} to LS'.format(msg))
        # Get the response and write it to the output file
        # Receive data from the server
        data_from_server = cs.recv(100).decode('utf-8')
        print('Received {} from LS'.format(data_from_server))
        output_file.write("{}\n".format(data_from_server))
            
    # Close client socket
    output_file.close()
    cs.close()
    exit()


client()

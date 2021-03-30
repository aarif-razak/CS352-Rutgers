import threading
import sys
import socket

def server(listenPort):
    file = open('PROJ2-DNSTS2.txt', 'r')
    contents = file.read().splitlines()
    file.close()
    hosts = []
    for x in contents:
        line = x.split(' ')
        hosts.append(tuple(line))
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', listenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    try:
        while 1:
            msg = csockid.recv(100).decode()
            if not msg:
                print("No more messages received. Closing connection with {}".format(addr))
                break
            print("Received message: {}".format(msg))
            result = [(x, y, z) for x, y, z in hosts if msg.lower() == x.lower()]
            response = ''
            if len(result) > 0:
                response = "{} {} {}".format(result[0][0], result[0][1], result[0][2])
                csockid.send(response.encode('utf-8'))
                print("Sent message: {}".format(response))
            # else do nothing
    except:
        print('Connection closed by client.')
    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    listenPort = int(sys.argv[1])
    t1 = threading.Thread(name='server', target=server, args=[listenPort])
    t1.start()

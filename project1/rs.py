import threading
import sys
import socket

def server(listenPort):
    # read from PROJI-DNSRS.txt and convert contents into a list of 3-tuples
    file = open('PROJI-DNSRS.txt', 'r')
    contents = file.read().splitlines()
    file.close()
    hosts = []
    ns = ''
    for x in contents:
        line = x.split(' ')
        hosts.append(tuple(line))
        if line[-1] == 'NS':
            ns = line[0] + ' ' + line[1] + ' ' + line[2]
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
        else:
            response = ns
            csockid.send(response.encode('utf-8'))
        print("Sent message: {}".format(response))
    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    listenPort = int(sys.argv[1])
    t1 = threading.Thread(name='server', target=server, args=[listenPort])
    t1.start()

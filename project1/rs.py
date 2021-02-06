import threading
import sys
import socket

def server(listenPort):
    # read from PROJI-DNSRS.txt and convert contents into a list of 3-tuples
    file = open('PROJI-DNSRS.txt', 'r')
    contents = file.read().splitlines()
    file.close()
    hosts = []
    for x in contents:
        hosts.append(tuple(x.split(" ")))

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

    msg = csockid.recv(100)
    print(msg.decode())
    result = [(x) for x, y, z in hosts if msg == x]
    print(result)
    csockid.send(result[0].encode('utf-8'))

    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    listenPort = int(sys.argv[1])
    t1 = threading.Thread(name='server', target=server, args=[listenPort])
    t1.start()

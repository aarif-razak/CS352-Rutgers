import threading
import sys
import socket


def server(listen_port, ts1_host, ts1_port, ts2_host, ts2_port):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', listen_port)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))



    # open connection to ts1 and ts2 servers

    while 1:
        msg = csockid.recv(100).decode()
        if not msg:
            print("No more messages received. Closing connection with {}".format(addr))
            break
        print("Received message: {}".format(msg))

        csockid.send(msg.encode('utf-8'))

        # forward msg to ts1 and ts2
        # nonblocking recv?
        # wait for response, send result to client

        # response = "{} {} {}".format(result[0][0], result[0][1], result[0][2])
        # csockid.send(response.encode('utf-8'))
        # print("Sent message: {}".format(response))
    # Close the server socket
    ss.close()
    exit()


if __name__ == "__main__":
    listen_port, ts1_host, ts1_port, ts2_host, ts2_port = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    t1 = threading.Thread(name='server', target=server, args=[listen_port, ts1_host, ts1_port, ts2_host, ts2_port])
    t1.start()

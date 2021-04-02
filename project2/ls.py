import select
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
    try:
        ts1s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Inputs
    ts1_ip = socket.gethostbyname(ts1_host)

    # connect to the server on local machine
    ts1server_binding = (ts1_ip, ts1_port)
    ts1s.connect(ts1server_binding)
    
    try:
        ts2s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS2]: Ts2 socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Inputs
    ts2_ip = socket.gethostbyname(ts1_host)

    # connect to the server on local machine
    ts2server_binding = (ts2_ip, ts2_port)
    ts2s.connect(ts2server_binding)

    while 1:
        msg = csockid.recv(100).decode()
        if not msg:
            print("No more messages received. Closing connection with {}".format(addr))
            break
        print("Received message from cleint: {}".format(msg))

        ts1s.send(msg.encode('utf-8'))
        ts2s.send(msg.encode('utf-8'))
        print("Sent message to ts servers: {}".format(msg))

        sockets = [ts1s, ts2s]

        readable, writable, errors = select.select(sockets, [], [], 5)

        if not readable:
            error_msg = "{} - Error:HOST NOT FOUND".format(msg)
            csockid.send(error_msg.encode('utf-8'))
            print("Sent message to client: {}".format(error_msg))
        else:
            for s in readable:
                ts_msg = s.recv(100).decode('utf-8')
                print("Received message from ts: {}".format(ts_msg))
                csockid.send(ts_msg.encode('utf-8'))
                print("Sent message to client: {}".format(ts_msg))





    # Close the server socket
    ss.close()
    ts1s.close()
    ts2s.close()
    exit()


if __name__ == "__main__":
    listen_port, ts1_host, ts1_port, ts2_host, ts2_port = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    t1 = threading.Thread(name='server', target=server, args=[listen_port, ts1_host, ts1_port, ts2_host, ts2_port])
    t1.start()

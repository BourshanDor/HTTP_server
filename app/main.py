import socket

OK = b'HTTP/1.1 200 OK\r\n\r\n'
NOT_FOUND = b'HTTP/1.1 404 Not Found\r\n\r\n'


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() 
    with conn : 
        data = conn.recv(1024)
        if b'HTTP' not in data : 
            return 
        lines = data.decode("utf-8").splitlines()
        first_line = lines[0].split()
        if len(first_line) == 3 and len(first_line[1]) ==1 and first_line[1][0] == '/' : 
            conn.send(OK)
        else : 
            conn.send(NOT_FOUND)


        

    




if __name__ == "__main__":
    main()

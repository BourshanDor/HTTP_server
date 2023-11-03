import socket

OK = b'HTTP/1.1 200 OK\r\n'
NOT_FOUND = b'HTTP/1.1 404 Not Found\r\n'
END = b'\r\n'


def build_response(content : str) -> bytes : 
    # text = content[6:]
    content_length = len(text)
    text = content.encode()
    content_length = f'Content-Length: {content_length}\r\n\r\n'.encode()
    message = OK + b'Content-Type: text/plain\r\n' + content_length +  text + END
    return message


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() 
    with conn : 
        
        data = conn.recv(1024)
        if b'HTTP' not in data : 
            return  
        lines = data.decode("utf-8").splitlines()
        first_line = lines[0].split()
        if len(first_line) == 3 and first_line[1] == '/' : 
            conn.send(OK + END)
        elif len(first_line) == 3 and '/echo' in first_line[1] :
            message = build_response((first_line[1])[6:]) 
            conn.send(message)
        else : 
            conn.send(NOT_FOUND + END)
        

if __name__ == "__main__":
    main()

import socket
from typing import List
import threading

OK = b'HTTP/1.1 200 OK\r\n'
NOT_FOUND = b'HTTP/1.1 404 Not Found\r\n'
END = b'\r\n'



def build_response(content : str) -> bytes : 
    content_length = len(content)
    text = content.encode()
    content_length = f'Content-Length: {content_length}\r\n\r\n'.encode()
    message = OK + b'Content-Type: text/plain\r\n' + content_length +  text + END
    return message

def user_agent(lines : List[str]) :
    for line in lines : 
        if 'User-Agent' in line : 
            content = line.split()
            return  content[-1]

def send_to_client(conn : socket) : 
    with conn : 
    
        data = conn.recv(1024)
        if b'HTTP' not in data : 
            return  
        lines = data.decode("utf-8").splitlines()
        first_line = lines[0].split()

        if len(first_line) == 3 and first_line[1] == '/' : 
            message = OK + END
            
        elif len(first_line) == 3 and '/echo' in first_line[1] :
            content = first_line[1]
            content = content[6:]
            message = build_response(content) 
            
        elif len(first_line) == 3 and '/user-agent' == first_line[1] :
            content = user_agent(lines)
            message = build_response(content) 

        else : 
            message = NOT_FOUND + END

        conn.sendall(message)

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    while True : 
        conn, addr = server_socket.accept() 
        threading.Thread(
            target= send_to_client, args=(conn)
        ).start()


                
if __name__ == "__main__":
    main()

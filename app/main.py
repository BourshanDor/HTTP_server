import socket
from typing import List
import threading
import sys 
import os 

OK = b'HTTP/1.1 200 OK\r\n'
OK201 = b'HTTP/1.1 201 OK\r\n'
NOT_FOUND = b'HTTP/1.1 404 Not Found\r\n'
END = b'\r\n'



def build_response(content : str, content_type: str, method) -> bytes : 
    content_length = len(content)
    text = content.encode()
    content_type = content_type.encode() 
    content_type = b'Content-Type: ' + content_type + END 
    content_length = f'Content-Length: {content_length}\r\n\r\n'.encode()
    if method == 'GET' : 
        message = OK + content_type + content_length +  text + END
    else : 
        message = OK201 + content_type + content_length +  text + END
    return message

def user_agent(lines : List[str]) :
    for line in lines : 
        if 'User-Agent' in line : 
            content = line.split()
            return  content[-1]
        


def send_to_client(conn : socket, addr, directory_path) : 
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
            message = build_response(content,'text/plain','GET') 
            
        elif len(first_line) == 3 and '/user-agent' == first_line[1] :
            content = user_agent(lines)
            message = build_response(content,'text/plain','GET') 

        elif len(first_line) == 3 and '/files' in first_line[1] and directory_path is not None and first_line[0] == 'GET': 
            file_name = first_line[1] 
            file_name = file_name[7:]
            real_file = check_file_exists(directory_path, file_name)

            if real_file : 
                path = os.path.join(directory_path, file_name)
                with open(path, 'rb') as file:
                    content = file.read().decode()
                    message = build_response(content,'application/octet-stream','GET')
            else : 

                message = NOT_FOUND + END

        elif len(first_line) == 3 and '/files' in first_line[1] and directory_path is not None and first_line[0] == 'POST' : 
            file_name = first_line[1] 
            file_name = file_name[7:]
            print('Im here')
            path = os.path.join(directory_path, file_name)
            content = lines[-1]
            print(content)
            with open(path, 'wb') as file:
                for i in range(1, len(lines)) : 
                    print('Im here')
                    content += file.write(lines[i]).decode()
                print(content)
                message = build_response(content,'application/octet-stream','GET')
    
        else : 
            message = NOT_FOUND + END

        conn.sendall(message)

def check_file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)


def main():
    if len(sys.argv) < 3 : 
        directory_path = None  
    else : 
        directory_path = sys.argv[2]

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    while True : 
        conn, addr = server_socket.accept() 
        threading.Thread(
            target= send_to_client, args=(conn, addr,directory_path)
        ).start()


                
if __name__ == "__main__":
    main()

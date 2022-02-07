# Sam Benoist
# CSEC 380 HW 2 - Act 3

import socket

# Global
host = "csec380-core.csec.rit.edu"
port = 82

def act3():
    # socket initialization
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # annoying header info
    header = "Host: " + host + "\r\n"
    contentType = "Content-Type: application/x-www-form-urlencoded\r\n"
    contentLength = "Content-Length: 12\r\n"
    params = "\r\nuser=sjb8894"
    Post = "POST /getSecure HTTP/1.1\r\n" + header + contentType + contentLength + params
    sock.sendall(Post.encode())
    data = sock.recv(4096).decode("utf-8")
    token = data.split()[-1][10:-2]  # extract token

    # token extracted, move get captcha
    token = "&token=" + token
    params = "user=sjb8894" + token
    cl = "Content-Length: " + str(len(params)) + "\r\n\r\n"
    p = "POST /getFlag3Challenge HTTP/1.1\r\n" + header + contentType + cl + params
    sock.sendall(p.encode())
    response = sock.recv(4096).decode()
    response = response.split()[-1][12:-2]
    sol = eval(response)
    print(sol)

    # equation solved, send solution to server
    solution = '&solution=' + str(sol)
    params = "user=sjb8894" + token + solution
    cl = "Content-Length: " + str(len(params)) + "\r\n\r\n"
    p = "POST /getFlag3Challenge HTTP/1.1\r\n" + header + contentType + cl + params
    sock.sendall(p.encode())

    # receive info from web server
    response = sock.recv(4096)
    sock.close()
    print(response)





def main():
    act3()
    # flag = 837536dd0c441755f12e0715ed26be5ec600aa1a4fea2beed3ef6e83


main()

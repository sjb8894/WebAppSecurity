# Sam Benoist
# CSEC 380 HW 2 - Act 2

import socket

# Global
host = "csec380-core.csec.rit.edu"
port = 82


def act2():
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

    # token extracted, move to recv flag
    token = "&token=" + token
    accept = "Accept: text-html\r\n"
    params = "user=sjb8894" + token
    cl = "Content-Length: " + str(len(params)) + "\r\n\r\n"
    p = "POST /getFlag2 HTTP/1.1\r\n" + header + contentType + cl + params
    sock.sendall(p.encode())

    # receive info from web server
    response = sock.recv(4096)
    sock.close()
    print(response)


def main():
    act2()
    # flag = 90c7031f2234d9fee7081d72c14822ce81bf020ea16534248e4831dd


main()

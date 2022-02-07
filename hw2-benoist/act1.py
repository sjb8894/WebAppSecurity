# Sam Benoist
# CSEC 380 HW 2 - Act 1

import socket

# Global
host = "csec380-core.csec.rit.edu"
port = 82


def act1():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    header = "Host: " + host + "\r\n"
    contentType = "Content-Type: application/x-www-form-urlencoded\r\n"
    contentLength = "Content-Length:12\r\n"
    username = "\r\nuser=sjb8894"
    Post = "POST / HTTP/1.1\r\n" + header + contentType + contentLength + username
    sock.sendall(Post.encode())
    resp = sock.recv(4096)
    sock.close()
    print(resp)


def main():
    act1()
    # flag = 1716d9063012a81c4c6d29b65e44bc834127cf6cf9eb23db8ee5ba64

main()

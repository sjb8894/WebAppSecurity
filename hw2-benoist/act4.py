# Sam Benoist
# CSEC 380 HW 2 - Act 4

import socket
import urllib3

# Global
host = "csec380-core.csec.rit.edu"
port = 82


def act4():
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

    # token extracted, create pw request
    accept = 'Accept: */*\r\n'
    acceptLang = 'Accept-Language: en-US\r\n'
    userAgent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko\r\n'
    acceptEncoding = 'Accept-Encoding: text/html\r\n'
    connection = 'Connection: keep-alive\r\n'
    contentType = "Content-Type: application/x-www-form-urlencoded\r\n"
    customUser = '&username=gavinbelson'
    params = "user=sjb8894&token=" + token + customUser
    cl = "Content-Length: " + str(len(params)) + "\r\n\r\n"
    p = "POST /createAccount HTTP/1.1\r\n" + header + accept + acceptLang + userAgent + acceptEncoding + connection + \
        contentType + cl + params
    sock.sendall(p.encode())
    response = sock.recv(4096).decode()
    password = response.split()[-1][21:-2]
    password = password.replace('&', '%26').replace('=', '%3D')

    # password extracted, create final request
    params = "user=sjb8894" + customUser + "&token=" + token + "&password=" + password
    cl = "Content-Length: " + str(len(params)) + "\r\n\r\n"
    p = "POST /login HTTP/1.1\r\n" + header + accept + acceptLang + userAgent + acceptEncoding + connection + \
        contentType + cl + params
    sock.sendall(p.encode())
    response = sock.recv(4096).decode()
    print(response)
    sock.close()


def main():
    act4()
    # flag = 9d89a3bd5c648468497a0f3e2ae6ae355731a2a9e77e6e8f84be2941


main()

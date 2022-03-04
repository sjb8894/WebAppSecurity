import re

from bs4 import BeautifulSoup
import socket
import ssl
import csv
import base64
from ast import parse


class Request:
    def __init__(self, webpage, port, secure=False):
        self.sock = self.createSock(secure)
        self.hostname = webpage
        self.port = port
        self.user = "sjb8894"
        self.request = b''
        self.parameters = ""

    def createSock(self, secure):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def getRequest(self, path):
        self.request = (f"GET {path} HTTP/1.1\r\n" +
                        f"Host: {self.hostname}\r\n" +
                        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36\r\n" +
                        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n" +
                        "Accept-Encoding: deflate\r\n" +
                        "Accept-Language: en-US,en;q=0.9\r\n\r\n"
                        )
        self.request = self.request.encode()
        return self.request

    def getRequestImage(self, pathPref="/", imgPairs=dict()):
        if imgPairs:
            for key in imgPairs:
                self.parameters = self.parameters + f"&{key}={imgPairs.get(key)}"
        self.request = (f"GET {pathPref} HTTP/1.1\r\n" +
                        f"Host: claws.rit.edu\r\n" +
                        "Sec-Ch-Ua: \"Chromium\";v=\"93\", \" Not;A Brand\";v=\"99\"\r\n" +
                        "Sec-Ch-Ua-Mobile: ?0\r\n" +
                        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36\r\n" +
                        "Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\n" +
                        "Sec-Fetch-Site: same-site\r\n" +
                        "Sec-Fetch-Mode: no-cors\r\n " +
                        "Sec-Fetch-Dest: image\r\n" +
                        "Referer: https://www.rit.edu/\r\n" +
                        "Accept-Encoding: deflate\r\n" +
                        "Accept-Language: en-US,en;q=0.9\r\n\r\n"
                        )
        self.request = self.request.encode()
        return self.request

    def sendSecureImg(self, site):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=site)
        sock.connect((self.hostname, self.port))
        sock.settimeout(3)
        sock.sendall(self.request)
        page = b''
        pg = sock.recv(512 * 8192)
        while pg != "" and pg != None:
            pgd = pg
            page = page + pgd
            try:
                pg = sock.recv(512 * 8192)
            except:
                break
        self.parameters = ""
        return page

    def collectPageContents(self, site):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=site)
        sock.connect((self.hostname, self.port))
        sock.settimeout(3)
        sock.sendall(self.request)
        page = ""
        pageb = b''
        try:
            pg = sock.recv(512 * 8192)
        except:
            return "Failed"
        while pg != "" and pg is not None:
            try:
                pgd = str(pg.decode())
                if pgd in page:
                    break
                page = page + pgd
            except:
                pgd = pg
                pageb = pageb + pgd
            try:
                pg = sock.recv(512 * 8192)
            except:
                break
        self.parameters = ""
        return page


class Parse:
    def __init__(self, site):
        self.site = site
        self.soup = BeautifulSoup(self.site, 'lxml')
        data = self.soup.find_all(text=True)
        self.courses = []
        self.csvHeader = ["Course Code, Course Name"]
        self.siteList = []
        self.sitesLinked = dict()
        for x in data:
            new = x.replace(u'\xa0', ' ')
            x.replace_with(new)

    # parses course name
    def parseCourse(self, cells):
        if len(cells) != 3:
            return 0
        coursExp = re.compile(r'[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]-\d\d\d')
        courseName = str(cells[0])
        courseName = courseName.split("<td>")
        courseName = courseName[1].split("</td>")
        name1 = str(courseName[0])

        if not coursExp.search(name1):
            return 0
        name1 = self.cleanUpWord(name1)
        divvies = cells[1].findAll("div", {"class": "course-name"})
        if len(divvies) >= 1:
            courseCode = str(divvies[0])
            courseCode = courseCode.split(">")[1]
            courseCode = courseCode.split("<")[0]
            courseCode = courseCode.lstrip('&nbsp')
            courseCode = self.cleanUpWord(courseCode)
        for item in self.courses:
            if item['courseName'] == name1:
                return 0
        if ":" in courseCode:
            courseCode = courseCode.split(':')[1]
            courseCode = self.cleanUpWord(courseCode)
        self.courses.append({'courseName': name1, 'courseCode': courseCode})

    # parses classes
    def parseClasses(self, course):
        tables = self.soup.find_all("table", {"class": course})
        for table in tables:
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                if course == "table-curriculum":
                    self.parseCourse(cells)

    # Something I rigged together, should work to remove leading whitespace
    def cleanUpWord(self, word):
        strippedWord = word
        for i in range(0, len(word)):
            num = ord(word[i])
            j = i + 1
            if num == 32:
                strippedWord = word[j:]
            else:
                return strippedWord

    # Write courses to CSV
    def exportCSV(self):
        identifier = ['courseCode', 'courseName']
        with open('/home/courses/coursesTest.csv', 'w+') as courses:
            writeToFile = csv.DictWriter(courses, fieldnames=identifier)
            writeToFile.writeheader()
            writeToFile.writerows(self.courses)

    def parseDirectory(self):
        rows = []
        rowList = self.soup.find_all("img", {"class": "card-img-top"})
        for row in rowList:
            rows.append(row)
        return rows

    def addToListHas(self, link, depth):
        if link not in self.sitesLinked.keys():
            self.sitesLinked[link] = depth
        if link not in self.siteList:
            self.siteList.append(link)

    def getSubLinks(self, link, depth):
        self.addToListHas(link, depth)
        returnHash = dict()
        for link in self.soup.find_all("a", {"href": re.compile("https:\/\/www.rit.edu|\.\/")}):
            try:
                slink = str(link).split("href=\"")[1]
                slink = slink.split("\"")[0]
                if slink not in self.siteList:
                    if (depth + 1) < 5:
                        self.sitesLinked[slink] = depth + 1
                        returnHash[slink] = depth + 1
            except:
                pass
        return returnHash

    def getImageSrcData(self, image):
        src = str(image).split("data-src=")[1]
        link = src.split("\"")[1]
        return link

    def getEmails(self):
        emailSet = set()
        emailregexstring = "mailto:(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        for semail in self.soup.find_all("a", {"href": re.compile(emailregexstring)}):
            email = str(semail).split("href=\"mailto:")[1]
            email = email.split("\"")[0]
            emailSet.add(email)
        return emailSet

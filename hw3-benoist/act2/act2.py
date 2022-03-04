import multiprocessing
import RequestAndParsing
import threading
from multiprocessing.context import Process
from sys import path
import time

listOfLinks = []
d1Set = set()
d2Set = set()
d3Set = set()
d4Set = set()


def siteCollector(site, path, port):
    socket = RequestAndParsing.Request(site, port, True)
    socket.getRequest(path)
    page = socket.collectPageContents(site)
    return page


def getPath(site, link):
    return link.split(site)[1]


def getSite(link):
    try:
        link = link.split("://")[1]
        link = link.split("/")[0]
    except:
        return "Failed"
    return link


def parseEmail(emailset, depth):
    for email in emailset:
        if email not in d1Set and email not in d2Set and email not in d3Set and email not in d4Set:
            if depth == 1:
                d1Set.add(email)
            elif depth == 2:
                d2Set.add(email)
            elif depth == 3:
                d3Set.add(email)
            else:
                d4Set.add(email)
            print(email)


def recursiveLinkSearch(link, depth):
    if depth > 4:
        return 0
    elif depth == 4:
        if link not in listOfLinks:
            site = getSite(link)
            if site == "Failed":
                pass
            else:
                path = getPath(site, link)
                page = siteCollector(site, path, 443)
                if page == "Failed":
                    pass
                else:
                    parser = RequestAndParsing.Parse(page)
                    emailList = parser.getEmails()
                    parseEmail(emailList, depth)
                    listOfLinks.append(link)
    else:
        if link not in listOfLinks:
            site = getSite(link)
            if site == "Failed":
                pass
            else:
                path = getPath(site, link)
                page = siteCollector(site, path, 443)
                if page == "Failed":
                    pass
                else:
                    parser = RequestAndParsing.Parse(page)
                    links = parser.getSubLinks(link, depth)  # get list of links
                    emailList = parser.getEmails()
                    listOfLinks.append(link)
                    parseEmail(emailList, depth)
                    for x in links.keys():
                        depth = links[x]
                        recursiveLinkSearch(x, depth)


def main():
    processes = []  # list of threads running
    site = siteCollector("www.rit.edu", "/", 443)
    # works to here
    parser = RequestAndParsing.Parse(site)
    subLinks = parser.getSubLinks("www.rit.edu", 0)
    # works to here
    for link in subLinks.keys():
        depth = subLinks[link]
        # works to here
        p = threading.Thread(target=recursiveLinkSearch, args=(link, depth,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()

    with open('depth1.txt', 'w+') as f:
        for email in d1Set:
            f.write(f"{email}\n")
    with open('depth2.txt', 'w+') as f:
        for email in d2Set:
            f.write(f"{email}\n")
    with open('depth3.txt', 'w+') as f:
        for email in d3Set:
            f.write(f"{email}\n")
    with open('depth4.txt', 'w+') as f:
        for email in d4Set:
            f.write(f"{email}\n")


main()

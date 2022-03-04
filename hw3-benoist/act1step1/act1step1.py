# imports
import RequestAndParsing

# Functionality is here - socket init w/ request, get req, and return page contents
def siteCollector(site, port):
    socket = RequestAndParsing.Request(site, port, True)  # creates socket
    socket.getRequest("/study/computing-security-bs")
    page = socket.collectPageContents(site)
    return page

# Main method
def main():
    site = siteCollector("www.rit.edu", 443)
    parse = RequestAndParsing.Parse(site)
    parse.parseClasses("table-curriculum")
    parse.exportCSV()
    print("Parsed!")

if __name__ == '__main__':
    main()

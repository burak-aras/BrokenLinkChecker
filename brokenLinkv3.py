import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class brokenLink():
    def __init__(self, xmlLink, searchWord):
        self.xmlLink = xmlLink
        self.searchWord = searchWord

    def xmlLinks(self):
        response = requests.get(self.xmlLink,verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        links = [i.getText("") for i in soup.find_all("loc")]
        links2 = []
        for i in links:
            if ".xml" in i:
                response2 = requests.get(i,verify=False)
                soup2 = BeautifulSoup(response2.text, "lxml")
                for i in soup2.find_all("loc"):
                    links2.append(i.getText(""))
        if links2:
            print(len(links2))
            return links2
        else:
            print(len(links))
            return links

    def subLinks(self, xmlLinks1):
        subLinks = []
        for i in xmlLinks1:
            response = requests.get(i,verify=False)
            soup = BeautifulSoup(response.text, "lxml")
            for i in soup.find_all("a"):
                subLinks.append(i.get("href"))
        subLinks = list(filter(None, subLinks))
        subLinks = list(dict.fromkeys(subLinks))
        subLinks = [i for i in subLinks if self.searchWord in i]
        print(len(subLinks))
        return subLinks

    def control(self, subLinks):
        f = open("output.txt", "w")
        for i in subLinks:
            try:
                response = requests.get(i, verify=False,timeout=3)
                if response.status_code == 404 or response.status_code == 406:
                    print(response, " ", i)
                    f.write(f"{response} {i} \n ")
            except:
                print("? ", i)
        f.close()


brokenLinkDetect = brokenLink(xmlLink=input("Sitemap .xml link : "), searchWord=input("Search word (http=all) : "))
p2 = brokenLinkDetect.subLinks(xmlLinks1=brokenLinkDetect.xmlLinks())
brokenLinkDetect.control(p2)

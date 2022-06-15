from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------SİTEMAP ÇEKME--------------------------


def get_urls_of_xml(xml_url):
    response = requests.get(xml_url, verify=False)
    xml = response.text
    soup = BeautifulSoup(xml, "lxml")
    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)
    print("{} main link \n ***PLEASE WAİT***" .format(len(links_arr)))
    return links_arr


def linksData(linkData):
    links_data_arr = get_urls_of_xml(linkData)
    return links_data_arr

# -------------------SİTEMAP ALTINDAKİ TÜM LİNKLER--------------------------


def siteMapLinks(xmlLink):
    allLinks = []
    for i in xmlLink:
        try:
            resp = requests.get(i, verify=False)
            html = resp.content
            soup = BeautifulSoup(html, "html.parser")
            for i in soup.find_all("a"):
                allLinks.append(i.get("href"))
        except:
            pass
    allLinks = list(dict.fromkeys(allLinks))
    print("{} all link".format(len(allLinks)))
    return allLinks


links_data_arr = linksData(input("Web Site sitemap.xml adress "))
allLinks = siteMapLinks(links_data_arr)

# ------------------İSTENİLEN WEBSİTELERİNE GÖRE FİLTRELEME---------------------------


def filters(filteritem):
    filteredlist = []
    for string in allLinks:
        if string == None:
            string = "31"
        string = string.split()
        res = [x for x in string if filteritem in x]
        filteredlist.append(res)
        filteredListLast = list(filter(None, filteredlist))
    return filteredListLast


# ----------------KIRIK LİNK TESPİTİ-----------------------------

def detect(filterList):
    dosya = open("cıktı.txt", "w")
    for i in filterList:
        for a in i:
            try:
                response = requests.get(a, verify=False)
                if (response.status_code == 404) or (response.status_code == 406):
                    print(response, " ", a,)
                    dosya.write(a)
                    dosya.write("\n")
                else:
                    print(response)
            except:
                print("error skip : {}".format(a))
    dosya.close()


for i in range(100):
    girdi = input("serach word (for all pages=http) : (exit=Q)")
    if girdi == "Q":
        break
    filteredListLast = filters(girdi)
    detect(filteredListLast)
    

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import os


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def group_scrape(grpNum, dataCategory):
    raw_html = simple_get('https://attack.mitre.org/groups/'+grpNum+'/')
    html = BeautifulSoup(raw_html, 'html.parser')
    techs = html.find_all('td')
    if dataCategory is 'T' or 't':
        techList = html.body.findAll(text=re.compile('T\d\d\d'))
        return techList
    elif dataCategory is 'S' or 's':
        swList = html.body.findAll(text=re.compile('S\d\d\d'))
        return swList

def stockpile_search(techList):
    pathStart = '/root/caldera/plugins/stockpile/data/abilities/'
    source_tech_ymls = []
    grep = "grep attack_id "
    cut = "|cut -d \":\" -f 2 | cut -d " " -f 2"
    for subfolder, dir, files in os.walk(pathStart):
        for ymlfile in files:
            curPath = subfolder+'/'+ymlfile
            file = open(curPath, "r")
#            search = os.system(grep + curPath)
            search = re.findall("T/d/d/d/d", file) 
            print("value @ search var: ", search)
            print("search var type: ", type(search))
            if search in techList:
                source_tech_ymls.append(ymlfile)
                print("WINNERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            else:
                print('Something went wrong! Check line 60')
                print(ymlfile)
            file.close()


def write_file(techlist):
    file = open("groupdump.txt", "w")
    for item in techlist:
        file.write(item+'\n')
    file.close()
    
def line_search(filename, matchString):
    file = open(filename, "r")
    file.read()
        
        if re.findall(matchString, filename) in line:
            return filename
        else:
            return 1
    file.close()


#Use below to dump your scrape to a txt file
#write_file(group_scrape('G0010','T'))
stockpile_search("groupdump.txt")

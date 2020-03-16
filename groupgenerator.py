from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import os
import yaml

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

def write_file(techlist):
    file = open("groupdump.txt", "w")
    for item in techlist:
        file.write(item+'\n')
    file.close()

def tech_compare(file1, file2):
	#Takes the target group file as file 1 and compares with a given file (file2) to see if a known tech ID is present in a yml.
	f1 = open(file1, "r")
	f2 = open(file2, "r")
	#To compare line-by-line, we'll read the line content files prior to comparison. 
	f1Data = f1.readlines()
	f2Data = f2.readlines()
	for techNum in f1Data:
		for line in f2Data:
			if techNum in line:
				#We only need to see if the techNum is in the file. If so, we grab the file name.				
				f1.close()
				f2.close()
				return file2
			else:
				continue
	f1.close()
	f2.close()
	return 1

def stockpile_search(techList):
	#Compares stockpiled abilities with a group's tech numbers. 
	pathStart = '/root/caldera/plugins/stockpile/data/abilities/'
	sourceTechYMLs = []
	techPattern = (r"T\d\d\d\d")
	#beginning recursive yml search
	for subfolder, dir, files in os.walk(pathStart):
		for ymlfile in files:
			curPath = subfolder+'/'+ymlfile
			techMatch = tech_compare(techList, curPath)
			#(if crawled yml has mathing technique as source group list):
			if techMatch is not 1:
				sourceTechYMLs.append(ymlfile)	
			else:
				continue		
	if len(sourceTechYMLs) <= 0:
		#if loop breaks and returns an empty list, return error code 1
		return 1
	else:
		#success returns list object with any ymls matching the core list. ymls in list will be not include full path.  
		sourceTechIDs = []
		for yml in sourceTechYMLs:
			ID = yml.replace('.yml', '')
			sourceTechIDs.append(ID)
		return sourceTechIDs

def adv_yml_locate(advName):
	pathStart = "/root/caldera/"
	for subfolder, dir, files in os.walk(pathStart):
		for ymlfile in files:
			curPath = subfolder+'/'+ymlfile			
			if ".yml" not in ymlfile:
				break
			curFile = open(curPath, "r")
			curData = curFile.readlines()
			for line in curData:
				if advName in line:
					return ymlfile.replace(".yml", ""), curPath
	#If all loops do not return any results, return with error code 1
	return 1

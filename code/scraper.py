from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import time
import sys
from urllib.parse import urlparse


#create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

directory_file=sys.path[0]+"\data\directory"
negative_file=sys.path[0]+"\data\\negative"
urls=[]
#regex from: https://www.geeksforgeeks.org/python-check-url-string/
regexCheck = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
regexHome= r"(?i)\b(?:https?://|www\d{0,3}[.]|[a-z0-9.-]+[.][a-z]{2,4})"

#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url):
    #check if the page is reachable
    try:
        driver.get(url)
    except:
        print ("Could not resolve URL: " + url + ", skipping it")
        return -1
    #check if the inner HTML is readable
    try:
        res_html = driver.execute_script('return document.body.innerHTML')
        soup = BeautifulSoup(res_html,'html.parser', parse_only=SoupStrainer('a')) #beautiful soup object to be used for parsing html content
    except: 
        print ("Could not read innerHTML property for URL: " + url + ", skipping it")
        return -1
    return soup

# scrape all URLs from the root page of a website
def scrape_urls(home_url):
    soup = get_js_soup(home_url)
    if soup==-1:
        return
    for index, link in enumerate(soup):
        # limit to 30 URLs per page to avoid data skew when training
        if index > 30:
            break
        if (link.has_attr('href')):
            href=link['href']
            #if there is a link, check to make sure it's a URL and not a relative link
            if (bool(urlparse(href).netloc)):
                urls.append(href)
            #ignore tel and mailto links
            elif (href.find('tel:')>-1 or href.find('mailto:')>-1):
                pass
            #otherwise it is a relative link so concat it with home_url
            else:
                urls.append(home_url+href)
    
    print ("Scraped URLs from " + home_url, flush=True)

    
def writeURLs(urls):
    #write URLs to the negative file 
    with open(negative_file, 'a', encoding="utf-8") as f:
        for url in urls:
            f.write(url+"\n")
        f.close()

with open(directory_file, 'r') as f:
    #iterate over each directory url
    for index, line in enumerate(f):
        #extract just the home page URL
        homepage=''.join(re.findall(regexHome,line))
        #make sure its a valid url
        if (len(re.findall(regexCheck,homepage))!=0):
            # add the home page and directory page
            urls.append(homepage)
            urls.append(line.strip())
            scrape_urls(homepage)
        else:
            print (line + " is not a valid URL, skipping it")
        #periodically write the results
        if (index % 10 == 5):
            writeURLs(urls)
            urls=[]
    f.close()

#remove any duplicates
with open(negative_file, 'r+', encoding="utf-8") as f:
    urls=f.readlines()
    urls = list(dict.fromkeys(urls))
    #completely rewrite the file
    f.seek(0)
    for url in urls:
        f.write(url)
    f.truncate()
    f.close()




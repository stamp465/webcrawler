import requests
from requests.exceptions import HTTPError
from urllib.parse import urljoin
import os, codecs
import sqlite3
import hashlib
from urllib.parse import unquote

connection = sqlite3.connect("webcrawler_timeout_2.db")
cursor = connection.cursor()

'''
cursor.execute("CREATE TABLE true_q (No INTEGER, raw_html TEXT, hash TEXT)")
cursor.execute("CREATE TABLE visited_q (No INTEGER, raw_html TEXT, hash TEXT)")
cursor.execute("CREATE TABLE frontier_q (No INTEGER, raw_html TEXT, hash TEXT)")
'''

headers = {
    'User-Agent': '6310500350_Witnapat',
    'From': 'witnapat.c@ku.ac.th'
}
seed_url = 'https://ku.ac.th'
frontier_q = [seed_url]
visited_q = []
true_q = []
robots = []
hosts = []
sitemaps = []

def hashs(want) :
    return int(hashlib.sha256(want.encode('utf-8')).hexdigest(), 16) % 10**8

######################################## GEN FOLDER #######################################

rows = cursor.execute("SELECT raw_html FROM true_q").fetchall()

countfolder = 0
#print(rows)

for row in rows :
    link = ''.join(row[0].split())
    if -1 == urljoin(link, '/').find("ku.ac.th") :
        continue
    if link[len(row)-6:] != ".html" and link[len(row)-5:] != ".htm" :
       continue
    #print(link)
    rawlink = link
    link = link.replace("http://","")
    link = link.replace("https://","")
    #link = link.replace("www.","")
    splink = link.split('/')
    check = #\\ / * ? : < > /|
    ch = 0
    for checklink in splink :
        for i in checklink :
            if i in check :
                ch = 1
    if ch == 1 :
        continue
    print("link = ",rawlink,link,splink)
    path = 'html' 
    for i in range(len(splink)) :
        if i != len(splink)-1 :
            path = path +  '/' + unquote(splink[i])
    os.makedirs(path, 0o755, exist_ok=True)

    text = f'<html><body><a href="{unquote(rawlink)}">{unquote(link)}</a></body></html>'
    raw_html = text
    abs_file = path + '/' + unquote(splink[len(splink)-1])
    f = codecs.open(abs_file, 'w', 'utf-8')
    f.write(raw_html)
    f.close()
    countfolder += 1

print(countfolder,"22222222222222222222222222222222222222222222222222222222222")
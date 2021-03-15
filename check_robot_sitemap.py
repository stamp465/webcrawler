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

######################################## CHECK ROBOTS AND SITEMAP #######################################


def robot_read(link) :
    if link[len(link)-1] == '/' :
        checkrobot = link
    else :
        checkrobot = link + '/'
    try:
        response = requests.get(checkrobot+"robots.txt", headers=headers, timeout=3)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        if checkrobot not in robots :
            print("SuccessR")
            robots.append(checkrobot)

def sitemap_read(link) :
    if link[len(link)-1] == '/' :
        checksitemap = link
    else :
        checksitemap = link + '/'
    try:
        response = requests.get(checksitemap+"sitemap.xml", headers=headers, timeout=3)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        if checksitemap not in sitemaps :
            print("SuccessS")
            sitemaps.append(checksitemap)

def gen_robots_txt() :
    with open('robots.txt', 'w') as f:
        for robot in robots:
            f.write(robot + '\n')
            

def gen_sitemaps_txt() :
    with open('sitemaps.txt', 'w') as f:
        for sitemap in sitemaps:
            f.write(sitemap + '\n')

cursor.execute("CREATE TABLE hosts (No INTEGER, raw_html TEXT, hash TEXT)")
nub = 0
hosts_in = "INSERT INTO hosts (No, raw_html, hash) VALUES (?, ?, ?)"

for i in range(80900) :

    row2 = cursor.execute(f"SELECT raw_html FROM visited_q WHERE No = {i}").fetchone()
    #print(row2[0])
    if row2 == None : continue
    link = ''.join(row2[0].split())
    robotwant = urljoin(link, '/')
    if robotwant.find("ku.ac.th") == -1 or robotwant.find("kku.ac.th") != -1 :
        continue

    row2check = cursor.execute(f"SELECT raw_html FROM hosts WHERE hash = {hashs(robotwant)}").fetchone()
    print(robotwant,row2check,hashs(robotwant))
    if row2check == None :
        cursor.execute(hosts_in, (nub, robotwant, hashs(robotwant)) )
        connection.commit()
        print("put")
        nub += 1
    else :
        continue
    del row2,robotwant,link

for i in range(nub) :

    host = cursor.execute(f"SELECT raw_html FROM hosts WHERE No = {i}").fetchone()[0]
    if host == None : continue
    robot_read(host) 
    sitemap_read(host) 
    
gen_robots_txt() 
gen_sitemaps_txt()
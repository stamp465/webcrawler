import requests
from requests.exceptions import HTTPError
from urllib.parse import urljoin
import os, codecs
import sqlite3
import hashlib
from urllib.parse import unquote

connection = sqlite3.connect("webcrawler_timeout_2.db")
cursor = connection.cursor()


cursor.execute("CREATE TABLE true_q (No INTEGER, raw_html TEXT, hash TEXT)")
cursor.execute("CREATE TABLE visited_q (No INTEGER, raw_html TEXT, hash TEXT)")
cursor.execute("CREATE TABLE frontier_q (No INTEGER, raw_html TEXT, hash TEXT)")


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


######################################## GEN RAW HTML #######################################


def get_page(url):
    global headers
    text = ''
    try:
        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()
    except HTTPError as http_err:
        print(url,f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(url,f'Other error occurred: {err}')  # Python 3.6
    else:
        print("Success")
        text = response.text
        extracted_links = link_parser(text)
        for link in extracted_links :
            base_url = 'https://ku.ac.th'
            link = urljoin(base_url, link)
            if check_frontier_q(link) and check_visited_q(link) and -1 != link.find("ku.ac.th") and -1 == link.find("kku.ac.th") and -1 == link.find(".pdf") and -1 == link.find(".exe") and -1 == link.find(".mp4") and -1 == link.find(".jpg") and -1 == link.find(".png"):
                inset_frontier_q(link)
        del text
        del extracted_links
        del response

def link_parser(raw_html):
    urls = [];
    pattern_start = '<a href="';  pattern_end = '"'
    index = 0;  length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            if len(link) > 0:
                if link not in urls:
                    urls.append(link)
            index = end
        else:
            break
    del raw_html
    return urls

def check_frontier_q(url) :
    rows = cursor.execute(f"SELECT raw_html FROM frontier_q WHERE hash = {hashs(url)}").fetchone()
    #print(rows)
    if rows == None :
        del rows
        return True
    del rows
    return False

def check_visited_q(url) :
    rows = cursor.execute(f"SELECT raw_html FROM visited_q WHERE hash = {hashs(url)}").fetchone()
    #print(rows)
    if rows == None :
        del rows
        return True
    del rows
    return False

def inset_frontier_q(url) :
    global c_frontier_q
    frontier_q_in = "INSERT INTO frontier_q (No, raw_html, hash) VALUES (?, ?, ?)"
    cursor.execute(frontier_q_in, (c_frontier_q, url, hashs(url)) )
    c_frontier_q += 1
    connection.commit()

def inset_visited_q(url) :
    global c_visited_q
    visited_q_in = "INSERT INTO visited_q (No, raw_html, hash) VALUES (?, ?, ?)"
    cursor.execute(visited_q_in, (c_visited_q, url, hashs(url)) )
    c_visited_q += 1
    connection.commit()

def inset_true_q(url) :
    global c_true_q
    true_q_in = "INSERT INTO true_q (No, raw_html, hash) VALUES (?, ?, ?)"
    cursor.execute(true_q_in, (c_true_q, url, hash(url)) )
    c_true_q += 1
    connection.commit()

c_frontier_q,c_visited_q,c_true_q = 0,0,0
start = seed_url
now = 0
inset_frontier_q(start)

while c_true_q < 10000 :

    current_url = cursor.execute(f"SELECT raw_html FROM frontier_q WHERE No = {now}").fetchone()[0]
    if current_url == None :
        print(now)
        break
    inset_visited_q(current_url)
    if -1 != current_url.find(".html") or -1 != current_url.find(".htm") :
        inset_true_q(current_url)
    get_page(current_url)
    now += 1

    cursor.execute(f"DELETE FROM frontier_q WHERE hash = {hashs(current_url)}")
    connection.commit()


print("11111111111111111111111111111111111111111111111111111111111")
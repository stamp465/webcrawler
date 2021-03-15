import requests
from requests.exceptions import HTTPError
from urllib.parse import urljoin
import os, codecs
import sqlite3
import hashlib
from urllib.parse import unquote

connection = sqlite3.connect("webcrawler_timeout_2.db")
cursor = connection.cursor()
c_frontier_q = 0

def inset_frontier_q(url) :
    global c_frontier_q
    frontier_q_in = "INSERT INTO frontier_q (No, raw_html, hash) VALUES (?, ?, ?)"
    cursor.execute(frontier_q_in, (c_frontier_q, url, hashs(url)) )
    c_frontier_q += 1
    connection.commit()

def hashs(want) :
    return int(hashlib.sha256(want.encode('utf-8')).hexdigest(), 16) % 10**8

for i in range(30544,30798) :
	row2 = cursor.execute(f"SELECT raw_html FROM visited_q WHERE No = {i}").fetchone()
	urls = row2[0]
	#print(row2)
	inset_frontier_q(urls)
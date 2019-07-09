#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import socks
import socket
import sys
import io
import bs4

from pprint import pprint

g_done = {}
g_depth = 0

def get_root_url(target_url):
    start_index = target_url.find("//")
    end_index = target_url.find("/", start_index + 2) + 1
    return target_url[0:end_index]



def check_url(target_url, depth):
    if depth > g_depth:
        return 
    if target_url in g_done:
        return
    else:
        g_done[target_url] = True

    print("target_url : " + target_url)
    try:
        if target_url.find("pdf") != -1:
          rep = requests.head(target_url)
        elif target_url.find("zip") != -1:
          rep = requests.head(target_url)
        elif target_url.find("jpg") != -1:
          rep = requests.head(target_url)
        elif target_url.find("png") != -1:
          rep = requests.head(target_url)
        else:
          rep = requests.get(target_url)
    except Exception as ex:
        print("NG: ", end="")
        print(target_url, end="")
        print(", coudn't connect")
        sys.stdout.flush()
        return
        
    if rep.status_code == 200:
        print("OK: ", end="")
        print(target_url)
        sys.stdout.flush()
        base_url = rep.url
#        print(base_url)
        index_tail = base_url.rfind("/") + 1
        base_url = base_url[0:index_tail]
#        print(base_url)

        soup = bs4.BeautifulSoup(rep.text, 'html.parser')
        links = soup.find_all("a")
#        pprint(links)

        for link in links:
#            print(link.get("href"))
            new_url = link.get("href")
            if new_url == None:
                return
            if new_url.find("/") == 0:
                new_url = new_url[1:]
                new_url = get_root_url(target_url) + new_url
            elif new_url.find("http") == -1:
                new_url = base_url + new_url
            check_url(new_url, depth + 1)
    else:
        print("NG: ", end="")
        print(target_url, end="")
        print(", %d" % (rep.status_code))
        sys.stdout.flush()
        



sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

parser = argparse.ArgumentParser(description="Web Link Checker")
parser.add_argument("target_url", help="target_url")
parser.add_argument("-d", "--depth", type=int, default=1, help="follow depth")

args = parser.parse_args()
target_url = args.target_url
g_depth = args.depth

check_url(target_url, 0)


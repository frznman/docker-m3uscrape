import json
import os
import subprocess
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from bottle import route, run, Bottle, request, static_file

app = Bottle()

@app.route('/m3uscrape', method='GET')
def getFromURL():
    url = request.query["url"]
    if "" != url:
        m3u_list = getM3U(url)
        return { "success" : True, "m3u-list" : m3u_list }
    else:
        return { "success" : False, "error" : "No URL specified" }

@app.route('/m3uscrape', method='POST')
def postFromURL():
    url = request.forms.get( "url" )
    if "" != url:
        m3u_list = getM3U(url)
        return { "success" : True, "m3u-list" : m3u_list }
    else:
        return { "success" : False, "error" : "No URL specified" }




def getM3U(url):
    r  = requests.get(url)

    # Add response
    resps = []
    resps.append(r)

    soup = BeautifulSoup(r.text, "html5lib")

    # Find and load iFrames
    for iframe in soup.find_all('iframe'):
        iframe_url = iframe.attrs['src']
        if iframe_url.startswith('http'):
            print(iframe_url)
            iframe_resp = requests.get(iframe_url)
        elif iframe_url.startswith('www'):
            print('http://' + iframe_url)
            iframe_resp = requests.get('http://' + iframe_url)
        else:
            print(urljoin(url, iframe_url))
            iframe_resp = requests.get(urljoin(url, iframe_url))

        resps.append(iframe_resp)

    # Look through responses to find m3us
    m3u_list = []

    for resp in resps:
    #    print re.findall(r'(?:\'|")(?:(http[s]?):\/\/)+([^:\/\s]+)(:[0-9]+)?((?:\/\w+)*\/)([\w\-\.]+[^#?\s]+)([^#\s]*)?(#[\w\-]+)?(?:\'[,]?|"[,]?)', resp.text)
    #    print re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', resp.text)
        m3u_list.extend(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:m3u8|m3u)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', resp.text))

    for i, m3u in enumerate(m3u_list):
        m3u_list[i] = m3u.rstrip('\'",')

    print (m3u_list)

    return m3u_list

app.run(host='0.0.0.0', port=9009, debug=True)

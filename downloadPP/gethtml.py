from urllib.request import urlopen
from re import findall
from constant import *

def get_html(url):
    response = urlopen(url)
    return response.read()

def get_all_elements(url):
    html = get_html(url)
    elements = []
    lines = html.split(b'\n')
    for line in lines:
        if elements_condition in line:
            elements.append(findall(elements_pattern, str(line))[0])
    return elements

def get_file_links(url):
    html = get_html(url)
    lines = html.split(b'\n')
    links = []
    for line in lines:
        if filelink_condition in line:
            links.append(findall(filelink_pattern, str(line))[0])
    return links

def get_file(url):
    html = get_html(url)
    try:
        return str(html, 'cp949')
    except:
        return str(html, 'utf-8')
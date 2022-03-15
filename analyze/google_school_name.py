#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import sys, os, time, signal
from googlesearch import search
def parse_school_name(name):
    # The type of variable name is 'str' while type(" university wikipedia") is unicode
    # so we need to convert the str to unicode type
    name = name.decode("utf-8")
    query = name + " university wikipedia"
    
    # Google search library may meet some error when encode the unicode variable
    # since we do not specify the encoding method in the library, so we pass in str type instead
    for j in search(query.encode("utf-8"), tld="co.in", num=10, stop=10):
        if "wikipedia.org" in j:
            page = requests.get(j)
            soup = BeautifulSoup(page.content, "html.parser")
            heading = soup.find("h1", {"id": "firstHeading"})
            result = heading.text.strip()
            return result
# We can not output variable in unicode type in print statement or write to file, so we have to encode it.
result = parse_school_name(sys.argv[1])
if result == None:
    print("not found")
else:
    print(result.encode("utf-8"))
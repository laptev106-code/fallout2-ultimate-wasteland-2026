import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def search_github(query):
    url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('items', [])
    except Exception as e:
        print("GitHub error for", query, ":", e)
        return []

import urllib.parse
print("Searching GitHub for gl_mapblur.int or mapblur:")
items = search_github("gl_mapblur filename:gl_mapblur")
for item in items[:5]:
    print(" ", item.get('name'), "->", item.get('html_url'))

items2 = search_github("gl_footsteps filename:gl_footsteps")
for item in items2[:5]:
    print(" ", item.get('name'), "->", item.get('html_url'))

items3 = search_github("glasses filename:gl_glasses")
for item in items3[:5]:
    print(" ", item.get('name'), "->", item.get('html_url'))

import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def search_duck(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            links = re.findall(r'<a class="result__url" href="([^"]+)"', html)
            snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
            print(f"=== Results for {query} ===")
            for l, s in zip(links[:5], snippets[:5]):
                clean_s = re.sub(r'<[^>]+>', '', s).strip()
                print(f"Link: {l}\nSnippet: {clean_s}\n")
    except Exception as e:
        print(f"Error {query}: {e}")

if __name__ == '__main__':
    search_duck('Fallout 2 "Talking Heads Addon" github OR mediafire OR mega OR nexusmods')
    search_duck('Fallout 2 "MapBlurFX" sfall')
    search_duck('Fallout 2 "gl_glasses" OR "glasses mod" sfall')

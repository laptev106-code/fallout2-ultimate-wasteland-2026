import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def inspect_page(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            # Look for txt links or changelog links
            txt_links = re.findall(r'href="([^"]+\.txt[^"]*)"', html, re.I)
            print(f"=== TXT links on {url} ===")
            for l in set(txt_links):
                print("  ", l)
            # Look for survival mentions
            matches = re.findall(r'.{0,50}(?:выживани|survival|голод|жажд).{0,50}', html, re.I)
            print(f"=== Mentions of survival ({len(matches)}) ===")
            for m in matches[:5]:
                print("  ", m.strip())
    except Exception as e:
        print(f"Error {url}: {e}")

if __name__ == '__main__':
    # Search for nuclear-city topic
    inspect_page('https://nuclear-city.com/index.php/topic/1010-fallout-2-rp-fixed-edition/')
    inspect_page('https://nuclear-city.com/index.php/topic/588-fallout-2-restoration-project-modifikaciya-sborka-ot-foxx/')

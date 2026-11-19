import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://vk.com/board174451664', headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
        html = raw.decode('windows-1251', errors='ignore')
        print("board174451664 length:", len(html))
        
        # Search for topics
        topics = re.findall(r'href="(/topic-174451664_\d+)"[^>]*>([^<]+)<', html)
        for t, title in topics:
            print("Topic:", t, "Title:", title)
            
        # Search for any topic
        all_topics = re.findall(r'/topic-174451664_\d+', html)
        print("All topic links:", set(all_topics))
except Exception as e:
    print("Error:", e)

import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Accept-Language': 'ru,en;q=0.9'
}

for url in ['https://m.vk.com/rebuild_by_foxx', 'https://m.vk.com/board174451664']:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode('windows-1251', errors='ignore')
            print(f"URL: {url}, length: {len(raw)}")
            
            # Search for topic links
            topics = re.findall(r'href="(/topic-[^"]+)"[^>]*>([^<]+)<', raw)
            for t, title in topics:
                print(f"  Topic: {t} -> {title}")
                
            all_topics = re.findall(r'/topic-174451664_\d+', raw)
            if all_topics:
                print(f"  All topics: {set(all_topics)}")
                
            # Search for links to txt or changelog
            txts = re.findall(r'href="([^"]+\.txt[^"]*)"', raw)
            if txts:
                print(f"  TXT links: {txts}")
                
    except Exception as e:
        print(f"Error {url}: {e}")

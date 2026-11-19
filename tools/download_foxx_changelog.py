import urllib.request
import re
import os

file_id = '1UgWjizQb-Ivig60tq13WDNcTQF_sY1OB'

# We can try export=download or direct drive download
urls = [
    f'https://drive.google.com/uc?export=download&id={file_id}',
    f'https://drive.usercontent.google.com/download?id={file_id}&export=download',
    f'https://drive.google.com/file/d/{file_id}/view'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

downloaded = False
for url in urls:
    try:
        print("Trying:", url)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            print("Received bytes:", len(data))
            
            # If it's HTML, check if there is a confirm link or file contents embedded
            if b'<html' in data.lower():
                html_text = data.decode('utf-8', errors='ignore')
                print("Received HTML page, title:", re.findall(r'<title>(.*?)</title>', html_text))
                
                # Check for confirm code or download url
                m = re.search(r'href="(/uc\?export=download[^"]+)"', html_text)
                if m:
                    confirm_url = 'https://drive.google.com' + m.group(1).replace('&amp;', '&')
                    print("Found confirm download url:", confirm_url)
                    req2 = urllib.request.Request(confirm_url, headers=headers)
                    with urllib.request.urlopen(req2, timeout=15) as resp2:
                        data = resp2.read()
                        
                # Check if it's the raw text preview
                # Google Drive often embeds text file contents in json
                json_matches = re.findall(r'window\[\'_initData\'\]\s*=\s*(.*?);</script>', html_text)
                if not json_matches:
                    json_matches = re.findall(r'data-doc-content="([^"]+)"', html_text)
                    
            # Try to decode as text
            for enc in ['utf-8', 'windows-1251', 'cp866']:
                try:
                    text = data.decode(enc)
                    if 'foxx' in text.lower() or 'fallout' in text.lower() or 'исправлен' in text.lower() or 'версия' in text.lower():
                        out_path = 'd:/AG games mods/fallout2-ultimate-wasteland-2026/tools/foxx_full_changelog.txt'
                        with open(out_path, 'w', encoding='utf-8') as out:
                            out.write(text)
                        print(f"SUCCESS! Decoded with {enc}, length: {len(text)}")
                        print("First 500 chars:")
                        print(text[:500])
                        downloaded = True
                        break
                except UnicodeDecodeError:
                    pass
            if downloaded:
                break
    except Exception as e:
        print("Error on", url, ":", e)

if not downloaded:
    print("Could not download directly, saving last response to gdrive_response.bin")
    with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/gdrive_response.bin', 'wb') as f:
        f.write(data)

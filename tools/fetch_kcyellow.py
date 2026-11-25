# -*- coding: utf-8 -*-
import urllib.request

url = "https://raw.githubusercontent.com/BGforgeNet/Fallout2_Restoration_Project/master/scripts_src/klamath/kcyellow.ssl"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode('utf-8')
    with open("E:/FALLOUT Ult pjt/tools/kcyellow.ssl", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Downloaded kcyellow.ssl, length:", len(content))
except Exception as e:
    print("ERROR:", e)

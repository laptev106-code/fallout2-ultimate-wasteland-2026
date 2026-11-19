import os
import urllib.request
import json
import time

headers = {'User-Agent': 'Mozilla/5.0'}

def download_file(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        with open(out_path, 'wb') as f:
            f.write(r.read())

def fetch_gh_folder(repo, folder_path, local_target_dir):
    url = f'https://api.github.com/repos/{repo}/contents/{folder_path}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        items = json.loads(r.read())
    
    for item in items:
        name = item['name']
        t = item['type']
        if t == 'file':
            dl_url = item['download_url']
            dest = os.path.join(local_target_dir, name)
            print(f"Downloading {name} to {dest}...")
            download_file(dl_url, dest)
        elif t == 'dir':
            sub_folder = f"{folder_path}/{name}"
            sub_target = os.path.join(local_target_dir, name)
            fetch_gh_folder(repo, sub_folder, sub_target)

if __name__ == '__main__':
    mods_to_fetch = [
        ('fo2_interface_upscaled.dat', 'fo2_interface_upscaled.dat'),
        ('fo2_pip_timers.dat', 'fo2_pip_timers.dat'),
        ('fo2_footprints', 'fo2_footprints')
    ]
    
    target_base = r'd:\AG games mods\fallout2-ultimate-wasteland-2026\mods'
    for src_folder, dest_folder in mods_to_fetch:
        dest_dir = os.path.join(target_base, dest_folder)
        print(f"=== Fetching {src_folder} -> {dest_dir} ===")
        fetch_gh_folder('rotators/fallout-mods', src_folder, dest_dir)
        print(f"Done {src_folder}!")

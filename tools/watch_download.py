import os
import time
import shutil
import glob

downloads_dir = os.path.expandvars(r'%USERPROFILE%\Downloads')
dest_dir = r'd:\AG games mods\downloads'
os.makedirs(dest_dir, exist_ok=True)

print("Monitoring Downloads folder for incoming Talking Heads archive...")
start_time = time.time()
found_file = None

while time.time() - start_time < 90:
    # Check for crdownload or newly created zip/7z/rar
    crfiles = glob.glob(os.path.join(downloads_dir, '*.crdownload'))
    if crfiles:
        for cr in crfiles:
            size = os.path.getsize(cr)
            print(f"Downloading: {os.path.basename(cr)} ({size / (1024*1024):.2f} MB)...")
    
    # Check for completed files in last 5 minutes
    files = glob.glob(os.path.join(downloads_dir, '*.*'))
    for f in files:
        if f.endswith('.crdownload'):
            continue
        mtime = os.path.getmtime(f)
        if mtime > start_time - 30 and any(k in os.path.basename(f).lower() for k in ['rpu', 'head', 'talking', '45', 'addon']):
            size = os.path.getsize(f)
            if size > 1024 * 1024: # > 1MB
                found_file = f
                break
    if found_file:
        break
    time.sleep(2)

if found_file:
    print(f"Download complete: {found_file} ({os.path.getsize(found_file)/(1024*1024):.2f} MB)")
    dest_path = os.path.join(dest_dir, os.path.basename(found_file))
    shutil.move(found_file, dest_path)
    print(f"Moved immediately to safe Drive D: {dest_path}")
else:
    print("No matching completed download detected within timeout.")

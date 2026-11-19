import zipfile

zip_path = "D:/Downloads/Fallout_Nevada_Sonora/Fallout_Sonora_v1.16.4_Complete.zip"
with zipfile.ZipFile(zip_path, 'r') as z:
    for name in z.namelist():
        if any(k in name.lower() for k in ['blur', 'glass', 'footstep', 'key', 'pixote', 'head', 'shader', 'sfall']):
            print("Sonora:", name)

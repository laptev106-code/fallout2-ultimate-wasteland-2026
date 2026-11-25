import zipfile

with zipfile.ZipFile(r"D:\AG games mods\downloads\miria.zip") as z:
    for n in z.namelist():
        print(n)

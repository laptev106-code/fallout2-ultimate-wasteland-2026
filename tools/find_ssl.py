# -*- coding: utf-8 -*-
import glob
print("ssl count in E:\\FALLOUT Ult pjt:", len(glob.glob(r"E:\FALLOUT Ult pjt\**\*.ssl", recursive=True)))
for p in glob.glob(r"E:\FALLOUT Ult pjt\**\*.ssl", recursive=True)[:20]:
    print(" ", p)

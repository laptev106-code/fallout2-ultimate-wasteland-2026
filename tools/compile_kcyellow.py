# -*- coding: utf-8 -*-
import os, subprocess, ctypes

def get_short_path(path):
    buf = ctypes.create_unicode_buffer(500)
    ctypes.windll.kernel32.GetShortPathNameW(path, buf, 500)
    return buf.value if buf.value else path

tools_dir = get_short_path(r"E:\FALLOUT Ult pjt\tools")
compiler = os.path.join(tools_dir, "compile.exe")

cmd = [
    compiler,
    "-p",
    "-q",
    "-s",
    f"-I{tools_dir}",
    "-O2",
    "kcyellow.ssl",
    "-o",
    "kcyellow.int"
]

print("Running in cwd:", tools_dir)
res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)

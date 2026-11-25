import subprocess
import os

tools_dir = r"e:\FALLOUT Ult pjt\tools"
compiler = os.path.join(tools_dir, "compile.exe")

ssl_code = """
#define SCRIPT_REALNAME "test_gvar"
#include "define.h"
procedure start;
procedure start begin
    set_global_var(50, 1);
    if (global_var(50) == 1) then begin
    end
end
"""
with open(os.path.join(tools_dir, 'test_gvar.ssl'), 'w') as f:
    f.write(ssl_code)

cmd = [
    compiler,
    "-p",
    "-q",
    "-s",
    "-Iheaders",
    "-O2",
    "test_gvar.ssl",
    "-o", "test_gvar.int"
]

res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
with open(os.path.join(tools_dir, 'test_gvar.int'), 'rb') as f:
    data = f.read()
print('Hex bytes:', data.hex())

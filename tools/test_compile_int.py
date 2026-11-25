import subprocess
import os

tools_dir = r"e:\FALLOUT Ult pjt\tools"
compiler = os.path.join(tools_dir, "compile.exe")

ssl_code = """
#define SCRIPT_REALNAME "test_opcodes"
#include "define.h"
procedure talk_p_proc;
procedure talk_p_proc begin
    start_gdialog(999, self_obj, 4, 158, 10);
    gSay_Start;
    gSay_End;
    end_dialogue;
end
"""
with open(os.path.join(tools_dir, 'test_opcodes.ssl'), 'w') as f:
    f.write(ssl_code)

cmd = [
    compiler,
    "-p",
    "-q",
    "-s",
    "-Iheaders",
    "-O2",
    "test_opcodes.ssl",
    "-o", "test_opcodes.int"
]

res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
with open(os.path.join(tools_dir, 'test_opcodes.int'), 'rb') as f:
    data = f.read()
print('Compiled size:', len(data))
print('Hex bytes:', data.hex())

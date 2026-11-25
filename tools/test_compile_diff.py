import subprocess
import os

script1 = """#pragma sce
#include "main.h"

procedure start begin
   variable obj;
   foreach obj in list_as_array(1) begin
      set_outline(obj, 0);
   end
end
"""

with open("tools/test_min.ssl", "w") as f:
    f.write(script1)

compiler = os.path.abspath("tools/compile.exe")
res1 = subprocess.run([compiler, "-q", "-s", "-Iheaders", "test_min.ssl"], cwd="tools", capture_output=True, text=True)
print("Result 1 (with 1):", res1.returncode)
if res1.returncode != 0:
    print(res1.stdout)

script2 = """#pragma sce
#include "sfall.h"

procedure start begin
   variable obj;
   foreach obj in list_as_array(LIST_GROUNDITEMS) begin
      set_outline(obj, 0);
   end
end
"""

with open("tools/test_min2.ssl", "w") as f:
    f.write(script2)

res2 = subprocess.run([compiler, "-q", "-s", "-Iheaders", "test_min2.ssl"], cwd="tools", capture_output=True, text=True)
print("Result 2 (with LIST_GROUNDITEMS):", res2.returncode)
if res2.returncode != 0:
    print(res2.stdout)

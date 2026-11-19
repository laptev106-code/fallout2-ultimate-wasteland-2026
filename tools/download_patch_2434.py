import subprocess
import json
import time
import os

env = os.environ.copy()
env['BSK_AUTO_START'] = '0'
bsk = os.path.expandvars(r'%USERPROFILE%\.local\bin\bsk.exe')

def run_bsk(args):
    cmd = [bsk] + args
    res = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding='utf-8')
    return res.stdout, res.stderr

out, _ = run_bsk(['cooperate', 'sync', '--session', 'yubj'])
idx = out.find('{')
data = json.loads(out[idx:])
obs = data['observation']['text']
print("Observation length:", len(obs))

# Find line with RPU 2.4.34 Patch
lines = obs.splitlines()
target_ref = None
for i, l in enumerate(lines):
    if 'RPU 2.4.34 Patch' in l:
        print("Found patch line:", l)
        for j in range(i, min(len(lines), i + 20)):
            print(f"  [{j}] {lines[j]}")
            if 'button "Manual download"' in lines[j]:
                target_ref = lines[j].split()[0]
                break
        break

print("Target ref:", target_ref)
if target_ref:
    ctx = data['context_id']
    print(f"Clicking {target_ref} with context {ctx}...")
    c_out, _ = run_bsk(['click', '--session', 'yubj', '--context', ctx, '--ref', target_ref])
    print("Click:", c_out)

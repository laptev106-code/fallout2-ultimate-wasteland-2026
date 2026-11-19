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

def sync_and_click(ref):
    out, _ = run_bsk(['cooperate', 'sync', '--session', 'yubj'])
    idx = out.find('{')
    data = json.loads(out[idx:])
    ctx = data['context_id']
    print(f"Context: {ctx}, clicking {ref}...")
    c_out, c_err = run_bsk(['click', '--session', 'yubj', '--context', ctx, '--ref', ref])
    print("Click:", c_out)
    if c_err:
        print("Click err:", c_err)

# Step 1: Click @e158
sync_and_click('@e158')
time.sleep(2)

# Step 2: Observe modal
out, _ = run_bsk(['observe', '--session', 'yubj'])
lines = out.splitlines()
modal_manual = None
for l in lines:
    if 'link "Manual download"' in l:
        modal_manual = l.split()[0]
        break
print("Modal Manual button:", modal_manual)
if modal_manual:
    sync_and_click(modal_manual)
    time.sleep(3)

# Step 3: Observe slow download page
out, _ = run_bsk(['observe', '--session', 'yubj'])
lines = out.splitlines()
slow_btn = None
for l in lines:
    if 'button "Slow download"' in l:
        slow_btn = l.split()[0]
        break
print("Slow download button:", slow_btn)
if slow_btn:
    sync_and_click(slow_btn)
    print("Triggered Slow Download!")

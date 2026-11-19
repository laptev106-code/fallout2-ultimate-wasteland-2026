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
    out, _ = run_bsk(['cooperate', 'sync', '--session', 'fnpt'])
    idx = out.find('{')
    if idx == -1:
        print("No JSON in output:", out)
        return
    data = json.loads(out[idx:])
    ctx = data['context_id']
    print(f"Context: {ctx}, clicking {ref}...")
    click_out, click_err = run_bsk(['click', '--session', 'fnpt', '--context', ctx, '--ref', ref])
    print("Click out:", click_out)
    if click_err:
        print("Click err:", click_err)

if __name__ == '__main__':
    sync_and_click('@e757')

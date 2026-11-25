import subprocess, os, json, time

bsk = os.path.join(os.environ['USERPROFILE'], '.local', 'bin', 'bsk.exe')
file_path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_square_input.png"

def run_bsk(args):
    return subprocess.run([bsk] + args, capture_output=True, text=True, encoding='utf-8', errors='ignore')

def sync():
    res = run_bsk(['cooperate', 'sync', '--session', 'cvkp', '--json'])
    s = res.stdout[res.stdout.find('{'):res.stdout.rfind('}')+1]
    return json.loads(s)

st = sync()
ctx, obs = st['context_id'], st['observation_id']

# 1. Unhide
unhide_js = """
(() => {
  const inp = document.getElementById('upload-avatar-file-input');
  if (inp) {
    inp.style.display = 'block';
    inp.style.visibility = 'visible';
    inp.style.opacity = '1';
    inp.style.position = 'fixed';
    inp.style.top = '100px';
    inp.style.left = '100px';
    inp.style.width = '200px';
    inp.style.height = '50px';
    inp.style.zIndex = '99999';
    return 'unhidden';
  }
  return 'not_found';
})()
"""
ev = run_bsk(['evaluate', unhide_js, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Unhide result:", ev.stdout)

# 2. Sync to update DOM state in bsk
st = sync()
ctx, obs = st['context_id'], st['observation_id']

# 3. Upload file
up = run_bsk(['upload', '--selector', '#upload-avatar-file-input', '--file', file_path, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Upload output:", up.stdout)
if up.stderr:
    print("Upload err:", up.stderr)

time.sleep(5)

# 4. Check DOM state after upload
st = sync()
ctx, obs = st['context_id'], st['observation_id']
page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text after upload:\n", page_text.stdout[:800])

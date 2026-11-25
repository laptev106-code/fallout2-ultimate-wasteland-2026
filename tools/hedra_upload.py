import subprocess, os, json

bsk = os.path.join(os.environ['USERPROFILE'], '.local', 'bin', 'bsk.exe')
file_path = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_square_input.png"

# 1. Sync
res = subprocess.run([bsk, 'cooperate', 'sync', '--session', 'cvkp', '--json'], capture_output=True, text=True)
s = res.stdout[res.stdout.find('{'):res.stdout.rfind('}')+1]
data = json.loads(s)
ctx = data['context_id']
obs = data['observation_id']

# 2. Make input visible
unhide_js = "var inp = document.querySelector('input[type=file]'); if (inp) { inp.style.display = 'block'; inp.style.visibility = 'visible'; inp.style.opacity = '1'; inp.style.position = 'fixed'; inp.style.top = '100px'; inp.style.left = '100px'; inp.style.width = '200px'; inp.style.height = '50px'; inp.style.zIndex = '99999'; 'unhidden'; } else { 'not_found'; }"
ev = subprocess.run([bsk, 'evaluate', unhide_js, '--session', 'cvkp', '--context', ctx, '--observation', obs], capture_output=True, text=True)
print('Unhide result:', ev.stdout)

# 3. Sync again to get new DOM state
res = subprocess.run([bsk, 'cooperate', 'sync', '--session', 'cvkp', '--json'], capture_output=True, text=True)
s = res.stdout[res.stdout.find('{'):res.stdout.rfind('}')+1]
data = json.loads(s)
ctx = data['context_id']
obs = data['observation_id']

# 4. Upload
up = subprocess.run([bsk, 'upload', '--selector', 'input[type=file]', '--file', file_path, '--session', 'cvkp', '--context', ctx, '--observation', obs], capture_output=True, text=True)
print('Upload output:', up.stdout)
if up.stderr:
    print('Upload err:', up.stderr)

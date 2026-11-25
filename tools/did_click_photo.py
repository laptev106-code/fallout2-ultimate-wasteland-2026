import subprocess, os, json, time

bsk = os.path.join(os.environ['USERPROFILE'], '.local', 'bin', 'bsk.exe')

def run_bsk(args):
    return subprocess.run([bsk] + args, capture_output=True, text=True, encoding='utf-8', errors='ignore')

def sync():
    res = run_bsk(['cooperate', 'sync', '--session', 'cvkp', '--json'])
    s = res.stdout[res.stdout.find('{'):res.stdout.rfind('}')+1]
    return json.loads(s)

st = sync()
ctx, obs = st['context_id'], st['observation_id']

# Click @e1075
res = run_bsk(['click', '--ref', '@e1075', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Click Create with photo:", res.stdout, res.stderr)

time.sleep(3)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text after click:\n", page_text.stdout[:600])

files = run_bsk(['evaluate', 'Array.from(document.querySelectorAll("input[type=file]")).map(i => ({id: i.id, accept: i.accept, visible: i.offsetParent !== null}))', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("File inputs:", files.stdout)

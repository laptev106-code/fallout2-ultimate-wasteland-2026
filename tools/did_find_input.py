import subprocess, os, json

bsk = os.path.join(os.environ['USERPROFILE'], '.local', 'bin', 'bsk.exe')

def run_bsk(args):
    return subprocess.run([bsk] + args, capture_output=True, text=True, encoding='utf-8', errors='ignore')

def sync():
    res = run_bsk(['cooperate', 'sync', '--session', 'cvkp', '--json'])
    s = res.stdout[res.stdout.find('{'):res.stdout.rfind('}')+1]
    return json.loads(s)

st = sync()
ctx, obs = st['context_id'], st['observation_id']

js = "Array.from(document.querySelectorAll('input[type=file]')).map(i => ({id: i.id, accept: i.accept, visible: i.offsetParent !== null, className: i.className}))"
res = run_bsk(['evaluate', js, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Inputs:", res.stdout)

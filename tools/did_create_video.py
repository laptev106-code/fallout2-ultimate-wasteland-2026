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

# Click @e720
res = run_bsk(['click', '--ref', '@e720', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Click output:", res.stdout)
if res.stderr:
    print("Click err:", res.stderr)

time.sleep(5)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
url = run_bsk(['evaluate', 'window.location.href', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Studio canvas URL:", url.stdout)

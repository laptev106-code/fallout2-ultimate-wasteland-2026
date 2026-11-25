import subprocess, os, json

bsk = os.path.join(os.environ['USERPROFILE'], '.local', 'bin', 'bsk.exe')

res = subprocess.run([bsk, 'cooperate', 'sync', '--session', 'cvkp', '--json'], capture_output=True, text=True)
s = res.stdout[res.stdout.find('{'):res.stdout.rfind('}')+1]
data = json.loads(s)
ctx = data['context_id']
obs = data['observation_id']

js = "document.querySelectorAll('input[type=file]').length"
ev = subprocess.run([bsk, 'evaluate', js, '--session', 'cvkp', '--context', ctx, '--observation', obs], capture_output=True, text=True)
print('File inputs count:', ev.stdout)

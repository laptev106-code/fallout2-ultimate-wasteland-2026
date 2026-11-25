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

js_change = """
(() => {
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Change');
  if (btn) {
    btn.click();
    return 'clicked Change voice';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_change, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Change voice:", ev.stdout)

time.sleep(3)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
voices = run_bsk(['evaluate', 'Array.from(document.querySelectorAll("[role=dialog], [role=listbox], ul, li")).map(e => e.innerText).slice(0, 5)', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Voices popup:\n", voices.stdout[:600])

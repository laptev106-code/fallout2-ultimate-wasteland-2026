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

js = """
(() => {
  const dialog = document.querySelector('[role="dialog"]');
  if (!dialog) return 'no dialog';
  return Array.from(dialog.querySelectorAll('button')).map(b => ({text: b.innerText, class: b.className, aria: b.getAttribute('aria-label')}));
})()
"""
res = run_bsk(['evaluate', js, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Dialog buttons:", res.stdout)

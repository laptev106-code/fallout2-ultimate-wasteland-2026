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

js_click = """
(() => {
  const btn = Array.from(document.querySelectorAll('button, a')).find(b => b.innerText && b.innerText.includes('Google'));
  if (btn) {
    btn.click();
    return 'clicked Google btn: ' + btn.innerText;
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_click, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Click res:", ev.stdout)

time.sleep(5)

tabs = run_bsk(['tab', 'list', '--session', 'cvkp'])
print("Tabs after click:\n", tabs.stdout)

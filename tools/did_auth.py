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
  const el = document.querySelector('div[data-identifier="laptev106@gmail.com"]');
  if (el) {
    el.click();
    return 'clicked laptev106';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_click, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Click res:", ev.stdout)

time.sleep(6)

st = sync()
ctx, obs = st['context_id'], st['observation_id']

# Check for consent "Продолжить"
js_consent = """
(() => {
  const btn = Array.from(document.querySelectorAll('button, div[role="button"], span')).find(e => e.innerText && e.innerText.trim() === 'Продолжить');
  if (btn) {
    btn.click();
    return 'clicked Продолжить';
  }
  return 'no continue button';
})()
"""
ev2 = run_bsk(['evaluate', js_consent, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Consent res:", ev2.stdout)

time.sleep(6)

tabs = run_bsk(['tab', 'list', '--session', 'cvkp'])
print("Tabs after D-ID login:\n", tabs.stdout)

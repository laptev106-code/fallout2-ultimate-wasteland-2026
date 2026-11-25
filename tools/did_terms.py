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

js_agree = """
(() => {
  const cb = document.querySelector('input[type="checkbox"], [role="checkbox"]');
  if (cb) {
    if (!cb.checked) cb.click();
  }
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Continue'));
  if (btn) {
    btn.click();
    return 'clicked continue';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_agree, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Agree res:", ev.stdout)

time.sleep(5)

# Check DOM
st = sync()
ctx, obs = st['context_id'], st['observation_id']
url = run_bsk(['evaluate', 'window.location.href', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("URL:", url.stdout)
text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text:\n", text.stdout[:600])

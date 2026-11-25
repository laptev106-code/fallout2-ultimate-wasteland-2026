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

js_apply = """
(() => {
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Apply voice'));
  if (btn) {
    btn.click();
    return 'clicked Apply voice';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_apply, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Apply res:", ev.stdout)

time.sleep(3)

# Click Next to move to Behavior/Knowledge/Conversation
st = sync()
ctx, obs = st['context_id'], st['observation_id']
js_next = """
(() => {
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Next');
  if (btn) {
    btn.click();
    return 'clicked Next';
  }
  return 'no next';
})()
"""
ev2 = run_bsk(['evaluate', js_next, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Next res:", ev2.stdout)

time.sleep(3)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text after Next:\n", page_text.stdout[:600])

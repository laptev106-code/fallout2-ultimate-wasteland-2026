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

js_step = """
(() => {
  const el = Array.from(document.querySelectorAll('div, button, span, label')).find(e => e.innerText && e.innerText.trim() === 'Just for fun');
  if (el) el.click();
  
  const next = Array.from(document.querySelectorAll('button')).find(b => b.innerText && (b.innerText.includes('Next') || b.innerText.includes('Finish') || b.innerText.includes('Get Started')));
  if (next) {
    next.click();
    return 'clicked fun & next';
  }
  return 'clicked fun';
})()
"""
ev = run_bsk(['evaluate', js_step, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Step:", ev.stdout)

time.sleep(2)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
# Click Next again if needed
js_next = """
(() => {
  const next = Array.from(document.querySelectorAll('button')).find(b => b.innerText && (b.innerText.includes('Next') || b.innerText.includes('Finish') || b.innerText.includes('Get Started') || b.innerText.includes('Start')));
  if (next) {
    next.click();
    return 'clicked ' + next.innerText;
  }
  return 'no button';
})()
"""
ev2 = run_bsk(['evaluate', js_next, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Next res:", ev2.stdout)

time.sleep(4)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text:\n", text.stdout[:600])

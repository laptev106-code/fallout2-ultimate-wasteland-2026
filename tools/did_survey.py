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

js_pick = """
(() => {
  const cards = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && e.innerText.trim() === 'Youtube');
  if (cards.length > 0) {
    cards[cards.length - 1].click();
  }
  
  setTimeout(() => {
    const done = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Done'));
    if (done) done.click();
  }, 500);
  
  return 'clicked youtube';
})()
"""
ev = run_bsk(['evaluate', js_pick, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Pick res:", ev.stdout)

time.sleep(5)

st = sync()
ctx, obs = st['context_id'], st['observation_id']

# If still disabled, check why
js_done = """
(() => {
  const done = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Done'));
  if (done && !done.disabled) {
    done.click();
    return 'clicked enabled done';
  }
  return done ? 'done is disabled: ' + done.outerHTML : 'no done';
})()
"""
ev2 = run_bsk(['evaluate', js_done, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Done res:", ev2.stdout)

time.sleep(5)
text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Text:\n", text.stdout[:600])

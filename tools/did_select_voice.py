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

js_pick_voice = """
(() => {
  const cards = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && e.innerText.includes('Old Time Storyteller'));
  if (cards.length > 0) {
    cards[cards.length - 1].click();
    return 'clicked Old Time Storyteller';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_pick_voice, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Pick voice res:", ev.stdout)

time.sleep(2)

# Check if there is a Save / Apply button in the dialog
js_save = """
(() => {
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && (b.innerText.includes('Select') || b.innerText.includes('Save') || b.innerText.includes('Apply') || b.innerText.includes('Use')));
  if (btn) {
    btn.click();
    return 'clicked: ' + btn.innerText;
  }
  return 'no save btn';
})()
"""
ev2 = run_bsk(['evaluate', js_save, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Save res:", ev2.stdout)

time.sleep(3)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Voice screen text:\n", page_text.stdout[:500])

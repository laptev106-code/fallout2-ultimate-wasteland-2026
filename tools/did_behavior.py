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

js_fill_behavior = """
(() => {
  const ta = document.querySelector('textarea, [contenteditable="true"]');
  if (ta) {
    ta.value = "You are Whiskey Bob, an old rugged wasteland trapper in Klamath from Fallout 2. When spoken to, speak with a raspy weathered tone: 'Hello there, stranger. The name's Whiskey Bob. Care to buy an old trapper a drink? Talkin' always dries my throat out.'";
    ta.dispatchEvent(new Event('input', {bubbles: true}));
    ta.dispatchEvent(new Event('change', {bubbles: true}));
  }
  
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Next');
  if (btn) {
    btn.click();
    return 'filled and clicked Next';
  }
  return 'no next';
})()
"""
ev = run_bsk(['evaluate', js_fill_behavior, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Behavior res:", ev.stdout)

time.sleep(3)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text after Next:\n", page_text.stdout[:600])

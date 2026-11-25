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

js_finish = """
(() => {
  // Fill greeting input
  const inp = document.querySelector('input[type="text"], textarea, [contenteditable="true"]');
  if (inp) {
    inp.value = "Hello there, stranger. The name's Whiskey Bob. Care to buy an old trapper a drink? Talkin' always dries my throat out.";
    inp.dispatchEvent(new Event('input', {bubbles: true}));
    inp.dispatchEvent(new Event('change', {bubbles: true}));
  }
  
  // Click Create agent
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Create agent'));
  if (btn) {
    btn.click();
    return 'filled greeting and clicked Create agent';
  }
  return 'button not found';
})()
"""
ev = run_bsk(['evaluate', js_finish, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Finish res:", ev.stdout)

time.sleep(6)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
url = run_bsk(['evaluate', 'window.location.href', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Final URL:", url.stdout)

page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text after creation:\n", page_text.stdout[:800])

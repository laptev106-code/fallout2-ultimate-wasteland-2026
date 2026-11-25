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

js_trigger = """
(() => {
  const inp = document.getElementById('upload-avatar-file-input');
  if (inp && inp.files && inp.files.length > 0) {
    inp.dispatchEvent(new Event('change', {bubbles: true}));
    return 'dispatched change event with ' + inp.files[0].name;
  }
  return inp ? 'inp has no files: ' + inp.files.length : 'no inp';
})()
"""
ev = run_bsk(['evaluate', js_trigger, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Trigger result:", ev.stdout)

time.sleep(5)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
page_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Page text after trigger:\n", page_text.stdout[:800])

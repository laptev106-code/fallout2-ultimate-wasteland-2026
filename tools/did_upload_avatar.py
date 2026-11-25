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

js_create_av = """
(() => {
  const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Create Avatar'));
  if (btn) {
    btn.click();
    return 'clicked Create Avatar';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_create_av, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Create avatar res:", ev.stdout)

time.sleep(3)

# Check file inputs
st = sync()
ctx, obs = st['context_id'], st['observation_id']
files = run_bsk(['evaluate', 'Array.from(document.querySelectorAll("input[type=file]")).map(i => ({id: i.id, accept: i.accept, visible: i.offsetParent !== null}))', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("File inputs:", files.stdout)

dialog_text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Dialog text:\n", dialog_text.stdout[:600])

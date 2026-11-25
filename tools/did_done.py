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

js_done = """
(() => {
  const opt = Array.from(document.querySelectorAll('div, button, span, label')).find(e => e.innerText && e.innerText.includes('ChatGPT'));
  if (opt) opt.click();
  
  const done = Array.from(document.querySelectorAll('button')).find(b => b.innerText && (b.innerText.includes('Done') || b.innerText.includes('Start')));
  if (done) {
    done.click();
    return 'clicked done: ' + done.innerText;
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js_done, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Done res:", ev.stdout)

time.sleep(5)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
url = run_bsk(['evaluate', 'window.location.href', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Studio URL:", url.stdout)

text = run_bsk(['evaluate', 'document.body.innerText', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Studio text:\n", text.stdout[:600])

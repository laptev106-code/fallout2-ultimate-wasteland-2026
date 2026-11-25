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

js = """
(() => {
  // Dismiss got it
  const gotIt = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Got it'));
  if (gotIt) gotIt.click();
  
  // Click Avatar Video
  const av = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Avatar Video'));
  if (av) {
    av.click();
    return 'clicked Avatar Video';
  }
  return 'not found';
})()
"""
ev = run_bsk(['evaluate', js, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Res:", ev.stdout)

time.sleep(5)

st = sync()
ctx, obs = st['context_id'], st['observation_id']
url = run_bsk(['evaluate', 'window.location.href', '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("URL:", url.stdout)

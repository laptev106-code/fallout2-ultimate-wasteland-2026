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
  const imgs = Array.from(document.querySelectorAll('img')).map(i => ({src: i.src.slice(0, 80), alt: i.alt, className: i.className}));
  const sel = document.querySelector('[aria-selected="true"], [data-selected="true"], .selected');
  return {
    imgs: imgs.slice(0, 10),
    selected: sel ? sel.outerHTML.slice(0, 150) : null
  };
})()
"""
res = run_bsk(['evaluate', js, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("DOM check:", res.stdout)

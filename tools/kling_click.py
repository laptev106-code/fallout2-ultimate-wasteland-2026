import subprocess, os, json

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
  const dialog = document.querySelector('dialog, [role="dialog"], .ant-modal, .modal');
  if (!dialog) return 'no dialog found';
  const closeBtn = dialog.querySelector('button, [aria-label*="close" i], [class*="close" i]');
  if (closeBtn) {
    closeBtn.click();
    return 'clicked close: ' + closeBtn.outerHTML.slice(0, 100);
  }
  return 'dialog HTML: ' + dialog.innerHTML.slice(0, 300);
})()
"""
res = run_bsk(['evaluate', js, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Res:", res.stdout)

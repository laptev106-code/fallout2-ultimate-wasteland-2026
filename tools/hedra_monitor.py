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

js_status = """
(() => {
  const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, [role="heading"], p, span'))
    .map(e => e.innerText)
    .filter(t => t && (t.includes('Анализ') || t.includes('Генерация') || t.includes('слои') || t.includes('Generating') || t.includes('Rendering') || t.includes('Ready') || t.includes('Готово') || t.includes('%') || t.includes('Остановить')));
  
  const videos = Array.from(document.querySelectorAll('video')).map(v => ({src: v.src, currentSrc: v.currentSrc, duration: v.duration, readyState: v.readyState}));
  
  return {
    status_snippets: Array.from(new Set(headings)).slice(0, 10),
    videos: videos
  };
})()
"""
res = run_bsk(['evaluate', js_status, '--session', 'cvkp', '--context', ctx, '--observation', obs])
print("Progress check:", res.stdout)

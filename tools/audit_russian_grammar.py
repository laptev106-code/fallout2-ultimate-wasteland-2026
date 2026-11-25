import sys, os, re
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
ru_dialogs = [k for k in vfs if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]

typo_patterns = [
    (r'\bсдесь\b', 'здесь'),
    (r'\bлудше\b', 'лучше'),
    (r'\bвообщем\b', 'в общем'),
    (r'\bврядли\b', 'вряд ли'),
    (r'\bпока-что\b', 'пока что'),
    (r'\bкое кто\b', 'кое-кто'),
    (r'\bкое что\b', 'кое-что'),
    (r'\bкак раз таки\b', 'как-раз-таки / как раз'),
]

results = {}

for d in ru_dialogs:
    txt, _ = efa.read_vfs_text(vfs[d])
    if not txt: continue
    for pat, fix in typo_patterns:
        for m in re.finditer(pat, txt, re.IGNORECASE):
            # Extract line context
            start = max(0, m.start() - 20)
            end = min(len(txt), m.end() + 20)
            snippet = txt[start:end].replace('\r', '').replace('\n', ' ')
            results.setdefault(d, []).append((m.group(0), fix, snippet))

print(f"Total files with prominent grammatical typos: {len(results)}")
for d, occurrences in list(results.items())[:15]:
    print(f"\n=== {d} ({len(occurrences)} typos) ===")
    for word, fix, snip in occurrences[:3]:
        print(f"  '{word}' -> '{fix}' | Context: ...{snip}...")

with open("tools/diff_ai_sections.py", "r", encoding="utf-8-sig") as f:
    code = f.read()

exec(code)

sections_to_show = ["[PARTY MARIA AGGRESSIVE]", "[PARTY MARIA BERSERK]", "[PARTY MARIA COWARD]", "[PARTY MARIA CUSTOM]", "[PARTY MARIA DEFENSIVE]"]
for s in sections_to_show:
    print("="*40)
    print("MIRIA DAT:", s)
    print("\n".join(sec_m[s]))
    print("-"*20)
    print("ECCO DAT:", s)
    print("\n".join(sec_e[s]))

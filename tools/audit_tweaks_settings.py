import os, sys, configparser

print('=== AUDIT: FO2TWEAKS & DDRAW CONFIG COMPARISON ===')

def check_configs(pname, pdir):
    print(f'\n--- Profile: {pname} ---')
    fo2_ini = os.path.join(pdir, 'mods', 'fo2tweaks.ini')
    if not os.path.exists(fo2_ini):
        fo2_ini = os.path.join(pdir, 'fo2tweaks.ini')
    print('fo2tweaks.ini path:', fo2_ini, 'exists:', os.path.exists(fo2_ini))
    
    if os.path.exists(fo2_ini):
        with open(fo2_ini, 'r', encoding='latin1') as f:
            lines = f.readlines()
        active_tweaks = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith(';') and '=' in line:
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                if v not in ('0', ''):
                    active_tweaks.append((k, v))
        print(f'Active tweaks count: {len(active_tweaks)}')
        for k, v in active_tweaks:
            print(f'  {k} = {v}')

check_configs('Gameplay', r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
check_configs('HD', r'E:\Fallout2_Ultimate\Fallout2_HD')

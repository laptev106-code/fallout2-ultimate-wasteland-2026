for p in [r'E:\Fallout2_Ultimate\Fallout2_Gameplay\ddraw.ini', r'E:\Fallout2_Ultimate\Fallout2_HD\ddraw.ini']:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'TempleTutorial=' not in c:
        with open(p, 'a', encoding='utf-8') as f:
            f.write('\nTempleTutorial=1\n')
        print('Added TempleTutorial=1 to', p)
    else:
        print('Already in', p)

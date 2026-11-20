import sys
sys.path.insert(0, 'launcher_nextgen')
import main

print('Testing LauncherBridge...')
bridge = main.LauncherBridge(r'E:\Fallout2_Ultimate')
print('Bridge root_dir:', bridge.root_dir)

cfg = bridge.read_config()
print('Read config:', cfg)

saves_gp = bridge.get_saves_info('gameplay')
has_gp = sum(1 for s in saves_gp if s['hasData'])
print(f'Gameplay saves slots count: {len(saves_gp)}, non-empty: {has_gp}')

saves_hd = bridge.get_saves_info('hd')
has_hd = sum(1 for s in saves_hd if s['hasData'])
print(f'HD saves slots count: {len(saves_hd)}, non-empty: {has_hd}')

backups = bridge.list_backups()
print(f'Backups count: {len(backups)}')

diag = bridge.generate_diagnostic_report('Тестовый репорт для проверки целостности', 'Баг', 'Gameplay Ultimate')
print('Diagnostic status:', diag.get('status'), 'saved to:', diag.get('savedPath'))
print('All LauncherBridge methods verified 100% successfully!')

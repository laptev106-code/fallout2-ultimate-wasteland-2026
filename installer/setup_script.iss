; ==============================================================================
; Fallout 2: Ultimate Wasteland Edition 2026 // Master Installer Script
; Inno Setup 6 Script (Ultra LZMA2 Solid Compression)
; ==============================================================================

#define MyAppName "Fallout 2: Ultimate Wasteland Edition"
#define MyAppVersion "2026 Director's Cut (v4.4.8 / RPU v28)"
#define MyAppPublisher "Wasteland 2026 Community"
#define MyAppExeName "Fallout2_NextGen_Launcher.exe"

[Setup]
AppId={{5E285641-7FEA-4C2E-8E5A-7C5BD58EA920}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=D:\Games\Fallout2_Ultimate
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=E:\Fallout2_Dist
OutputBaseFilename=Setup_Fallout2_Ultimate_2026
SetupIconFile=app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
InternalCompressLevel=ultra64
LZMAUseSeparateProcess=yes
WizardStyle=modern
DisableWelcomePage=no
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Types]
Name: "full"; Description: "Полная установка (Рекомендуется: оба профиля Gameplay + HD)"
Name: "gameplay"; Description: "Только Gameplay Ultimate (sfall 4.4.8 + RPU v28 + 24 мода + студийный звук)"
Name: "hd"; Description: "Только Rework HD Community Edition (C++ SDL2 + свет Dustlight + 2K/4K)"
Name: "custom"; Description: "Выборочная установка"; Flags: iscustom

[Components]
Name: "launcher"; Description: "Мастер-лаунчер Pip-Boy Next-Gen и конфигуратор графики"; Types: full gameplay hd custom; Flags: fixed
Name: "gameplay"; Description: "Профиль 'Gameplay Ultimate' (Восстановленные города, броня напарников, 3D-голова Кэссиди, звук 44.1 кГц, баллистика, фиксы сюжетных дыр)"; Types: full gameplay custom
Name: "hd"; Description: "Профиль 'Rework HD' (Открытый C++ движок SDL2, динамический свет Dustlight, субпиксельная камера, 2K/4K)"; Types: full hd custom
Name: "survival"; Description: "Режим хардкорного выживания (Голод, жажда, усталость/сон и готовка у костров)"; Flags: dontinheritcheck

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на &Рабочем столе"; GroupDescription: "Дополнительные ярлыки:"; Flags: checkedonce
Name: "startmenuicon"; Description: "Создать ярлыки в меню &Пуск"; GroupDescription: "Дополнительные ярлыки:"; Flags: checkedonce

[Files]
; Документация, манифест сборки, протоколы аудита и ченджлог
Source: "E:\Fallout2_Ultimate\MASTER_CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\ENGINE_AUDIT_PROTOCOL.md"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\FALLOUT_LORE_CANON.md"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\PROJECT_MAP.md"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\Docs\*"; DestDir: "{app}\Docs"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: launcher

; 1. Главный Next-Gen Лаунчер и интерфейс
Source: "E:\Fallout2_Ultimate\Fallout2_NextGen_Launcher.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\Run_NextGen_Launcher.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\launcher_nextgen\*"; DestDir: "{app}\launcher_nextgen"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: launcher

; 2. Запасной ретро-лаунчер Pip-Boy (Tkinter CRT)
Source: "E:\Fallout2_Ultimate\Fallout2_PipBoy_Launcher.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\Run_Launcher.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: launcher

; 3. Профиль Gameplay Ultimate (полный рабочий билд с модами и фиксами)
Source: "E:\Fallout2_Ultimate\Fallout2_Gameplay\*"; DestDir: "{app}\Fallout2_Gameplay"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.log,*.tmp,*.bak"; Components: gameplay

; 4. Профиль HD Community Edition (C++ движок и шейдеры)
Source: "E:\Fallout2_Ultimate\Fallout2_HD\*"; DestDir: "{app}\Fallout2_HD"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.log,*.tmp,*.bak"; Components: hd

[Icons]
; Ярлык на Рабочем столе для запуска главного лаунчера
Name: "{autodesktop}\Fallout 2 Ultimate 2026"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Ярлыки в меню Пуск
Name: "{group}\{#MyAppName} (Мастер-Лаунчер)"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{group}\Список изменений (Changelog)"; Filename: "{app}\MASTER_CHANGELOG.md"; Tasks: startmenuicon
Name: "{group}\Запуск Gameplay Ultimate (sfall)"; Filename: "{app}\Fallout2_Gameplay\fallout2.exe"; WorkingDir: "{app}\Fallout2_Gameplay"; Components: gameplay; Tasks: startmenuicon
Name: "{group}\Запуск Rework HD (Dustlight SDL2)"; Filename: "{app}\Fallout2_HD\dustlight.exe"; WorkingDir: "{app}\Fallout2_HD"; Components: hd; Tasks: startmenuicon
Name: "{group}\Удалить {#MyAppName}"; Filename: "{uninstallexe}"; Tasks: startmenuicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Запустить лаунчер Fallout 2 Ultimate 2026"; Flags: nowait postinstall skipifsilent

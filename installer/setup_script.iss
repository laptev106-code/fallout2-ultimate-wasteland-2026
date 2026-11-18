; Script generated for Fallout 2: Ultimate Wasteland Edition 2026
; Inno Setup 6 Script

#define MyAppName "Fallout 2 - Ultimate Wasteland Edition 2026"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Wasteland 2026 Team"
#define MyAppExeName "Fallout2_Launcher.exe"

[Setup]
AppId={{5E285641-7FEA-4C2E-8E5A-7C5BD58EA920}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=C:\Games\Fallout2_Ultimate
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=E:\Fallout2_Dist
OutputBaseFilename=Setup_Fallout2_Ultimate_2026
SetupIconFile=app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/normal
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Types]
Name: "full"; Description: "Полная установка (Оба профиля: Gameplay + HD Visual)"
Name: "gameplay"; Description: "Только классический Gameplay Ultimate (sfall 4.4 + RPU + EcCo + Озвучка)"
Name: "hd"; Description: "Только HD Visual Dustlight (Движок C++ + 4x нейротекстуры + свет)"
Name: "custom"; Description: "Выборочная установка"; Flags: iscustom

[Components]
Name: "launcher"; Description: "Автономный мастер-лаунчер Pip-Boy с каталогом модов"; Types: full gameplay hd custom; Flags: fixed
Name: "gameplay"; Description: "Профиль 'Gameplay Ultimate' (Каноничный RPU v28, боевка EcCo, напарники B-Team, звук Mark Morgan)"; Types: full gameplay custom
Name: "hd"; Description: "Профиль 'HD Visual Dustlight' (Движок Fallout 2 Community Edition, AI 4x-текстуры, свет Direct3D 11)"; Types: full hd custom

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на &Рабочем столе"; GroupDescription: "Дополнительные ярлыки:"; Flags: checkedonce
Name: "startmenuicon"; Description: "Создать ярлыки в меню &Пуск"; GroupDescription: "Дополнительные ярлыки:"; Flags: checkedonce

[Files]
Source: "E:\Fallout2_Ultimate\Fallout2_Launcher.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher
Source: "E:\Fallout2_Ultimate\Run_Launcher.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: launcher

Source: "E:\Fallout2_Ultimate\Fallout2_Gameplay\*"; DestDir: "{app}\Fallout2_Gameplay"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.log,*.tmp,*.bak"; Components: gameplay

Source: "E:\Fallout2_Ultimate\Fallout2_HD\*"; DestDir: "{app}\Fallout2_HD"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.log,*.tmp,*.bak"; Components: hd

[Icons]
Name: "{autodesktop}\Fallout 2 Launcher"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{group}\{#MyAppName} - Лаунчер"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{group}\Fallout 2 (Gameplay Ultimate)"; Filename: "{app}\Fallout2_Gameplay\fallout2.exe"; WorkingDir: "{app}\Fallout2_Gameplay"; Components: gameplay; Tasks: startmenuicon
Name: "{group}\Fallout 2 (HD Dustlight)"; Filename: "{app}\Fallout2_HD\dustlight.exe"; WorkingDir: "{app}\Fallout2_HD"; Components: hd; Tasks: startmenuicon
Name: "{group}\Удалить {#MyAppName}"; Filename: "{uninstallexe}"; Tasks: startmenuicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Запустить Fallout 2 Launcher"; Flags: nowait postinstall skipifsilent
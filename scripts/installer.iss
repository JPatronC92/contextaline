; Requiere Inno Setup (iscc.exe)
#define MyAppName "Julio Devs — Document Intelligence"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Julio Devs"
#define MyAppExeName "IntelligentDocumentFinder.exe"

[Setup]
AppId={{7ED4C2B2-0A5D-4E39-9D10-5F86B4C8A7CD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\JulioDevs\DocumentIntelligence
DefaultGroupName=Julio Devs
DisableDirPage=no
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
; Include version in filename to avoid replacing a locked file
OutputBaseFilename=DocumentIntelligence_Setup_{#MyAppVersion}
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "..\dist\IntelligentDocumentFinder\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent

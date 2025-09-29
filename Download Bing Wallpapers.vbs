Set objShell = CreateObject("Wscript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get folder where this VBS is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Command to run inside PowerShell
cmd = "python .\Download_Bing_Wallpapers.py"

' Build full Windows Terminal launch command with startingDirectory
terminalCmd = "wt.exe -d """ & scriptDir & """ powershell -NoExit -ExecutionPolicy Bypass -Command " & Chr(34) & cmd & Chr(34)

' Run Windows Terminal with the correct working directory
objShell.Run terminalCmd, 1, True

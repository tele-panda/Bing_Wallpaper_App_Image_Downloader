Set objShell = CreateObject("Wscript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Full path to Python file
pyFile = "Download_Bing_Wallpapers.py"

' Get the folder where the Python file resides (project directory)
projectDir = fso.GetParentFolderName(pyFile)

' Default command: pip + requirements.txt
cmd = "pip install -r requirements.txt & python " & pyFile

' Check if uv exists
On Error Resume Next
uvCheck = objShell.Run("uv --version", 0, True)
If Err.Number = 0 Then
    ' uv exists — use uv run instead
    cmd = "uv run python " & pyFile
End If
On Error GoTo 0

' Launch Windows Terminal starting in the project directory
terminalCmd = "wt.exe -d """ & projectDir & """ powershell -NoExit -ExecutionPolicy Bypass -Command " & Chr(34) & cmd & Chr(34)

' Run
objShell.Run terminalCmd, 1, True

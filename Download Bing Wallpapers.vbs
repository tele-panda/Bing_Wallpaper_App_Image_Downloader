Set objShell = CreateObject("Wscript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
Set args = WScript.Arguments
Set env = objShell.Environment("PROCESS")

pyFile = ".\Download_Bing_Wallpapers.py"

If Not fso.FileExists(pyFile) Then
    ' If not, fallback: resolve relative to VBS script location
    scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)
    pyFile = fso.BuildPath(scriptFolder, fso.GetFileName(pyFile))
End If

If Not fso.FileExists(pyFile) Then
    MsgBox "Python file not found: " & pyFile & vbCrLf & _
        "Please correct the path in the VBS script.", vbCritical, "File Not Found"
    WScript.Quit 1
End If

projectDir = fso.GetParentFolderName(pyFile)
logFile = fso.BuildPath(projectDir, "run.log")

interactive = True
If args.Count > 0 Then
    Select Case LCase(args(0))
        Case "/quiet", "/silent", "/background"
            interactive = False
    End Select
End If

' --- Check if uv exists ---
On Error Resume Next
uvCheck = objShell.Run("cmd.exe /c where uv >nul 2>&1", 0, True)
On Error GoTo 0

If uvCheck = 0 Then
    scriptCmd = "uv run python """ & pyFile & """"
Else
    scriptCmd = "pip install -r requirements.txt && python """ & pyFile & """"
End If

terminalCmd = "cmd.exe /c cd /d """ & projectDir & """ && " & scriptCmd

If interactive Then
    ' Interactive mode: change /c to /k so terminal stays open
    terminalCmd = Replace(terminalCmd, "/c", "/k")
    env("BING_INTERACTIVE") = "1"
    objShell.Run terminalCmd, 1, True
Else
    ' Non-interactive: append log redirection
    terminalCmd = terminalCmd & " > """ & logFile & """ 2>&1"
    env("BING_INTERACTIVE") = "0"
    objShell.Run terminalCmd, 0, False
End If
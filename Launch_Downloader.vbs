' Silent double-click entry — no CMD/PowerShell window flash.
' Shortcuts should target this file (icon set via install_shortcuts.ps1).
Option Explicit

Dim sh, fso, root, ps1, cmd
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(WScript.ScriptFullName)
ps1 = root & "\Launch.ps1"

If Not fso.FileExists(ps1) Then
  MsgBox "Launch.ps1 not found next to Launch_Downloader.vbs", vbCritical, "FitGirl Downloader"
  WScript.Quit 1
End If

' 0 = hidden window, False = do not wait
cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & ps1 & """"
sh.Run cmd, 0, False

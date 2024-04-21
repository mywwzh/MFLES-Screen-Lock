@echo off
setlocal

certutil -user -addstore Root "CA.cer"

set /p "door_number=duid:"
echo %door_number%>>config.ini
xcopy /E /I "%~dp0*" "c:\screenlock"
attrib +h +a +s +r "c:\screenlock"
attrib +h +a +s +r "c:\screenlock\_internal"
attrib +h +a +s +r "c:\screenlock\config.ini"
attrib +h +a +s +r "c:\screenlock\mslkp.exe"
attrib +h +a +s +r "c:\screenlock\mainui.exe"
attrib +h +a +s +r "c:\screenlock\sync.exe"

del "c:\screenlock\install.bat"
del "c:\screenlock\uninstall.bat"
set "shortcut_path=%userprofile%\Desktop\下课锁屏.lnk"
set "target_path=c:\screenlock\screenlock.exe"
set "icon_path=c:\screenlock\screenlock.exe"
set "description=下课锁屏"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut_path%'); $Shortcut.TargetPath = '%target_path%';$Shortcut.IconLocation = '%icon_path%'; $Shortcut.Description = '%description%'; $Shortcut.Save()"

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "screenlock" /t REG_SZ /d "c:\screenlock\screenlock.exe" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Windows MSL Service" /t REG_SZ /d "c:\screenlock\mslkp.exe" /f

echo 安装完成!!!
pause


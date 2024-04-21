taskkill /f /im status.exe
taskkill /f /im screenlock.exe
taskkill /f /im mainui.exe
taskkill /f /im sync.exe
net stop "Windows MSL Service"
taskkill /f /im mslkp.exe
attrib -h -a -s -r "c:\screenlock"
attrib -h -a -s -r "c:\screenlock\_internal"
attrib -h -a -s -r "c:\screenlock\config.ini"
attrib -h -a -s -r "c:\screenlock\mslkp.exe"
attrib -h -a -s -r "c:\screenlock\mainui.exe"
attrib -h -a -s -r "c:\screenlock\sync.exe"
del /S /Q /F C:\screenlock\_internal
del /S /Q /F C:\screenlock
rmdir C:\screenlock\_internal\*
rmdir C:\screenlock\*
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "screenlock" /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Windows MSL Service" /f

@echo off
setlocal

certutil -user -addstore Root "CA.cer"

REM 步骤1：提示用户输入门牌号，写入config.ini
set /p "door_number=请输入门牌号: "
echo %door_number%>>config.ini

REM 步骤2：拷贝当前目录及其子目录下的所有文件至c:\screenlock
xcopy /E /I "%~dp0*" "c:\screenlock"

REM 步骤3：设置c:\screenlock隐藏属性
attrib +h +a +s +r "c:\screenlock"

REM 步骤4：创建快捷方式至桌面
set "shortcut_path=%userprofile%\Desktop\下课锁屏.lnk"
set "target_path=c:\screenlock\screenlock.exe"
set "icon_path=c:\screenlock\screenlock.exe"
set "description=下课锁屏"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut_path%'); $Shortcut.TargetPath = '%target_path%';$Shortcut.IconLocation = '%icon_path%'; $Shortcut.Description = '%description%'; $Shortcut.Save()"

REM 步骤5：添加注册表开机自启动项
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "screenlock" /t REG_SZ /d "c:\screenlock\screenlock.exe" /f

echo 安装完成！
pause

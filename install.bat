@echo off
setlocal

certutil -user -addstore Root "CA.cer"

REM ����1����ʾ�û��������ƺţ�д��config.ini
set /p "door_number=���������ƺ�: "
echo %door_number%>>config.ini

REM ����2��������ǰĿ¼������Ŀ¼�µ������ļ���c:\screenlock
xcopy /E /I "%~dp0*" "c:\screenlock"

REM ����3������c:\screenlock��������
attrib +h +a +s +r "c:\screenlock"

REM ����4��������ݷ�ʽ������
set "shortcut_path=%userprofile%\Desktop\�¿�����.lnk"
set "target_path=c:\screenlock\screenlock.exe"
set "icon_path=c:\screenlock\screenlock.exe"
set "description=�¿�����"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut_path%'); $Shortcut.TargetPath = '%target_path%';$Shortcut.IconLocation = '%icon_path%'; $Shortcut.Description = '%description%'; $Shortcut.Save()"

REM ����5�����ע�������������
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "screenlock" /t REG_SZ /d "c:\screenlock\screenlock.exe" /f

echo ��װ��ɣ�
pause

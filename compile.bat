@echo off
setlocal

echo Compiling MFLES Screen Lock v1.2.0...

timeout 5

echo Compiling mainui.exe...
pyinstaller -w main.py --version-file main.txt -i Copilot.ico -n mainui
echo mainui.py compiled successfully!

timeout 2
echo Compiling sync.exe...
pyinstaller -w status.py --version-file status.txt -i Teams.ico -n sync
echo sync.py compiled successfully!

timeout 2
echo Compiling mslkp.exe...
pyinstaller -w mslkp.py --version-file mslkp.txt -i WindowsBackup.ico -n mslkp
echo mslkp.exe compiled successfully!

timeout 2
echo Compiling screenlock.exe...
pyinstaller -w screenlock.py --version-file screenlock.txt -i mfles.ico -n screenlock
echo screenlock.exe compiled successfully!
@echo off
setlocal

echo Compiling MFLES Screen Lock v1.2.0...

timeout /nobreak 5

echo install requiements...

pip install -r requiements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

timeout /nobreak 2
echo Compiling mainui.exe...
timeout /nobreak 2
pyinstaller -w main.py --version-file main.txt -i Copilot.ico -n mainui --noconfirm
echo mainui.py compiled successfully!

timeout /nobreak 2
echo Compiling sync.exe...
timeout /nobreak 2
pyinstaller -w status.py --version-file status.txt -i Teams.ico -n sync --noconfirm
echo sync.py compiled successfully!

timeout /nobreak 2
echo Compiling mslkp.exe...
timeout /nobreak 2
pyinstaller -w mslkp.py --version-file mslkp.txt -i WindowsBackup.ico -n mslkp --noconfirm
echo mslkp.exe compiled successfully!

timeout /nobreak 2
echo Compiling screenlock.exe...
timeout /nobreak 2
pyinstaller -w screenlock.py --version-file screenlock.txt -i mfles.ico -n screenlock --noconfirm
echo screenlock.exe compiled successfully!

echo compile successfully!!!

pause
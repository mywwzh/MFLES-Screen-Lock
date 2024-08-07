# MFLES Screen Lock

## 简介
这是一个使用Python的Tkinter库创建的锁屏应用程序。

服务端请见`server`分支。

## 背景
希沃管家的锁屏功能过于弱鸡，很容易被解锁，大量学生在破解后玩儿电脑，因此需要一个更安全的锁屏方式。

## 主要功能

1. **生成随机密码**：应用程序会生成一个6位数的随机密码，用于解锁屏幕。
2. **显示二维码**：应用程序会生成一个包含随机密码的二维码，并在屏幕上显示。
3. **输入密码解锁**：用户可以通过键盘输入密码来解锁屏幕。
4. **防止非法关闭**: 应用程序会阻止用户通过任务栏或任务管理器关闭应用程序。

## 技术细节

1. **Tkinter库**：应用程序使用Tkinter库来创建图形用户界面。这包括全屏窗口、二维码标签、密码标签和键盘按钮。
2. **qrcode库**：应用程序使用qrcode库来生成二维码。
3. **requests库**：应用程序使用requests库来发送HTTP请求，检查是否需要锁屏。
4. **ctypes库**：应用程序使用ctypes库来调用Windows API，使窗口始终置顶。
5. **threading库**：应用程序使用threading库来创建多线程，一个线程用于显示锁屏窗口，另一个线程用于检查是否需要锁屏。

## 截图

![image](https://github.com/user-attachments/assets/d9b5846b-78f3-4450-8805-7ec10782adf2)

![image](https://github.com/user-attachments/assets/dd60a64b-8a0f-4faa-9a1c-72156a71d06c)


## 使用方法

### 安装依赖
使用pip安装所需的库：

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
### 编译程序
在命令行中运行以下命令：

```
compile.bat
```

### 添加启动项
将`screenlock.exe`添加到启动项中，以便在计算机启动时自动运行该程序。

运行程序后，屏幕将被锁定，显示一个二维码。用户需要扫描二维码获取密码，然后通过键盘输入密码来解锁屏幕。

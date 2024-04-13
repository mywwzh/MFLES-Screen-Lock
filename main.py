import tkinter as tk
from PIL import ImageTk
import random
import qrcode
import sys
import ctypes
import requests as r
import uuid
import json
import base64
import time
import os
import subprocess
import psutil

machine_uuid = str(uuid.UUID(int=uuid.getnode()))
random_password = ''.join(random.choices('0123456789', k=6))  # 生成6位随机验证码
try:
    f = open('C:/screenlock/config.ini', 'r', encoding='utf-8')
    addr = f.readline().strip()  # 读取配置的门牌号
    f.close()
except:
    addr = "获取失败"

try:
    admin_password = r.get("[your_url]/select_admin_password.php", verify=False).text 
except:
    pass 
    

def check_process_exists(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def set_always_on_top(root):
    """
    窗口强制置顶
    """
    root.attributes("-topmost", True)
    ctypes.windll.user32.SetWindowPos(root.winfo_id(), -1, 0, 0, 0, 0, 0x0001)


def ignore_close_windows():
    """
    空函数，绑定在窗口关闭事件上来禁用窗口关闭
    """
    pass


class LockScreenApp:
    def __init__(self, master):
        # 初始化函数，将参数master传递给类的成员变量
        self.master = master
        # 设置窗口标题
        self.master.title("Lock Screen")
        # 设置窗口大小
        self.master.geometry(
            "{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        # 设置窗口为全屏
        self.master.attributes('-fullscreen', True)
        # 创建一个背景标签，填充整个窗口
        self.background_label = tk.Label(master, bg="lightblue")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 生成一个二维码图片
        self.qr_code_image = self.generate_qr_code()
        # 将二维码图片转换为PhotoImage对象
        self.qr_code_photo = ImageTk.PhotoImage(self.qr_code_image)
        # 创建一个二维码标签，显示二维码图片
        self.qr_code_label = tk.Label(master, image=self.qr_code_photo)
        self.qr_code_label.place(x=300, y=master.winfo_screenheight() // 3)
        self.copyright_label = tk.Label(
            master, text="MFLES Screen Lock v1.1.2\n Build 2024-04-13\n 当前教室: {0}\nCopyright (C) 2024 刘子涵 保留所有权利".format(
                addr),
            font=("SimHei", 12), bg="lightblue")
        self.copyright_label.place(
            x=master.winfo_screenwidth() - 400, y=master.winfo_screenheight() - 80)
        # 初始化解锁码为空字符串
        self.password = ""
        # 创建一个密码标签，显示请输入解锁码
        self.password_label = tk.Label(
            master, text="请输入解锁码: ", font=("SimHei", 24), bg="lightblue", fg="black")
        self.password_label.place(x=master.winfo_screenwidth()//5*3-100, y=200)

        # 创建一个键盘框架
        self.keypad_frame = tk.Frame(
            master, width=300, height=600, relief="ridge", bg="lightblue")
        self.keypad_frame.place(x=master.winfo_screenwidth(
        )//5*3-100, y=master.winfo_screenheight() // 3)
        # 创建键盘按钮
        self.create_keypad_buttons()
        # 设置窗口始终置顶
        set_always_on_top(master)

    def create_keypad_buttons(self):
        # 创建键盘按钮
        keypad_buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("0", 3, 1)
        ]

        # 遍历键盘按钮列表
        for (text, row, column) in keypad_buttons:
            # 创建一个按钮画布
            canvas = tk.Canvas(self.keypad_frame, width=100,
                               height=50, bg="lightblue", highlightthickness=0)
            # 显示按钮画布
            canvas.grid(row=row, column=column, padx=10, pady=30)
            # 创建按钮背景
            canvas.create_rectangle(
                0, 0, 100, 50, fill="lightblue", outline="black", width=2)
            # 创建按钮文本
            canvas.create_text(50, 25, text=text, font=("SimHei", 12))
            # 绑定按钮点击事件
            canvas.bind("<Button-1>", lambda event,
                        t=text: self.add_to_password(t))

        # 创建清空按钮画布
        clear_button_canvas = tk.Canvas(
            self.keypad_frame, width=100, height=50, bg="lightblue", highlightthickness=0)
        # 显示清空按钮画布
        clear_button_canvas.grid(row=3, column=2, padx=5, pady=5)
        # 创建清空按钮背景
        clear_button_canvas.create_rectangle(
            0, 0, 100, 50, fill="lightblue", outline="black", width=2)
        # 创建清空按钮文本
        clear_button_canvas.create_text(50, 25, text="清空", font=("SimHei", 12))
        # 绑定清空按钮点击事件
        clear_button_canvas.bind(
            "<Button-1>", lambda event: self.clear_password())

    def generate_qr_code(self):
        # 生成好的随机密码
        global random_password
        url = "[your_url]/verify.php?password={0}&machine_uuid={1}&addr={2}".format(random_password, machine_uuid, addr)
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # 生成二维码图片
        qr_image = qr.make_image(fill_color="black", back_color="lightblue")
        return qr_image

    def add_to_password(self, char):
        # 添加字符到密码中
        self.password += char
        self.password_label.config(
            text="请输入解锁码: " + "*" * len(self.password), bg="lightblue", fg="black")
        if len(self.password) == 6:
            self.check_password()

    def clear_password(self):
        # 清空密码
        self.password = ""
        self.password_label.config(text="请输入解锁码: ", bg="lightblue", fg="black")

    def check_password(self):
        # 检查解锁码
        global random_password
        global admin_password
        if self.password == random_password or self.password == admin_password:
            subprocess.Popen('C:\\Windows\\explorer.exe')  # 恢复explorer
            sys.exit()
        else:
            # 解锁码错误，清空密码
            self.password = ""
            self.password_label.config(
                text="解锁码错误!请重新输入!", bg="lightblue", fg="red")


def main():
    # 创建主函数，把关闭窗口事件绑定到空函数上
    root = tk.Tk()
    app = LockScreenApp(root)
    root.protocol("WM_DELETE_WINDOW", ignore_close_windows)
    root.mainloop()


if __name__ == "__main__":
    try:
        os.system("taskkill /f /im explorer.exe")  # 先杀死explorer，防止卡出开始菜单和任务栏
        if not check_process_exists("status.exe"):
            subprocess.Popen("C:/screenlock/status.exe")
    except:
        pass

    main()

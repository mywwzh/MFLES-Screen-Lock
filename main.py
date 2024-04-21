import tkinter as tk
from PIL import ImageTk
import qrcode
import ctypes
import requests as r
import uuid
import os
import subprocess
import psutil

headers = {
    'User-Agent': 'MFLES Screen Lock v1.2.0'
}
machine_uuid = str(uuid.UUID(int=uuid.getnode()))
try:
    f = open('C:/screenlock/config.ini', 'r', encoding='utf-8')
    addr = f.readline().strip()  # 读取配置的门牌号
    f.close()
except:
    addr = "获取失败"

api_source = "https://msl.mywwzh.top/get_source.php?addr={0}".format(addr)
try:
    response = r.get(api_source, verify=False, headers=headers).text
    if response == "mfles":
        source = "mfles"
    elif response == "mywwzh":
        source = "mywwzh"
except:
    source = "mfles"


def download_background_image():
    retries = 0
    while retries < 3:
        try:
            response = r.get(
                "https://msl.mywwzh.top/background.jpg", headers=headers)
            with open("C:/screenlock/background.jpg", "wb") as f:
                f.write(response.content)
                f.close()
            break
        except:
            retries += 1
            continue


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
    ctypes.windll.user32.SetWindowPos(
        root.winfo_id(), -1, 0, 0, 0, 0, 0x0001 | 0x0002)


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
        self.master.title("Windows Copilot")
        # 设置窗口大小
        self.master.geometry(
            "{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        # 设置窗口为全屏
        self.master.attributes('-fullscreen', True)
        # 设置背景图片
        self.background_image = ImageTk.PhotoImage(
            file="C:/screenlock/background.jpg")
        # 创建一个标签，用于显示背景图片
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 生成一个二维码图片
        self.qr_code_image = self.generate_qr_code()
        # 创建一个二维码标签，显示二维码图片
        self.qr_code = ImageTk.PhotoImage(
            self.qr_code_image.resize((300, 300)))
        self.qr_code_label = tk.Label(master, image=self.qr_code)
        self.qr_code_label.place(x=master.winfo_screenwidth(
        ) // 2 - 150, y=master.winfo_screenheight() // 2 - 250, width=300, height=300)

        set_always_on_top(master)

    def generate_qr_code(self):
        if source == "mfles":
            url = "https://oa.mfles.cn/api/v1/verify?muid={0}&duid={1}".format(
                machine_uuid, addr)
        elif source == "mywwzh":
            url = "https://msl.mywwzh.top/verifyv2.php?machine_uuid={0}&addr={1}".format(
                machine_uuid, addr)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=12,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # 生成二维码图片
        qr_image = qr.make_image(fill_color="black")
        return qr_image


def main():
    # 创建主函数，把关闭窗口事件绑定到空函数上
    root = tk.Tk()
    app = LockScreenApp(root)
    root.protocol("WM_DELETE_WINDOW", ignore_close_windows)
    root.mainloop()


if __name__ == "__main__":
    download_background_image()
    try:
        os.system("taskkill /f /im explorer.exe")  # 先杀死explorer，防止卡出开始菜单和任务栏
        if not check_process_exists("sync.exe"):
            subprocess.Popen("C:/screenlock/sync.exe")
    except:
        pass

    main()

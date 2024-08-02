import json
import os
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from tkcalendar import Calendar

from my.generateVideosByBeginAndEnd import generate_postcards_from_json
from my.upload_bilibili import upload_videos_to_bilibili
from my.upload_douyin import upload_videos_to_douyin
from my.upload_tencent import upload_videos_to_tencent
from pathUtils import get_dest_dir, get_base_dir
from my.get_douyin_cookie import setup_douyin_account
from my.get_bilibili_cookie import open_bilibili_folder
from my.get_tencent_cookie import setup_tencent_account

class TextEditorApp:
    def __init__(self, root, json_file, wav_file, background_file):
        self.root = root
        self.json_file = get_dest_dir() / json_file  # 使用获取本地磁盘文件路径
        self.wav_file = get_base_dir() / wav_file  # 使用 get_base_dir 获取虚拟文件路径
        self.background_file = get_base_dir() / background_file
        self.records = self.load_json()
        self.create_widgets()
        self.update_highlight_dates()
        self.set_default_date()
        self.load_texts_for_date()  # 默认点击查询

        # 使窗口居中
        self.center_window(800, 600)  # 设置窗口宽度为800，高度为600

    def load_json(self):
        """从文件加载 JSON 数据。"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("错误", "JSON 文件未找到。")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("错误", "解码 JSON 文件时出错。")
            return []

    def create_widgets(self):
        """创建并放置控件。"""
        self.root.title("推送内容预告")

        # 配置样式
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)
        style.configure('TText', font=('Arial', 12))

        # 日历控件
        self.calendar = Calendar(self.root, selectmode='day', year=datetime.now().year, month=datetime.now().month,
                                 day=datetime.now().day)
        self.calendar.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        # 绑定日历选择事件
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected_from_calendar)

        # 文本框，用于显示和编辑文本
        self.text_box = tk.Text(self.root, wrap='word', height=20, width=80, font=('Arial', 12), borderwidth=2,
                                relief='sunken')
        self.text_box.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')

        # 非必要步骤按钮
        self.save_button = ttk.Button(self.root, text="保存（非必要步骤）", command=self.save_texts)
        self.save_button.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

        self.generate_video_button = ttk.Button(self.root, text="生成选定日期视频（非必要步骤）",
                                                command=self.generate_video_for_selected_date)
        self.generate_video_button.grid(row=3, column=0, padx=20, pady=10, sticky='ew')
        # 上传cookies按钮
        self.cookies_tencent_button = ttk.Button(self.root, text="cookies  抖音", command=setup_douyin_account)

        self.cookies_tencent_button.grid(row=2, column=1, padx=20, pady=10, sticky='ew')

        self.cookies_bilibili_button = ttk.Button(self.root, text="cookies Bilibili",
                                                    command=open_bilibili_folder)
        self.cookies_bilibili_button.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

        self.cookies_tencent_button = ttk.Button(self.root, text="cookies Tencent",
                                                   command=setup_tencent_account)
        self.cookies_tencent_button.grid(row=4, column=1, padx=20, pady=10, sticky='ew')

        # 上传步骤按钮
        self.upload_button = ttk.Button(self.root, text="一键上传当日视频到抖音", command=self.upload_video_to_douyin)
        self.upload_button.grid(row=2, column=2, padx=20, pady=10, sticky='ew')

        self.upload_to_bilibili_button = ttk.Button(self.root, text="一键上传当日视频到 Bilibili",
                                                    command=self.upload_video_to_bilibili)
        self.upload_to_bilibili_button.grid(row=3, column=2, padx=20, pady=10, sticky='ew')

        self.upload_to_tencent_button = ttk.Button(self.root, text="一键上传当日视频到 Tencent",
                                                   command=self.upload_video_to_tencent)
        self.upload_to_tencent_button.grid(row=4, column=2, padx=20, pady=10, sticky='ew')

        # 打开文件夹按钮
        self.open_folder_button = ttk.Button(self.root, text="打开当日文件夹，调整你要上传的视频",
                                             command=self.open_folder_for_selected_date)
        self.open_folder_button.grid(row=4, column=0, padx=20, pady=10, sticky='ew')

        # 调整列权重以确保文本框和按钮占据足够空间
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def open_folder_for_selected_date(self):
        """打开选择的日期对应的文件夹。"""
        date_str = self.calendar.get_date()
        try:
            date = datetime.strptime(date_str, '%m/%d/%y')  # 将日期字符串转换为 datetime 对象
            date_str = date.strftime('%Y-%m-%d')  # 将 datetime 对象转换为所需格式
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return

        if not self.is_valid_date(date_str):
            messagebox.showwarning("警告", "请输入有效的日期，格式为 YYYY-MM-DD。")
            return

        # 构建文件夹路径
        folder_path = get_dest_dir() / "postcards" / date_str
        folder_path.mkdir(parents=True, exist_ok=True)

        # 打开文件夹
        if folder_path.exists():
            try:
                if sys.platform == 'win32':  # Windows
                    os.startfile(folder_path)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', folder_path])
                elif sys.platform == 'linux':  # Linux
                    subprocess.run(['xdg-open', folder_path])
                else:
                    messagebox.showwarning("警告", "无法识别的操作系统。")
            except Exception as e:
                messagebox.showerror("错误", f"打开文件夹时出错: {e}")
        else:
            messagebox.showwarning("警告", "文件夹不存在。")

    def set_default_date(self):
        """设置默认查询日期为今天。"""
        today = datetime.now().date()
        self.calendar.selection_set(today)

    def update_highlight_dates(self):
        """根据 JSON 数据中的日期更新高亮显示。"""
        content_dates = set(datetime.strptime(record['date'], '%Y-%m-%d').date() for record in self.records)
        # 将所有日期设置为默认样式
        self.calendar.calevent_remove('highlight', 'all')

        # 为有数据的日期高亮
        for date in content_dates:
            self.calendar.calevent_create(date, '有数据', 'highlight')

    def on_date_selected_from_calendar(self, event):
        """处理日历选择事件，自动加载所选日期的文本。"""
        date = self.calendar.get_date()
        self.load_texts_for_date(date)

    def load_texts_for_date(self, date=None):
        """加载指定日期的文本。"""
        if date is None:
            date = self.calendar.get_date()

        # 确保 date 是 datetime 对象
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%m/%d/%y')  # 假设日期格式为 MM/DD/YY
            except ValueError:
                messagebox.showwarning("警告", "无效的日期格式。")
                return
        elif isinstance(date, datetime):
            pass
        else:
            messagebox.showwarning("警告", "日期对象无效。")
            return

        date_str = date.strftime('%Y-%m-%d')

        if not self.is_valid_date(date_str):
            messagebox.showwarning("警告", "请输入有效的日期，格式为 YYYY-MM-DD。")
            return

        # 清空文本框
        self.text_box.delete(1.0, tk.END)

        # 根据指定日期过滤记录
        self.current_date_records = [record for record in self.records if record['date'] == date_str]

        if not self.current_date_records:
            messagebox.showinfo("信息", "没有找到该日期的记录。")
        else:
            for record in self.current_date_records:
                self.text_box.insert(tk.END, f"{record['text']}\n\n")

    def is_valid_date(self, date_str):
        """检查给定的日期字符串是否为 YYYY-MM-DD 格式。"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def save_texts(self):
        """将编辑后的文本保存回 JSON 文件。"""
        print("保存按钮被点击。")  # 调试输出
        # 获取选择的日期，并将其转换为 datetime 对象
        date_str = self.calendar.get_date()
        try:
            date = datetime.strptime(date_str, '%m/%d/%y')  # 将日期字符串转换为 datetime 对象
            date_str = date.strftime('%Y-%m-%d')  # 将 datetime 对象转换为所需格式
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return

        if not self.is_valid_date(date_str):
            messagebox.showwarning("警告", "请输入有效的日期，格式为 YYYY-MM-DD。")
            return

        # 获取编辑后的文本
        edited_text = self.text_box.get(1.0, tk.END).strip()
        print(f"编辑后的文本: '{edited_text}'")  # 调试输出

        # 按双换行符分割编辑文本
        entries = [entry.strip() for entry in edited_text.split('\n\n') if entry.strip()]

        # 检查每个日期是否有超过10条记录
        if len(entries) > 10:
            messagebox.showwarning("警告", "每一天最多只能有 10 条记录。请减少当前记录数量。")
            return

        updated_records = []

        # 创建带有日期和自增 ID 的新记录
        id_counter = max((record['id'] for record in self.records), default=0) + 1
        for entry in entries:
            updated_records.append({
                'id': id_counter,
                'date': date_str,
                'text': entry
            })
            id_counter += 1

        # 移除指定日期的旧记录
        self.records = [record for record in self.records if record['date'] != date_str]

        # 添加新的记录
        self.records.extend(updated_records)

        # 保存到 JSON 文件
        try:
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump(self.records, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("成功", "文本已成功保存。")
        except IOError as e:
            messagebox.showerror("错误", f"保存文件时出错: {e}")

    def generate_video_for_selected_date(self):
        """为选择的日期生成视频。"""
        date_str = self.calendar.get_date()
        try:
            date = datetime.strptime(date_str, '%m/%d/%y')  # 将日期字符串转换为 datetime 对象
            date_str = date.strftime('%Y-%m-%d')  # 将 datetime 对象转换为所需格式
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return

        # 获取选择的日期对应的记录
        selected_records = [record for record in self.records if record['date'] == date_str]
        if not selected_records:
            messagebox.showinfo("信息", "没有找到该日期的记录。")
            return

        # 生成视频
        try:
            # 生成到真实路径
            generate_postcards_from_json(self.json_file, self.wav_file, self.background_file)
            messagebox.showinfo("成功", "视频生成完成。")
        except Exception as e:
            messagebox.showerror("错误", f"生成视频时出错: {e}")

    def upload_video_to_douyin(self):
        """上传当日视频到抖音。"""
        date_str = self.calendar.get_date()
        try:
            date = datetime.strptime(date_str, '%m/%d/%y')  # 将日期字符串转换为 datetime 对象
            date_str = date.strftime('%Y-%m-%d')  # 将 datetime 对象转换为所需格式
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return

        # 获取选择的日期对应的记录
        selected_records = [record for record in self.records if record['date'] == date_str]
        if not selected_records:
            messagebox.showinfo("信息", "没有找到该日期的记录。")
            return

        # 上传视频
        try:
            upload_videos_to_douyin(date_str)
            messagebox.showinfo("成功", "视频已成功上传到抖音。")
        except Exception as e:
            messagebox.showerror("错误", f"上传视频到抖音时出错: {e}")

    def upload_video_to_tencent(self):
        """上传当日视频到腾讯。"""
        date_str = self.calendar.get_date()
        try:
            date = datetime.strptime(date_str, '%m/%d/%y')  # 将日期字符串转换为 datetime 对象
            date_str = date.strftime('%Y-%m-%d')  # 将 datetime 对象转换为所需格式
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return

        # 获取选择的日期对应的记录
        selected_records = [record for record in self.records if record['date'] == date_str]
        if not selected_records:
            messagebox.showinfo("信息", "没有找到该日期的记录。")
            return

        # 上传视频
        try:
            upload_videos_to_tencent(date_str)
            messagebox.showinfo("成功", "视频已成功上传到腾讯。")
        except Exception as e:
            messagebox.showerror("错误", f"上传视频到腾讯时出错: {e}")

    def upload_video_to_bilibili(self):
        """上传当日视频到 Bilibili。"""
        date_str = self.calendar.get_date()
        try:
            date = datetime.strptime(date_str, '%m/%d/%y')  # 将日期字符串转换为 datetime 对象
            date_str = date.strftime('%Y-%m-%d')  # 将 datetime 对象转换为所需格式
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return


        # 获取选择的日期对应的记录
        selected_records = [record for record in self.records if record['date'] == date_str]
        if not selected_records:
            messagebox.showinfo("信息", "没有找到该日期的记录。")
            return

        # 上传视频
        try:
            upload_videos_to_bilibili(date_str)
            messagebox.showinfo("成功", "视频已成功上传到 Bilibili。")
        except Exception as e:
            messagebox.showerror("错误", f"上传视频到 Bilibili 时出错: {e}")

    def center_window(self, width, height):
        """将窗口居中。"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root, json_file="source/texts.json", wav_file="staticSource/大地.wav",
                        background_file="staticSource/background.jpg")
    root.mainloop()

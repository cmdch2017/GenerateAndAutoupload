import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
from generateVideosByBeginAndEnd import generate_postcards_from_json
import os
from upload_douyin import upload_videos_to_douyin
from upload_bilibili import upload_videos_to_bilibili

class TextEditorApp:
    def __init__(self, root, json_file):
        self.root = root
        self.json_file = json_file
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
        self.text_box.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')

        # 保存按钮
        self.save_button = ttk.Button(self.root, text="保存", command=self.save_texts)
        self.save_button.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

        # 生成视频按钮
        self.generate_video_button = ttk.Button(self.root, text="生成选定日期视频",
                                                command=self.generate_video_for_selected_date)
        self.generate_video_button.grid(row=2, column=1, padx=20, pady=10, sticky='ew')

        # 上传视频按钮
        self.upload_button = ttk.Button(self.root, text="一键上传当日视频到抖音", command=self.upload_video_to_douyin)
        self.upload_button.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

        # 上传视频按钮到 Bilibili
        self.upload_to_bilibili_button = ttk.Button(self.root, text="一键上传当日视频到 Bilibili",
                                                    command=self.upload_video_to_bilibili)
        self.upload_to_bilibili_button.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

        # 调整列权重以确保文本框和按钮占据足够空间
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

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

        # 添加更新后的记录
        self.records.extend(updated_records)

        # 将更新后的记录保存回 JSON 文件
        try:
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump(self.records, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("信息", "更改已成功保存。")
        except IOError:
            messagebox.showerror("错误", "保存 JSON 文件时出错。")

    def generate_video_for_selected_date(self):
        """生成选择日期的视频。"""
        selected_date = self.calendar.get_date()
        try:
            selected_date = datetime.strptime(selected_date, '%m/%d/%y')
            selected_date_str = selected_date.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("警告", "无效的日期格式。")
            return

        json_file = self.json_file
        audio_file = '../staticSource/大地.wav'
        output_dir = '../postcards'
        max_items_per_day = 10
        duration = 5

        # 调用生成视频的函数
        generate_postcards_from_json(json_file, audio_file, output_dir, begin_date=selected_date_str,
                                     end_date=selected_date_str, max_items_per_day=max_items_per_day, duration=duration)
        messagebox.showinfo("信息", f"{selected_date_str} 的视频已生成。")

    def upload_video_to_douyin(self):
        """上传当天的视频到抖音。"""
        today_str = datetime.now().strftime('%Y-%m-%d')
        video_path = f'../postcards/{today_str}'  # 假设视频文件以日期命名
        if not os.path.exists(video_path):
            messagebox.showwarning("警告", f"未找到当天的视频文件: {video_path}")
            return

        # 调用上传到抖音的函数
        try:
            upload_videos_to_douyin(today_str)
            messagebox.showinfo("信息", "视频已成功上传到抖音。")
        except Exception as e:
            messagebox.showerror("错误", f"1上传视频到抖音时出错: {e}")

    def upload_video_to_bilibili(self):
        """上传当天的视频到 Bilibili。"""
        today_str = datetime.now().strftime('%Y-%m-%d')
        video_path = f'../postcards/{today_str}'  # 假设视频文件以日期命名
        if not os.path.exists(video_path):
            messagebox.showwarning("警告", f"未找到当天的视频文件: {video_path}")
            return

        # 调用上传到 Bilibili 的函数
        try:
            upload_videos_to_bilibili(today_str)
            messagebox.showinfo("信息", "视频已成功上传到 Bilibili。")
        except Exception as e:
            messagebox.showerror("错误", f"上传视频到 Bilibili 时出错: {e}")

    def center_window(self, width, height):
        """将窗口居中。"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.root.geometry(f'{width}x{height}+{x}+{y}')


# 创建主窗口
root = tk.Tk()
app = TextEditorApp(root, '../source/texts.json')
root.mainloop()

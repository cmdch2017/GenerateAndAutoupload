import os
import json
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def text_to_image(text, font_size=80, output_path='output.png', postcard_path="source/background.jpg", line_width=12,
                  line_spacing=10):
    postcard = Image.open(postcard_path)
    width, height = postcard.size

    font_path = "simhei.ttf"  # 替换为你的字体文件路径
    font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(postcard)
    wrapped_text = textwrap.fill(text, width=line_width)

    # 计算文本的总高度
    lines = wrapped_text.split('\n')
    max_line_width = max(
        [draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0] for line in lines])
    total_text_height = len(lines) * (font_size + line_spacing) - line_spacing

    # 计算文本的起始位置
    x = (width - max_line_width) // 2
    y = (height - total_text_height) // 2

    # 绘制文本
    for line in lines:
        draw.text((x, y), line, font=font, fill='orange')
        y += font_size + line_spacing

    postcard.save(output_path)


def combine_image_audio(image_path, audio_path, output_path='output.mp4', duration=5):
    if os.path.exists(output_path):
        os.remove(output_path)

    cmd = [
        'ffmpeg',
        '-y',
        '-loop', '1', '-i', image_path,
        '-i', audio_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-t', str(duration),
        output_path
    ]
    subprocess.run(cmd, check=True)


def generate_text_file(text, output_path, tags="#读书推荐 #读书成长 #读书摘抄"):
    """生成一个包含截取到第一个句号并添加标签的文本文件。"""
    first_sentence = text.split('。')[0] + '。🥺❤️‍🩹'
    full_text = f"{first_sentence}\n{tags}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)


def generate_postcards_from_json(json_file, audio_file, postcard_path="source/background.jpg", output_dir='postcards',
                                 begin_date=None, end_date=None, tags="#读书推荐 #读书成长 #读书摘抄",
                                 max_items_per_day=10, duration=5):
    os.makedirs(output_dir, exist_ok=True)

    with open(json_file, 'r', encoding='utf-8') as file:
        records = json.load(file)

    # 处理日期范围
    if not begin_date:
        begin_date = datetime.today().strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')

    begin_date = datetime.strptime(begin_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # 按日期分组记录
    grouped_records = {}
    for record in records:
        date = datetime.strptime(record['date'], '%Y-%m-%d').date()
        if not (begin_date <= date <= end_date):
            continue
        if date not in grouped_records:
            grouped_records[date] = []
        grouped_records[date].append(record)

    # 生成图像和视频
    for date, items in grouped_records.items():
        date_str = date.strftime('%Y-%m-%d')
        date_dir = os.path.join(output_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)

        # 按最大条目数分割记录
        for i in range(0, len(items), max_items_per_day):
            batch = items[i:i + max_items_per_day]
            for j, record in enumerate(batch):
                text = record['text']
                image_path = os.path.join(date_dir, f'{date_str}_{j}.png')
                video_path = os.path.join(date_dir, f'{date_str}_{j}.mp4')
                text_file_path = os.path.join(date_dir, f'{date_str}_{j}.txt')

                text_to_image(text, output_path=image_path, postcard_path=postcard_path, line_spacing=20)  # 修改行间距
                combine_image_audio(image_path, audio_file, output_path=video_path, duration=duration)
                generate_text_file(text, text_file_path, tags=tags)


if __name__ == '__main__':
    # 示例：生成2024年7月29日至2024年7月31日之间的明信片视频
    generate_postcards_from_json('source/texts.json', 'staticSource/大地.wav',
                                 postcard_path="staticSource/background.jpg",
                                 output_dir='../postcards', max_items_per_day=10, tags="#读书推荐 #读书成长 #读书摘抄",
                                 duration=10)

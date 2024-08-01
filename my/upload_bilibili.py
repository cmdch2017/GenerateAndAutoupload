import sys
import time
from pathlib import Path

from bilibili_uploader.main import read_cookie_json_file, extract_keys_from_json, random_emoji, BilibiliUploader
from utils.constant import VideoZoneTypes
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags
from pathUtils import get_dest_dir, get_base_dir



def upload_videos_to_bilibili(date_str, videos_per_day=10, daily_times=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]):
    dest_dir=get_dest_dir()
    # 配置路径
    filepath = dest_dir / "postcards" / date_str
    account_file = dest_dir / "bilibili_uploader" / "account.json"

    # 检查配置文件是否存在
    if not account_file.exists():
        print(f"{account_file.name} 配置文件不存在")
        return

    # 读取 cookie 数据
    cookie_data = read_cookie_json_file(account_file)
    cookie_data = extract_keys_from_json(cookie_data)

    tid = VideoZoneTypes.SPORTS_FOOTBALL.value  # 设置分区 id
    folder_path = Path(filepath)
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    if file_num < videos_per_day:
        videos_per_day = file_num

    # 生成调度时间
    timestamps = generate_schedule_time_next_day(file_num, videos_per_day, daily_times=daily_times, timestamps=True)

    # 遍历文件并上传
    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        title += random_emoji()  # 避免标题重复
        tags_str = ','.join(tags)  # 将标签列表转换为逗号分隔的字符串

        # 打印视频信息
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")

        desc = title  # 设置描述为标题

        # 上传视频
        bili_uploader = BilibiliUploader(cookie_data, file, title, desc, tid, tags, timestamps[index])
        bili_uploader.upload()

        # 暂停以避免过快上传
        time.sleep(30)


if __name__ == '__main__':
    upload_videos_to_bilibili("2024-07-29")

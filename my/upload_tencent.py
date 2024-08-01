import asyncio
from pathlib import Path
from conf import BASE_DIR
from tencent_uploader.main import weixin_setup, TencentVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags
import sys
from pathUtils import get_dest_dir, get_base_dir


def upload_videos_to_tencent(date_str, category=TencentZoneTypes.KNOWLEDGE.value, videos_per_day=10,
                             daily_times=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]):
    dest_dir=get_dest_dir()
    filepath = dest_dir / "postcards" / date_str
    account_file = dest_dir / "tencent_uploader" / "account.json"
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    if file_num < videos_per_day:
        videos_per_day = file_num
    # 生成定时发布的日期和时间
    publish_datetimes = generate_schedule_time_next_day(file_num, videos_per_day, daily_times=daily_times)

    # 设置微信 cookie
    cookie_setup = asyncio.run(weixin_setup(account_file, handle=True))

    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))

        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")

        # 初始化腾讯视频上传类
        app = TencentVideo(title, file, tags, publish_datetimes[index], account_file, category)

        # 执行上传
        asyncio.run(app.main(), debug=False)


if __name__ == '__main__':
    category = TencentZoneTypes.KNOWLEDGE.value  # 标记原创需要否则不需要传

    upload_videos_to_tencent("2024-07-29", category=category)

import asyncio

from douyin_uploader.main import douyin_setup, DouYinVideo
from pathUtils import get_dest_dir
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags


def upload_videos_to_douyin(date_str, videos_per_day=10, daily_times=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]):
    """
    上传指定日期的视频到抖音。

    :param date_str: 指定日期，格式为 'YYYY-MM-DD'
    :param daily_times: 每日上传时间列表，默认为 [10]
    """
    try:
        dest_dir = get_dest_dir()
        # 设置文件路径
        filepath = dest_dir / "postcards" / date_str
        account_file = dest_dir / "douyin_uploader" / "account.json"
        folder_path = filepath

        # 获取文件夹中的所有 .mp4 文件
        files = list(folder_path.glob("*.mp4"))
        print(f"打印文件路径：{folder_path}")
        if not files:
            print(f"未找到指定日期 {date_str} 的视频文件。")
            return

        file_num = len(files)

        if file_num < videos_per_day:
            videos_per_day = file_num
        publish_datetimes = generate_schedule_time_next_day(file_num, videos_per_day, daily_times=daily_times)

        cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))

        for index, file in enumerate(files):
            title, tags = get_title_and_hashtags(str(file))
            print(f"视频文件名：{file}")
            print(f"标题：{title}")
            print(f"Hashtag：{tags}")
            app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file)
            asyncio.run(app.main(), debug=False)
        print(f"所有视频已成功上传到抖音。")
    except Exception as e:
        print(f"上传视频到抖音时出错: {e}")


# 示例调用
if __name__ == '__main__':
    upload_videos_to_douyin("2024-07-29")

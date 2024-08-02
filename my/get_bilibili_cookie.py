import subprocess
import os

def open_folder(folder_path):
    try:
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return

        # 使用 subprocess.run 打开文件夹
        result = subprocess.run(['explorer', folder_path], check=True)

        if result.returncode == 0:
            print("Folder opened successfully.")
        else:
            print(f"Command returned non-zero exit status {result.returncode}.")
    except FileNotFoundError:
        print("File explorer not found. Please check your system.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    folder_path = r'D:\Demos\social-auto-upload-main\bilibili_uploader'
    open_folder(folder_path)

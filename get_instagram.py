import os
from datetime import datetime
from itertools import filterfalse
import instaloader
import time
import random
import json

# 設定IG帳號和密碼
USERNAME = 'account'
PASSWORD = 'password'

# 建立 Instaloader 物件，並模擬 Chrome 瀏覽器
L = instaloader.Instaloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)

# Instagram 帳號與暱稱的列表（可多筆）
instagram_accounts = [
    {"IAccount": "sayaka_oonuki", "INickName": "大貫彩香"},
    #{"IAccount": "evaaasong", "INickName": "然然Eva🐷"},
    #{"IAccount": "kimi.0917", "INickName": "瞳 𝐾𝑖𝑚𝑖"},
    #{"IAccount": "changyachuu", "INickName": "Changyachu🦄 妮娜張張"},
    #{"IAccount": "changyachuu", "INickName": "Changyachu🦄 妮娜張張"},
    #{"IAccount": "changyachuu", "INickName": "Changyachu🦄 妮娜張張"},
    #{"IAccount": "changyachuu", "INickName": "Changyachu🦄 妮娜張張"}
]

# 設定要儲存 Instagram 下載的根目錄
Instagram_Save_Root = r"D:\Instagram_images"

# 檢查 Instagram_Save_Root 資料夾是否存在，不存在則建立
if not os.path.exists(Instagram_Save_Root):
    os.makedirs(Instagram_Save_Root)
    print(f"已建立資料夾: {Instagram_Save_Root}")

# 將 session_file 存放在 Instagram_Save_Root 中
session_file = os.path.join(Instagram_Save_Root, USERNAME + "_session")

# 嘗試載入 session 以避免每次重新登入
try:
    L.load_session_from_file(USERNAME, session_file)
    print(f"已載入 session 檔案: {session_file}")
except FileNotFoundError:
    print("未找到 session 檔案，進行登入...")
    L.login(USERNAME, PASSWORD)  # 登入 Instagram
    L.save_session_to_file(session_file)  # 儲存 session 到指定路徑

# 設定篩選貼文的日期範圍
FROM = datetime(2022, 1, 1)  # 從這一天起（包含這天）
TILL = datetime(2024, 12, 31)  # 到這一天為止（不包含這天）

# 逐一處理每個 Instagram 帳號
for account in instagram_accounts:
    IAccount = account["IAccount"]
    INickName = account["INickName"]

    # 切換到儲存圖片的資料夾路徑
    os.chdir(Instagram_Save_Root)

    # 設定要下載的 Instagram 帳號名稱
    posts = instaloader.Profile.from_username(L.context, IAccount).get_posts()

    # 記錄起始時間
    start_time = time.time()

    # 用於儲存貼文資訊的 JSON 檔案列表
    json_list = []

    # 紀錄抓取的總圖片數量
    total_images = 0

    # 下載範圍內的貼文並儲存到指定的資料夾
    for post in filterfalse(lambda p: not (FROM <= p.date < TILL), posts):
        print(post.date)  # 列出貼文日期

        # 儲存每篇貼文的基本資訊至 JSON 結構
        post_info = {
            'date': post.date.strftime("%Y-%m-%d %H:%M:%S"),
            'shortcode': post.shortcode,
            'url': post.url,
            'likes': post.likes,
            'comments': post.comments,
        }

        json_list.append(post_info)

        # 將圖片下載到指定的資料夾
        L.download_post(post, IAccount + "(" + INickName + ")")
        total_images += 1  # 每次下載圖片後，更新總圖片數量

        # 在存取每張照片後等待 0 到 1 秒
        wait_time_photo = random.uniform(1, 4)
        print(f"存取完成，等待 {wait_time_photo:.2f} 秒...")
        time.sleep(wait_time_photo)

        # 每抓取完一篇貼文 (一個 JSON)，等待 3 到 5 秒
        wait_time_json = random.uniform(5, 8)
        print(f"抓取 JSON 完成，等待 {wait_time_json:.2f} 秒...")
        time.sleep(wait_time_json)

    # 記錄結束時間
    end_time = time.time()

    # 計算執行時間
    execution_time = end_time - start_time

    # 將所有貼文資訊存入 JSON 檔案
    json_filename = IAccount + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_list, json_file, ensure_ascii=False, indent=4)

    # 印出總抓取圖片數量和執行時間
    print(f"所有貼文資訊已存入 {json_filename}")
    print(f"總共抓取了 {total_images} 張圖片")
    print(f"總執行時間: {execution_time:.2f} 秒")

    # 每個帳號抓取完成後，等待 120 到 240 秒
    wait_time_account = random.uniform(120, 240)
    print(f"{IAccount} 帳號抓取完成，等待 {wait_time_account:.2f} 秒後繼續下一個帳號...")
    time.sleep(wait_time_account)

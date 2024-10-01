import os
import requests
from bs4 import BeautifulSoup
import re
import urllib.request

# 0. 從 terminal 交互中輸入網頁
url = input("請輸入要抓取的網頁網址: ")

# 設定 headers 和 cookies 來模擬瀏覽器訪問
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 設定 cookie，模擬 "已滿18歲"
cookies = {
    'age_verified': 'yes'  # 假設 'age_verified' 是網站用來判定是否已滿18歲的cookie名稱
}

# 發送請求抓取網頁內容，帶上 cookies
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.content, 'html.parser')

# 取得 <title> 中的文字
title_tag = soup.find('title')
if title_tag:
    title_text = title_tag.get_text().strip()
    # 過濾不合法的文件名字符
    title_text = re.sub(r'[\\/*?:"<>|]', '', title_text)  # 移除非法字符
    
    # 過濾掉從 "FC2-PPV" 開始的部分
    title_text = re.split(r'FC2-PPV', title_text)[0].strip()
else:
    title_text = "NoTitle"

# 3. 從 /article 後抓取數字，並以 "FC2-PPV-" + <title> 作為目錄名稱
match = re.search(r'/article/(\d+)', url)
if match:
    article_id = match.group(1)
    directory_name = f"FC2-PPV-{article_id} {title_text}"
    os.makedirs(directory_name, exist_ok=True)  # 建立目錄

# 4. 抓取 <div class="items_article_MainitemThumb"><span> 和 <p class="items_article_info"> 之間的圖片
thumb_div = soup.find('div', class_='items_article_MainitemThumb')
if thumb_div:
    img_tag = thumb_div.find('img')
    if img_tag and 'src' in img_tag.attrs:
        img_url = img_tag['src']
        
        # 如果 URL 是以 // 開頭，補上 https:
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        
        # 打印圖片 URL 以便檢查
        print(f"下載封面圖片 URL: {img_url}")

        try:
            # 取得絕對的圖片文件名路徑
            img_filename = os.path.join(os.getcwd(), directory_name, os.path.basename(img_url))
            
            # 下載圖片
            urllib.request.urlretrieve(img_url, img_filename)
            print(f"已下載封面圖片: {img_filename}")
        except Exception as e:
            print(f"下載封面圖片失敗: {e}")

# 5. 抓取 <h3>預覽圖片</h3><ul class="items_article_SampleImagesArea"> 和 </section><section> 中間的圖片
sample_images_area = soup.find('ul', class_='items_article_SampleImagesArea')
if sample_images_area:
    img_tags = sample_images_area.find_all('img')
    for img_tag in img_tags:
        if 'src' in img_tag.attrs:
            img_url = img_tag['src']
            
            # 如果 URL 是以 // 開頭，補上 https:
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            
            # 打印圖片 URL 以便檢查
            print(f"下載預覽圖片 URL: {img_url}")

            try:
                # 取得絕對的圖片文件名路徑
                img_filename = os.path.join(os.getcwd(), directory_name, os.path.basename(img_url))
                
                # 下載預覽圖片
                urllib.request.urlretrieve(img_url, img_filename)
                print(f"已下載預覽圖片: {img_filename}")
            except Exception as e:
                print(f"下載預覽圖片失敗: {e}")

print("所有圖片抓取完成。")

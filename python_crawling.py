import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# 设置关键词
keyword = "光交箱"
save_dir = "images"  # 存储图片的文件夹
os.makedirs(save_dir, exist_ok=True)  # exist_ok:只有在目录不存在时创建目录，目录已存在时不会抛出异常。

# 从外网加载webdriver
# ChromeDriverManager().install()
# # 启动 Chrome
# service = Service(ChromeDriverManager().install())
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 无头模式（不打开浏览器窗口）
# options.add_argument("--disable-gpu")
# driver = webdriver.Chrome(service=service, options=options) # driver 是 WebDriver（浏览器驱动），用于 自动控制浏览器，模拟人类浏览网页的操作

# 使用离线 webdriver
chrome_driver_path = "C:/chromeDirver/chromedriver-win64/chromedriver.exe"
service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无头模式（不打开浏览器窗口）
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=options)



# 百度图片 URL
search_url = f"https://image.baidu.com/search/index?tn=baiduimage&word={keyword}"
driver.get(search_url) # 是阻塞方法（同步方法），它会一直等待，直到页面加载完成**（即浏览器的 onload 事件触发） 但是，Selenium 默认只等待 HTML 结构加载完成，并不会等待所有图片、JS、Ajax 请求等异步资源加载完毕
time.sleep(5)  # 等待页面加载 即等待页面图片的异步加载 同时也能避免：频繁、快速请求可能触发百度的反爬机制，导致 IP 被封或返回空页面

# 获取当前照片数量
old_img_count = len(driver.find_elements(By.CSS_SELECTOR, "img.main_img"))

# 滚动页面加载更多图片
for _ in range(10):  # 滚动 1 次
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END) # 滚动到底部
    time.sleep(2)  # 等待 2 秒，让新图片加载
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "img.main_img")) > old_img_count # 直到新图片数量大于旧图片数量
    )
    old_img_count = len(driver.find_elements(By.CSS_SELECTOR, "img.main_img"))

# 获取所有图片元素
img_elements = driver.find_elements(By.CSS_SELECTOR, "img.main_img")
print(f"找到 {len(img_elements)} 张图片")

# 下载图片
for idx, img in enumerate(img_elements):
    img_url = img.get_attribute("src")  # 获取图片 URL
    if img_url and img_url.startswith("http"):
        try:
            response = requests.get(img_url, timeout=10)
            with open(os.path.join(save_dir, f"光交箱_{idx+1}.jpg"), "wb") as file:
                file.write(response.content)
            print(f"✅ 下载成功: {img_url}")
        except Exception as e:
            print(f"❌ 下载失败: {img_url}，错误: {e}")

# 关闭浏览器
driver.quit()
print("✅ 爬取完成！")

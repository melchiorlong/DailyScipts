from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 配置 ChromeOptions
chrome_options = Options()
chrome_options.headless = True  # 启用无头模式
chrome_options.add_argument('--headless')  # 启用无头模式
chrome_options.add_argument('--disable-gpu')  # 禁用 GPU
chrome_options.add_argument('--no-sandbox')  # 在 Linux 系统上使用
chrome_options.add_argument('--window-size=1920x1080')  # 设置窗口大小

# 指定 ChromeDriver 的路径
service = Service('/usr/local/bin/chromedriver/chromedriver')

# 创建 WebDriver 实例
driver = webdriver.Chrome(service=service, options=chrome_options)

# 访问网页
driver.get('https://www.google.com')
print(driver.title)

# 关闭浏览器
driver.quit()

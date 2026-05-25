import urllib.request
import re

req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有文章链接
links = re.findall(r'href="(https://supplychain-tips\.pages\.dev/posts/[^"]+)"', html)
print(f'首页文章链接数: {len(links)}')

# 提取日期
dates = []
for link in links:
    match = re.search(r'/(\d{4}-\d{2}-\d{2})-', link)
    if match:
        dates.append(match.group(1))

if dates:
    print(f'最新文章日期: {max(dates)}')
else:
    print('未找到日期')
    for link in links[:10]:
        print(f'  {link}')

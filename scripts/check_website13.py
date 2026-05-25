import urllib.request
import re

# 检查网站首页
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 提取文章slug
urls = re.findall(r'https://supplychain-tips\.pages\.dev/posts/([^"\'\s/>]+)', html)
print(f'文章数: {len(urls)}')
for url in urls:
    print(f'  {url}')

# 检查是否有5月25日的文章（通过slug判断）
may25 = [u for u in urls if '2026-05-25' in u]
print(f'\n5月25日文章数: {len(may25)}')

# 检查其他日期
all_dates = set()
for u in urls:
    m = re.search(r'(\d{4}-\d{2}-\d{2})', u)
    if m:
        all_dates.add(m.group(1))
print(f'所有日期: {sorted(all_dates)}')

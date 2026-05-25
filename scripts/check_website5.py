import urllib.request
import re

req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有文章链接
links = re.findall(r'href=["\']([^"\']*)["\']', html)
post_links = [l for l in links if 'posts/' in l]
print(f'文章链接数: {len(post_links)}')

# 提取日期
dates = []
for link in post_links:
    match = re.search(r'(\d{4}-\d{2}-\d{2})', link)
    if match:
        dates.append(match.group(1))

if dates:
    print(f'最新文章日期: {max(dates)}')
    # 统计各日期文章数
    from collections import Counter
    date_counts = Counter(dates)
    for date, count in sorted(date_counts.items())[-5:]:
        print(f'  {date}: {count}篇')
else:
    print('未找到日期')
    for link in post_links[:10]:
        print(f'  {link}')

import urllib.request
import re

req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有包含2026-05的链接
links = re.findall(r'href=["\']([^"\']*2026-05[^"\']*)["\']', html)
print(f'5月文章链接数: {len(links)}')
for link in links[:10]:
    print(f'  {link}')

# 查找所有文章卡片
cards = re.findall(r'<article[^>]*>.*?</article>', html, re.DOTALL)
print(f'文章卡片数: {len(cards)}')

# 从卡片中提取日期
for card in cards[:5]:
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', card)
    if date_match:
        print(f'  日期: {date_match.group(1)}')

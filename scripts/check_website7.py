import urllib.request
import re

req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有文章链接
links = re.findall(r'href=([^>\s]+)', html)
post_links = [l.strip('"').strip("'") for l in links if 'posts/' in l]
print(f'文章链接数: {len(post_links)}')

# 检查5月25日的文章
may25_links = [l for l in post_links if '2026-05-25' in l]
print(f'5月25日文章数: {len(may25_links)}')

# 显示所有链接
for link in post_links:
    print(f'  {link}')

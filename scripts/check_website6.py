import urllib.request
import re

req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有href
links = re.findall(r'href=([^>\s]+)', html)
print(f'总链接数: {len(links)}')
# 显示前20个
for link in links[:20]:
    print(f'  {link}')

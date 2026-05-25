import urllib.request
import re

# 检查网站首页
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有文本内容
texts = re.findall(r'>([^<]{10,})<', html)
print(f'文本片段数: {len(texts)}')
for t in texts[:20]:
    clean = t.strip()
    if clean:
        print(f'  {clean[:80]}')

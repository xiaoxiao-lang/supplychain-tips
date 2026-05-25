import urllib.request
import re

# 检查网站首页
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有文章标题（在h3或h2中）
articles = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html, re.DOTALL)
print(f'文章标题数: {len(articles)}')
for a in articles[:15]:
    clean = re.sub(r'<[^>]+>', '', a).strip()
    if clean and len(clean) > 5:
        print(f'  {clean[:60]}')

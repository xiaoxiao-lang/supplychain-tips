import urllib.request
import re

# 检查网站首页
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找文章标题和链接
titles = re.findall(r'<h2[^>]*>(.*?)</h2>', html)
print(f'首页h2标题数: {len(titles)}')
for t in titles[:10]:
    print(f'  {t.strip()}')

# 查找文章卡片
articles = re.findall(r'<a[^>]*href="([^"]*posts/[^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
print(f'文章链接数: {len(articles)}')
for url, title in articles[:10]:
    print(f'  {url} - {title.strip()}')

import urllib.request
import re

# 检查网站首页
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找所有包含posts/的URL
urls = re.findall(r'https://supplychain-tips\.pages\.dev/posts/[^"\'\s]+', html)
print(f'文章URL数: {len(urls)}')
for url in urls:
    print(f'  {url}')

# 查找文章标题（前面有链接的）
print('\n文章标题:')
titles = re.findall(r'<a[^>]*href="[^"]*posts/[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
for t in titles:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    if clean and len(clean) > 5:
        print(f'  {clean[:60]}')

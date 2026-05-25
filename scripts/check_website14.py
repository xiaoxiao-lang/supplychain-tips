import urllib.request
import re

# 检查网站首页 - 可能是缓存问题，强制刷新
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={
        'User-Agent': 'Mozilla/5.0',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找文章标题
articles = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
print(f'h3标题数: {len(articles)}')
for a in articles[:15]:
    clean = re.sub(r'<[^>]+>', '', a).strip()
    if clean and len(clean) > 5:
        print(f'  {clean[:60]}')

# 查找所有链接中的posts
links = re.findall(r'href=["\']([^"\']*posts/[^"\']*)["\']', html)
print(f'\n文章链接数: {len(links)}')
for l in links:
    print(f'  {l}')

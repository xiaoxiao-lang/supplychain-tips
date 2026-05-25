import urllib.request
import re

# 检查网站首页
req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 查找文章卡片（包含文章标题和链接）
# Hugo默认只显示最近10篇文章
sections = re.findall(r'<section[^>]*>(.*?)</section>', html, re.DOTALL)
print(f' section数: {len(sections)}')

# 查找文章链接和标题
links = re.findall(r'<a[^>]*href="([^"]*posts/[^"]*)"[^>]*>\s*<h[23][^>]*>(.*?)</h[23]>', html, re.DOTALL)
print(f'文章链接+标题数: {len(links)}')
for url, title in links:
    clean_title = re.sub(r'<[^>]+>', '', title).strip()
    print(f'  {url}')
    print(f'    -> {clean_title[:50]}')

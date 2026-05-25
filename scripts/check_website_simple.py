import urllib.request
import re

# 检查线上网站
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

# 查找文章标题和日期
items = re.findall(r'<div class=list-item>(.*?)</div>\s*</div>', html, re.DOTALL)
print(f'线上文章项数: {len(items)}')
for item in items:
    link_match = re.search(r'href="([^"]+)"', item)
    link = link_match.group(1) if link_match else 'no link'

    title_match = re.search(r'<h3[^>]*>(.*?)</h3>', item, re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    else:
        title = 'no title'

    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', item)
    if date_match:
        date = date_match.group(1)
    else:
        date_match = re.search(r'(\d+)月(\d+)日', item)
        if date_match:
            date = f'2026-{date_match.group(1).zfill(2)}-{date_match.group(2).zfill(2)}'
        else:
            date = 'unknown'

    print(f'  {date} - {title[:40]}')

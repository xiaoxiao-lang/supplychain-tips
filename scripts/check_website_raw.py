import urllib.request
import re

# 检查线上网站原始HTML
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

# 保存到文件以便分析
with open(r'D:\myseosite\scripts\website_raw.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'HTML长度: {len(html)}')
print('HTML前500字符:')
print(html[:500])
print('\n...')
print('HTML最后500字符:')
print(html[-500:])

import urllib.request
import re

req = urllib.request.Request(
    'https://supplychain-tips.pages.dev/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode('utf-8', errors='ignore')

# 保存部分HTML用于分析
print('HTML前2000字符:')
print(html[:2000])
print('\n...')
print('HTML最后1000字符:')
print(html[-1000:])

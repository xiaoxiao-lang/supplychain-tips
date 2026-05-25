import os
import re

# 检查本地构建的index.html
index_file = r'D:\myseosite\public\index.html'
with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 查找文章链接
links = re.findall(r'href=["\']([^"\']*posts/[^"\']*)["\']', html)
print(f'本地index文章链接数: {len(links)}')

# 检查5月25日
may25 = [l for l in links if '2026-05-25' in l]
print(f'5月25日文章数: {len(may25)}')

# 显示所有链接
for l in links[:15]:
    print(f'  {l}')

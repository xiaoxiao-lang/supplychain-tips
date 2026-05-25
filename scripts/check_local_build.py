import os
import re

# 检查本地构建输出
public_dir = r'D:\myseosite\public'
index_file = os.path.join(public_dir, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 查找文章链接
links = re.findall(r'href=["\']([^"\']*posts/[^"\']*)["\']', html)
print(f'本地构建文章链接数: {len(links)}')
for l in links[:15]:
    print(f'  {l}')

# 检查5月25日文章
may25 = [l for l in links if '2026-05-25' in l]
print(f'\n5月25日文章数: {len(may25)}')

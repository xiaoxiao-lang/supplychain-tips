import os
import re

# 检查Hugo构建的public/index.html
index_file = r'D:\myseosite\public\index.html'
with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 查找所有文章链接
links = re.findall(r'href=["\']([^"\']*posts/[^"\']*)["\']', html)
print(f'文章链接数: {len(links)}')
for l in links:
    print(f'  {l}')

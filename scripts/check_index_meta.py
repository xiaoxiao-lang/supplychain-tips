import os
import re

# 检查Hugo构建的public/index.html中的文章卡片
index_file = r'D:\myseosite\public\index.html'
with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 查找所有文章链接
links = re.findall(r'href=["\']([^"\']*posts/[^"\']*)["\']', html)
print(f'文章链接数: {len(links)}')

# 查找文章meta中的日期
metas = re.findall(r'<div class="post-meta">(.*?)</div>', html, re.DOTALL)
print(f'文章meta数: {len(metas)}')
for m in metas[:10]:
    clean = re.sub(r'<[^>]+>', ' ', m).strip()
    print(f'  {clean}')

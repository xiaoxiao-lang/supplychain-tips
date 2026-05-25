import os
import re

# 检查Hugo构建的public/index.html
index_file = r'D:\myseosite\public\index.html'
with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 查找文章列表区域
list_group = re.findall(r'<div class="list-group">(.*?)</div>\s*</main>', html, re.DOTALL)
if list_group:
    content = list_group[0]
    # 查找所有文章项
    items = re.findall(r'<div class="list-item">(.*?)</div>\s*</div>', content, re.DOTALL)
    print(f'文章项数: {len(items)}')
    for item in items:
        # 提取链接
        link_match = re.search(r'href="([^"]+)"', item)
        link = link_match.group(1) if link_match else 'no link'
        
        # 提取标题
        title_match = re.search(r'<h3[^>]*>(.*?)</h3>', item, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        else:
            title = 'no title'
        
        # 提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', item)
        if date_match:
            date = date_match.group(1)
        else:
            date_match = re.search(r'(\d+)月(\d+)日', item)
            if date_match:
                date = f'2026-{date_match.group(1).zfill(2)}-{date_match.group(2).zfill(2)}'
            else:
                date = 'unknown'
        
        print(f'  {date} - {title[:40]} - {link}')
else:
    print('未找到list-group')

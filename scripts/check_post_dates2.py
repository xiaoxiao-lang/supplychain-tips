import os
import re

# 检查public/posts下的文章目录
public_posts_dir = r'D:\myseosite\public\posts'
dirs = [d for d in os.listdir(public_posts_dir) if os.path.isdir(os.path.join(public_posts_dir, d))]

print(f'构建输出文章数: {len(dirs)}')

# 读取每个文章的index.html，查找日期（更宽松的模式）
articles = []
for d in dirs:
    index_file = os.path.join(public_posts_dir, d, 'index.html')
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 查找日期 - 多种格式
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            date = date_match.group(1)
        else:
            # 查找中文日期
            date_match = re.search(r'(\d+)月(\d+)日', content)
            if date_match:
                date = f'2026-{date_match.group(1).zfill(2)}-{date_match.group(2).zfill(2)}'
            else:
                date = 'unknown'
        
        articles.append((date, d))

# 按日期排序
articles_sorted = sorted(articles, key=lambda x: x[0], reverse=True)
print('最新15篇文章:')
for date, slug in articles_sorted[:15]:
    print(f'  {date} - {slug}')

# 统计5月25日的文章
may25 = [a for a in articles if a[0].startswith('2026-05-25')]
print(f'\n5月25日文章数: {len(may25)}')

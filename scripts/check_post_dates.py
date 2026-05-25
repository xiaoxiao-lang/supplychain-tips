import os
import re

# 检查public/posts下的文章目录
public_posts_dir = r'D:\myseosite\public\posts'
dirs = [d for d in os.listdir(public_posts_dir) if os.path.isdir(os.path.join(public_posts_dir, d))]

print(f'构建输出文章数: {len(dirs)}')

# 读取每个文章的index.html，查找日期
articles = []
for d in dirs:
    index_file = os.path.join(public_posts_dir, d, 'index.html')
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 查找日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            date = date_match.group(1)
        else:
            date = 'unknown'
        
        articles.append((date, d))

# 按日期排序
articles_sorted = sorted(articles, key=lambda x: x[0], reverse=True)
print('最新15篇文章:')
for date, slug in articles_sorted[:15]:
    print(f'  {date} - {slug}')

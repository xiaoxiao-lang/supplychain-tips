import os
import re

# 检查content/posts目录下的文章frontmatter
posts_dir = r'D:\myseosite\content\posts'
files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]

articles = []
for f in files:
    filepath = os.path.join(posts_dir, f)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # 提取date
    date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        date = date_match.group(1)
    else:
        date = 'unknown'

    # 提取title
    title_match = re.search(r'title:\s*"([^"]*)"', content)
    if title_match:
        title = title_match.group(1)
    else:
        title = f

    articles.append((date, title, f))

# 按日期排序
articles_sorted = sorted(articles, key=lambda x: x[0], reverse=True)
print('最新15篇文章（按date排序）:')
for date, title, filename in articles_sorted[:15]:
    print(f"  {date} - {filename}")

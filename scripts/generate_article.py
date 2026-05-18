#!/usr/bin/env python3
"""
SEO文章自动生成脚本
每天跑一次，生成一篇新的SEO优化文章
"""

import os, json, datetime, hashlib, re
from pathlib import Path

# 配置
SITE_DIR = r"D:\myseosite"
API_KEY = "sk-ffc7d8a98a3742f5a92b7f792c9c26b4"  # DeepSeek API
API_URL = "https://api.deepseek.com/v1/chat/completions"

# SEO关键词库 - 供应链行业
KEYWORDS = [
    "供应链管理", "采购流程优化", "库存管理技巧", "物流成本控制",
    "ERP系统实施", "供应商评估", "供应链金融", "仓储效率提升",
    "JIT准时制", "VMI供应商管理库存", "SKU管理", "供应链风险",
    "采购谈判技巧", "仓库KPI", "运输管理", "供应链数字化转型",
    "MRP物料需求计划", "供应链协同", "库存周转率", "采购成本分析",
]

def call_deepseek(prompt):
    """调用DeepSeek API生成内容"""
    import urllib.request
    
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
        "max_tokens": 3000,
    }).encode('utf-8')
    
    req = urllib.request.Request(
        API_URL, 
        data=payload,
        headers={
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {API_KEY}"
        }
    )
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    return result["choices"][0]["message"]["content"]

def parse_article(ai_output):
    """解析AI输出，提取标题、slug、tags和正文"""
    lines = ai_output.strip().split('\n')
    
    title = ""
    slug = ""
    tags = []
    description = ""
    content_lines = []
    in_content = False
    
    for line in lines:
        line = line.strip()
        if line.startswith("标题:"):
            title = line[3:].strip()
        elif line.startswith("slug:"):
            slug = line[5:].strip().lower().replace(' ', '-')
        elif line.startswith("标签:") or line.startswith("tags:"):
            tags_str = line[3:].strip() if line.startswith("标签:") else line[5:].strip()
            tags = [t.strip() for t in tags_str.replace('[', '').replace(']', '').split(',')]
        elif line.startswith("描述:") or line.startswith("description:"):
            description = line[3:].strip() if line.startswith("描述:") else line[12:].strip()
        elif line.startswith("正文:") or line.startswith("内容:") or line.startswith("# "):
            in_content = True
            if '# ' in line:
                content_lines.append(line)
        elif in_content or (line and not ':' in line):
            content_lines.append(line)
            in_content = True
    
    content = '\n'.join(content_lines)
    return title, slug, tags, description, content

def generate_article_md(title, slug, tags, description, content, date):
    """生成Hugo文章Markdown文件"""
    tags_yaml = '\n    - '.join(tags) if tags else ""
    
    frontmatter = f'''---
title: "{title}"
date: {date}
slug: {slug}
tags:
    - {tags_yaml}
description: "{description}"
---

{content}
'''
    return frontmatter

def main():
    today = datetime.date.today()
    today_str = today.isoformat()
    
    # 根据日期选择关键词（每天轮换）
    keyword_index = today.day % len(KEYWORDS)
    keyword = KEYWORDS[keyword_index]
    
    print(f"[{today_str}] 生成文章: {keyword}")
    
    # 生成提示词
    prompt = f"""请写一篇关于「{keyword}」的中文SEO文章。

要求：
1. 标题要包含关键词，25-30字，吸引人点击
2. 文章长度1500-2000字
3. 结构：引言 → 3-5个小标题（用###）→ 总结
4. 口语化，像业内人士分享经验
5. 适当使用小标题、列表、加粗等Markdown格式
6. 文章末尾加一句「关注公众号「供应链那些事」获取更多干货」
7. 不要写成广告，要有真实价值

输出格式（严格按这个格式）：
标题: [文章标题]
slug: [英文短链接，2-4个单词]
标签: [标签1, 标签2, 标签3]
描述: [150字以内的SEO描述]
正文:
[Markdown格式的文章内容]

请开始写："""
    
    # 调用AI生成
    try:
        ai_output = call_deepseek(prompt)
        title, slug, tags, description, content = parse_article(ai_output)
        
        if not title or not slug:
            print("解析失败，使用默认标题")
            title = f"{keyword}实战指南"
            slug = re.sub(r'[^\w-]', '', keyword.lower())[:30]
        
        # 生成文件
        content_dir = Path(SITE_DIR) / "content" / "posts"
        content_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{today_str}-{slug}.md"
        filepath = content_dir / filename
        
        md_content = generate_article_md(title, slug, tags, description, content, today_str)
        filepath.write_text(md_content, encoding='utf-8')
        
        print(f"[OK] 文章已生成: {filename}")
        print(f"     标题: {title}")
        print(f"     标签: {', '.join(tags)}")
        
    except Exception as e:
        print(f"[ERROR] 生成失败: {e}")
        raise

if __name__ == "__main__":
    main()

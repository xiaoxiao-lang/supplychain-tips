#!/usr/bin/env python3
"""
SEO文章自动生成脚本
每天跑一次，生成多篇SEO优化文章
用法: python generate_article.py [--count 10]
"""

import os, json, datetime, re, sys, random
from pathlib import Path

# 配置
SITE_DIR = r"D:\myseosite"
API_KEY = "sk-ffc7d8a98a3742f5a92b7f792c9c26b4"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# SEO关键词库 - 供应链行业
KEYWORDS = [
    "供应链管理", "采购流程优化", "库存管理技巧", "物流成本控制",
    "ERP系统实施", "供应商评估", "供应链金融", "仓储效率提升",
    "JIT准时制", "VMI供应商管理库存", "SKU管理", "供应链风险",
    "采购谈判技巧", "仓库KPI", "运输管理", "供应链数字化转型",
    "MRP物料需求计划", "供应链协同", "库存周转率", "采购成本分析",
    "跨境物流", "最后一公里配送", "逆向物流", "物流外包",
    "仓储自动化", "WMS系统", "RFID技术", "条码管理",
    "采购合同管理", "供应商关系管理", "TCO总拥有成本", "招标采购",
    "冷链物流", "危险品运输", "绿色供应链", "供应链可视化",
    "需求预测", "安全库存", "经济订货量", "ABC分类法",
]

def call_deepseek(prompt):
    """调用DeepSeek API生成内容"""
    import urllib.request
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.85,
        "max_tokens": 3000,
    }).encode('utf-8')
    req = urllib.request.Request(
        API_URL, data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    return result["choices"][0]["message"]["content"]

def parse_article(ai_output):
    """解析AI输出"""
    lines = ai_output.strip().split('\n')
    title = slug = description = ""
    tags = []
    content_lines = []
    in_content = False
    
    for line in lines:
        line = line.strip()
        if line.startswith("标题:"):
            title = line[3:].strip()
        elif line.startswith("slug:"):
            slug = line[5:].strip().lower().replace(' ', '-')
        elif line.startswith("标签:") or line.startswith("tags:"):
            raw = line[3:].strip() if "标签" in line else line[5:].strip()
            tags = [t.strip() for t in raw.replace('[','').replace(']','').split(',')]
        elif line.startswith("描述:") or line.startswith("description:"):
            description = line[3:].strip() if "描述" in line else line[12:].strip()
        elif line.startswith("正文:") or line.startswith("内容:") or line.startswith("# "):
            in_content = True
            if '# ' in line:
                content_lines.append(line)
        elif in_content or (line and ':' not in line[:5]):
            content_lines.append(line)
            in_content = True
    
    return title, slug, tags, description, '\n'.join(content_lines)

def generate_one(keyword, today_str, content_dir):
    """生成一篇文章"""
    prompt = f"""请写一篇关于「{keyword}」的中文SEO文章。

风格要求：年轻、网感、不端着。对标知乎高赞+公众号爆款文的风格。

标题要求（最重要）：
- 25字以内，短！狠！有情绪！
- 用数字、反差、悬念、扎心痛点吸引点击
- 参考风格：「月薪5千的采购和月薪5万的采购，差在这3点」「干了10年供应链，我劝你别踩这5个坑」「库存压了500万才明白的事」
- 不要「XX的XX」这种老套结构

文章要求：
1. 长度1500-2000字
2. 开篇用场景/痛点/故事代入，别上来就讲定义
3. 3-5个小标题（用###），每段别太长
4. 口语化，犀利干脆，像同行在群里唠嗑，不用敬语
5. 适当用「你」「我」这种第一人称
6. 排版：多用短句、列表、加粗
7. 文章末尾加一句「关注公众号「甲方乙方供应链」获取更多干货」
8. 有真实价值，别写废话

输出格式：
标题: [标题]
slug: [英文短链接，2-4个单词]
标签: [标签1, 标签2, 标签3]
描述: [150字以内的SEO描述]
正文:
[正文]

请开始写："""
    
    ai_output = call_deepseek(prompt)
    title, slug, tags, description, content = parse_article(ai_output)
    
    if not title or not slug:
        title = f"{keyword}实战分享"
        slug = re.sub(r'[^\w-]', '', keyword.lower())[:30]
    if not description:
        description = f"{keyword}的实战经验分享"
    
    # 避免slug重复
    slug = slug.lower().replace(' ', '-')[:50]
    filename = f"{today_str}-{slug}.md"
    filepath = content_dir / filename
    
    if filepath.exists():
        slug = f"{slug}-{random.randint(100,999)}"
        filename = f"{today_str}-{slug}.md"
        filepath = content_dir / filename
    
    tags_yaml = '\n    - '.join(tags) if tags else keyword
    md = f"""---
title: "{title}"
date: {today_str}
slug: {slug}
tags:
    - {tags_yaml}
description: "{description}"
---

{content}
"""
    filepath.write_text(md, encoding='utf-8')
    return filename, title, tags

def main():
    # 解析参数
    count = 10
    if len(sys.argv) > 1 and sys.argv[1] == '--count' and len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except:
            pass
    
    # 限制最大20篇/天
    count = min(count, 20)
    
    today = datetime.date.today()
    today_str = today.isoformat()
    content_dir = Path(SITE_DIR) / "content" / "posts"
    content_dir.mkdir(parents=True, exist_ok=True)
    
    # 今天已生成的文章数量
    existing_today = len(list(content_dir.glob(f"{today_str}-*.md")))
    print(f"今日已存在: {existing_today} 篇")
    
    # 已用过的关键词
    used_keywords = set()
    for f in content_dir.glob("*.md"):
        try:
            text = f.read_text(encoding='utf-8')
            for kw in KEYWORDS:
                if kw in text:
                    used_keywords.add(kw)
        except:
            pass
    
    # 选关键词：优先选没用过的
    available = [k for k in KEYWORDS if k not in used_keywords]
    if len(available) < count:
        available.extend(random.sample(KEYWORDS, count - len(available)))
    
    selected = random.sample(available, min(count, len(available)))
    
    print(f"开始生成 {len(selected)} 篇文章...")
    print(f"关键词: {', '.join(selected)}")
    print()
    
    ok = 0
    for i, keyword in enumerate(selected, 1):
        try:
            filename, title, tags = generate_one(keyword, today_str, content_dir)
            ok += 1
            print(f"[{i}/{len(selected)}] ✅ {title}")
        except Exception as e:
            print(f"[{i}/{len(selected)}] ❌ {keyword}: {e}")
    
    print(f"\n结果: {ok}/{len(selected)} 篇生成成功")
    print(f"目录: {content_dir}")

if __name__ == "__main__":
    main()

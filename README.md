# 供应链管理指南

专注供应链管理知识分享，从采购到物流，从入门到精通。

## 自动更新

每天自动生成一篇SEO优化文章，已配置定时任务。

## 技术栈

- Hugo静态网站生成器
- Cloudflare Pages免费托管
- DeepSeek AI自动生成文章

## 本地开发

```bash
# 编译
hugo

# 本地预览
hugo server

# 生成新文章
python scripts/generate_article.py

# 发布
./publish.bat
```

## 部署

推送到GitHub后，Cloudflare Pages自动部署。

访问: https://supplychain-tips.pages.dev/

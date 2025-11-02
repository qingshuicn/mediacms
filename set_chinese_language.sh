#!/bin/bash
# 设置 Django 管理后台为中文的脚本

echo "正在设置 Django 管理后台语言为简体中文..."

# 获取 CSRF token
CSRF_TOKEN=$(curl -s -c cookies.txt http://localhost:8080/admin/ | grep -oP 'csrfmiddlewaretoken.*?value="\K[^"]+')

echo "CSRF Token: $CSRF_TOKEN"

# 发送语言切换请求
curl -X POST http://localhost:8080/i18n/setlang/ \
  -b cookies.txt \
  -c cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Referer: http://localhost:8080/admin/" \
  -d "csrfmiddlewaretoken=$CSRF_TOKEN&language=zh-hans&next=/admin/"

echo ""
echo "语言设置完成！"
echo "请在浏览器中访问 http://localhost:8080/admin/ 并清除缓存（Ctrl+Shift+R）"
echo ""
echo "如果仍然显示英文，请："
echo "1. 清除浏览器 Cookie（F12 -> Application -> Cookies -> 删除 django_language）"
echo "2. 刷新页面"


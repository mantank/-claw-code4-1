#!/usr/bin/env bash
# ============================================================
# 公众号发布 SOP 脚本
# 将 Markdown 文章打包成公众号发布所需的全部素材
#
# 用法：
#   ./wechat-sop.sh <markdown文件路径>
#
# 示例：
#   ./wechat-sop.sh ~/articles/my-post.md
#
# 输出目录（与输入文件同目录，名为 <文件名>_wechat/）：
#   article.html    — 适合粘贴到 Markdown Nice 的 HTML
#   article.md      — 清理后的 Markdown 原文
#   cover.txt       — 封面图 AI 生成提示词
#   checklist.md    — 发布检查清单
# ============================================================

set -euo pipefail

if [[ $# -lt 1 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
  echo "用法: $0 <markdown文件路径>"
  echo "示例: $0 ~/articles/my-post.md"
  exit 1
fi

INPUT="$1"

if [[ ! -f "$INPUT" ]]; then
  echo "❌ 文件不存在: $INPUT"
  exit 1
fi

# 准备输出目录
BASENAME="$(basename "$INPUT" .md)"
OUTDIR="$(dirname "$INPUT")/${BASENAME}_wechat"
mkdir -p "$OUTDIR"

echo "📦 正在处理: $INPUT"
echo "📂 输出目录: $OUTDIR"

# ----------------------------------------------------------
# 1. 清理 Markdown 并生成 article.md
# ----------------------------------------------------------
# 将 markdown 表格转为列表格式，去除 front-matter
awk '
BEGIN { in_front=0; in_table=0 }
/^---$/ && NR<=3 { in_front=!in_front; next }
in_front { next }
# 表格转列表
/^\|.*\|$/ {
  if (!in_table) {
    in_table=1
    # 读取表头
    gsub(/^\||\|$/, "")
    n=split($0, headers, "|")
    for (i=1;i<=n;i++) gsub(/^ +| +$/, "", headers[i])
    next
  }
  # 跳过分隔行
  if ($0 ~ /^\|[-: |]+\|$/) next
  # 数据行
  gsub(/^\||\|$/, "")
  split($0, cells, "|")
  for (i=1;i<=n;i++) {
    gsub(/^ +| +$/, "", cells[i])
    if (cells[i] != "") printf "- **%s**: %s\n", headers[i], cells[i]
  }
  print ""
  next
}
{ in_table=0; print }
' "$INPUT" > "$OUTDIR/article.md"

echo "✅ article.md"

# ----------------------------------------------------------
# 2. 提取标题（第一个 # 标题）
# ----------------------------------------------------------
TITLE="$(grep -m1 '^#\s' "$OUTDIR/article.md" | sed 's/^#\+\s*//')"
if [[ -z "$TITLE" ]]; then
  TITLE="$BASENAME"
fi

# ----------------------------------------------------------
# 3. 生成 article.html（适配 Markdown Nice）
# ----------------------------------------------------------
# 尝试用 pandoc，否则用纯 bash 简易转换
if command -v pandoc &>/dev/null; then
  pandoc "$OUTDIR/article.md" \
    --from markdown --to html5 \
    --no-highlight \
    -o "$OUTDIR/article.html"
else
  # 简易 Markdown → HTML 转换
  python3 -c "
import re, sys, html as H

text = open(sys.argv[1], encoding='utf-8').read()
lines = text.split('\n')
out = []
in_code = False
in_ul = False
in_quote = False

for line in lines:
    # code block
    if line.startswith('\`\`\`'):
        if in_code:
            out.append('</code></pre>')
            in_code = False
        else:
            lang = line[3:].strip()
            out.append('<pre><code>' if not lang else f'<pre><code class=\"language-{lang}\">')
            in_code = True
        continue
    if in_code:
        out.append(H.escape(line))
        continue

    # close lists/quotes if needed
    if in_ul and not line.startswith(('- ', '* ', '  ')):
        out.append('</ul>')
        in_ul = False
    if in_quote and not line.startswith('>'):
        out.append('</blockquote>')
        in_quote = False

    # headings
    m = re.match(r'^(#{1,6})\s+(.*)', line)
    if m:
        n = len(m.group(1))
        out.append(f'<h{n}>{m.group(2)}</h{n}>')
        continue

    # blockquote
    if line.startswith('>'):
        if not in_quote:
            out.append('<blockquote>')
            in_quote = True
        out.append(re.sub(r'^>\s?', '', line) + '<br>')
        continue

    # list
    if re.match(r'^[-*]\s', line):
        if not in_ul:
            out.append('<ul>')
            in_ul = True
        content = re.sub(r'^[-*]\s', '', line)
        out.append(f'<li>{content}</li>')
        continue

    # empty line
    if not line.strip():
        out.append('')
        continue

    # paragraph
    out.append(f'<p>{line}</p>')

if in_ul: out.append('</ul>')
if in_quote: out.append('</blockquote>')
if in_code: out.append('</code></pre>')

# inline formatting
result = '\n'.join(out)
result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
result = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', result)
result = re.sub(r'\`([^\`]+?)\`', r'<code>\1</code>', result)
result = re.sub(r'\!\[([^\]]*)\]\(([^)]+)\)', r'<img src=\"\2\" alt=\"\1\">', result)
result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href=\"\2\">\1</a>', result)

print(result)
" "$OUTDIR/article.md" > "$OUTDIR/article.html"
fi

echo "✅ article.html"

# ----------------------------------------------------------
# 4. 生成封面图提示词 cover.txt
# ----------------------------------------------------------
# 从文章提取关键词用于提示词
KEYWORDS="$(grep -oP '(?<=\*\*).+?(?=\*\*)' "$OUTDIR/article.md" | head -5 | tr '\n' '、' | sed 's/、$//')"
if [[ -z "$KEYWORDS" ]]; then
  KEYWORDS="$TITLE"
fi

cat > "$OUTDIR/cover.txt" << EOF
请生成一张微信公众号封面图，要求如下：

风格：卡通插画风，扁平化设计，色彩鲜明活泼
尺寸：1920 x 1080 像素（16:9）
主题：${TITLE}
关键元素：${KEYWORDS}

构图要求：
- 画面简洁大气，主体突出
- 留出右侧或底部空间放标题文字
- 背景使用渐变或纯色，避免过于复杂
- 适合在手机端小图预览时仍能辨识主体

色调建议：科技蓝 / 活力橙 / 清新绿（根据主题选择）
EOF

echo "✅ cover.txt"

# ----------------------------------------------------------
# 5. 生成发布检查清单 checklist.md
# ----------------------------------------------------------
cat > "$OUTDIR/checklist.md" << EOF
# 📋 公众号发布检查清单

**文章标题：** ${TITLE}
**生成时间：** $(date '+%Y-%m-%d %H:%M')

---

- [ ] 标题确认（是否需要修改标题以提高打开率）
- [ ] 封面图已生成（使用 cover.txt 提示词生成 1920x1080 封面）
- [ ] 内容已粘贴到 Markdown Nice（打开 editor.mdnice.com）
- [ ] 预览效果检查（检查格式、图片、代码块显示）
- [ ] 复制到公众号后台（从 Markdown Nice 复制富文本）
- [ ] 摘要已填写
- [ ] 封面图已上传
- [ ] 预览发送到手机确认
- [ ] 发布

---

> 素材目录：\`${OUTDIR}\`
EOF

echo "✅ checklist.md"
echo ""
echo "🎉 全部素材已生成！"
echo "📂 $OUTDIR/"
ls -1 "$OUTDIR/"

const { createCanvas, registerFont } = require('canvas');
const fs = require('fs');
const path = require('path');

// Register fonts
registerFont('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc', { family: 'NotoSansCJK', weight: 'bold' });
registerFont('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc', { family: 'NotoSansCJK', weight: 'normal' });
registerFont('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc', { family: 'NotoSansCJK', weight: '500' });

const W = 1242, H = 1660;

function wrapText(ctx, text, maxWidth) {
  const lines = [];
  let line = '';
  for (const ch of text) {
    const test = line + ch;
    if (ctx.measureText(test).width > maxWidth && line) {
      lines.push(line);
      line = ch;
    } else {
      line = test;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function drawCard1(outPath) {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  // Background - warm gradient feel with solid color
  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0, 0, W, H);

  // Accent bar top
  const grad = ctx.createLinearGradient(0, 0, W, 0);
  grad.addColorStop(0, '#6366f1');
  grad.addColorStop(1, '#8b5cf6');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, 8);

  // Big emoji
  ctx.font = '160px "NotoSansCJK"';
  ctx.textAlign = 'center';
  ctx.fillText('🤯', W / 2, 300);

  // Title line 1
  ctx.font = 'bold 72px "NotoSansCJK"';
  ctx.fillStyle = '#ffffff';
  ctx.fillText('我让AI接管了知识库', W / 2, 460);

  // Title line 2 - accent color
  ctx.fillStyle = '#a78bfa';
  ctx.fillText('它比我整理得还好', W / 2, 560);

  // Divider
  const divGrad = ctx.createLinearGradient(W * 0.2, 0, W * 0.8, 0);
  divGrad.addColorStop(0, 'transparent');
  divGrad.addColorStop(0.5, '#6366f1');
  divGrad.addColorStop(1, 'transparent');
  ctx.strokeStyle = divGrad;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(W * 0.2, 620);
  ctx.lineTo(W * 0.8, 620);
  ctx.stroke();

  // Feature tags
  const tags = [
    { icon: '⚡', text: '20分钟搭建' },
    { icon: '🚫', text: '不用写代码' },
    { icon: '📱', text: '手机也能用' },
    { icon: '🆓', text: '免费工具' },
  ];

  const tagY = 720;
  const tagW = 500, tagH = 90, tagGap = 30;
  const startX = (W - tagW * 2 - tagGap) / 2;
  const startY = tagY;

  tags.forEach((tag, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = startX + col * (tagW + tagGap);
    const y = startY + row * (tagH + tagGap);

    // Tag background
    ctx.fillStyle = 'rgba(99, 102, 241, 0.15)';
    roundRect(ctx, x, y, tagW, tagH, 16);
    ctx.fill();

    // Tag border
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.3)';
    ctx.lineWidth = 1.5;
    roundRect(ctx, x, y, tagW, tagH, 16);
    ctx.stroke();

    // Tag text
    ctx.font = '40px "NotoSansCJK"';
    ctx.fillStyle = '#e0e7ff';
    ctx.textAlign = 'center';
    ctx.fillText(`${tag.icon} ${tag.text}`, x + tagW / 2, y + 58);
  });

  // Bottom section - what it does
  const bottomY = 1060;
  ctx.textAlign = 'left';
  const leftPad = 120;

  const items = [
    { emoji: '📎', text: '丢个链接 → AI自动总结归档' },
    { emoji: '📚', text: '14万字 → 一晚整理完毕' },
    { emoji: '🔍', text: '找资料 → 问一句话搞定' },
  ];

  items.forEach((item, i) => {
    const y = bottomY + i * 100;
    ctx.font = '44px "NotoSansCJK"';
    ctx.fillStyle = '#c4b5fd';
    ctx.fillText(item.emoji, leftPad, y);
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '40px "NotoSansCJK"';
    ctx.fillText(item.text, leftPad + 70, y);
  });

  // Footer
  ctx.textAlign = 'center';
  ctx.font = '32px "NotoSansCJK"';
  ctx.fillStyle = 'rgba(255,255,255,0.4)';
  ctx.fillText('深夜开发者LND', W / 2, H - 80);

  // Accent bar bottom
  ctx.fillStyle = grad;
  ctx.fillRect(0, H - 8, W, 8);

  // Save
  const buf = canvas.toBuffer('image/png');
  fs.writeFileSync(outPath, buf);
  console.log('Saved:', outPath, 'Size:', buf.length);
}

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

const outDir = path.join(__dirname, '..', 'content', 'xhs');
fs.mkdirSync(outDir, { recursive: true });
drawCard1(path.join(outDir, 'cover.png'));

const { createCanvas, registerFont } = require('canvas');
const fs = require('fs');
const path = require('path');

registerFont('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc', { family: 'Noto', weight: 'bold' });
registerFont('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc', { family: 'Noto', weight: 'normal' });
registerFont('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc', { family: 'Noto', weight: '500' });

const W = 1242, H = 1660;

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

function drawCover(outPath) {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  // Dark background
  ctx.fillStyle = '#111111';
  ctx.fillRect(0, 0, W, H);

  // Top accent gradient bar
  const topGrad = ctx.createLinearGradient(0, 0, W, 0);
  topGrad.addColorStop(0, '#7c3aed');
  topGrad.addColorStop(1, '#2563eb');
  ctx.fillStyle = topGrad;
  ctx.fillRect(0, 0, W, 6);

  // Large decorative circle (subtle)
  ctx.beginPath();
  ctx.arc(W / 2, 280, 140, 0, Math.PI * 2);
  const circGrad = ctx.createRadialGradient(W / 2, 280, 0, W / 2, 280, 140);
  circGrad.addColorStop(0, 'rgba(124, 58, 237, 0.3)');
  circGrad.addColorStop(1, 'rgba(124, 58, 237, 0)');
  ctx.fillStyle = circGrad;
  ctx.fill();

  // "AI" text inside circle
  ctx.font = 'bold 120px "Noto"';
  ctx.fillStyle = '#a78bfa';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('AI', W / 2, 280);

  // Title
  ctx.textBaseline = 'alphabetic';
  ctx.font = 'bold 76px "Noto"';
  ctx.fillStyle = '#ffffff';
  ctx.fillText('我让AI接管了知识库', W / 2, 500);

  ctx.fillStyle = '#c084fc';
  ctx.font = 'bold 76px "Noto"';
  ctx.fillText('它比我整理得还好', W / 2, 600);

  // Thin divider
  ctx.strokeStyle = 'rgba(124, 58, 237, 0.4)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(200, 660);
  ctx.lineTo(W - 200, 660);
  ctx.stroke();

  // 4 feature tags in 2x2 grid
  const tags = ['20分钟搭建', '不用写代码', '手机也能用', '完全免费'];
  const icons = ['>', '/>', '[ ]', '$0'];  // simple ascii symbols
  const tagW = 480, tagH = 100, gap = 30;
  const sx = (W - tagW * 2 - gap) / 2;
  const sy = 720;

  tags.forEach((tag, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = sx + col * (tagW + gap);
    const y = sy + row * (tagH + gap);

    ctx.fillStyle = 'rgba(124, 58, 237, 0.12)';
    roundRect(ctx, x, y, tagW, tagH, 14);
    ctx.fill();
    ctx.strokeStyle = 'rgba(124, 58, 237, 0.25)';
    ctx.lineWidth = 1.5;
    roundRect(ctx, x, y, tagW, tagH, 14);
    ctx.stroke();

    // Dot indicator
    ctx.beginPath();
    ctx.arc(x + 40, y + tagH / 2, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#7c3aed';
    ctx.fill();

    ctx.font = '42px "Noto"';
    ctx.fillStyle = '#e0e7ff';
    ctx.textAlign = 'left';
    ctx.fillText(tag, x + 65, y + tagH / 2 + 14);
  });

  // 3 key points
  ctx.textAlign = 'left';
  const points = [
    ['>>>', '丢个链接 → AI自动总结归档'],
    ['>>>', '14万字 → 一晚整理完毕'],
    ['>>>', '找资料 → 问一句话搞定'],
  ];
  const py = 1100;
  points.forEach((p, i) => {
    const y = py + i * 110;
    // Arrow indicator
    ctx.fillStyle = '#7c3aed';
    ctx.font = 'bold 36px "Noto"';
    ctx.fillText('▸', 120, y);
    // Text
    ctx.font = '44px "Noto"';
    ctx.fillStyle = '#d1d5db';
    ctx.fillText(p[1], 170, y);
  });

  // Footer
  ctx.textAlign = 'center';
  ctx.font = '30px "Noto"';
  ctx.fillStyle = 'rgba(255,255,255,0.35)';
  ctx.fillText('深夜开发者LND  |  普通人也能用好的AI', W / 2, H - 80);

  // Bottom accent bar
  ctx.fillStyle = topGrad;
  ctx.fillRect(0, H - 6, W, 6);

  const buf = canvas.toBuffer('image/png');
  fs.writeFileSync(outPath, buf);
  console.log('Saved:', outPath, buf.length, 'bytes');
}

const outDir = path.join(__dirname, '..', 'content', 'xhs');
fs.mkdirSync(outDir, { recursive: true });
drawCover(path.join(outDir, 'cover-v2.png'));

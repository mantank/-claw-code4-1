import { Document, Packer, Paragraph, TextRun, HeadingLevel, TableCell, TableRow, Table, WidthType, BorderStyle, AlignmentType } from "docx";
import { writeFileSync } from "fs";

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        text: "折腾了一晚上，终于在 Linux 服务器上把 OpenClaw 跑起来了",
        heading: HeadingLevel.HEADING_1,
        alignment: AlignmentType.CENTER,
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "一个非程序员的 OpenClaw 部署踩坑实录", color: "888888", size: 24 })],
        spacing: { after: 400 },
      }),
      new Paragraph({ children: [new TextRun({ text: "我不是程序员。", bold: true })] }),
      new Paragraph({ text: "但昨晚花了大概三个小时，把自己的 AI 助手部署到了 Telegram 上。中间踩了不少坑，全记下来了，希望能帮到后来人。", spacing: { after: 200 } }),

      // What is OpenClaw
      new Paragraph({ text: "OpenClaw 是什么", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "简单讲：装好 OpenClaw，你就有了一个 24 小时在线的私人 AI 助手 Bot。它是个开源框架，能把 Claude、GPT 这些大模型接到 Telegram、WhatsApp 上。不用开网页，手机上随时跟 AI 聊。", spacing: { after: 200 } }),

      // Env
      new Paragraph({ text: "部署前准备", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "我用的是腾讯云 OpenCloudOS 服务器。你需要提前准备：", spacing: { after: 100 } }),
      new Paragraph({ text: "• 一台 Linux 服务器（CentOS / Ubuntu / OpenCloudOS 都行）", indent: { left: 360 } }),
      new Paragraph({ text: "• Anthropic API Key（去 console.anthropic.com 申请）", indent: { left: 360 } }),
      new Paragraph({ text: "• Telegram Bot Token（通过 @BotFather 创建）", indent: { left: 360 } }),
      new Paragraph({ text: "• 你的 Telegram 用户 ID（用 @userinfobot 查）", indent: { left: 360 }, spacing: { after: 200 } }),

      // Pit 1
      new Paragraph({ text: "坑 1：Node.js 装不上", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "OpenClaw 跑在 Node.js 上，得先装。官方脚本跑到一半报错了，说不支持当前系统。我的 OpenCloudOS 虽然是 RPM 系的，但它就是不认。", spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "解决：", bold: true }), new TextRun("别用官方脚本，手动来。")], spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "dnf install -y nodejs npm", font: "Courier New", size: 22 })], shading: { fill: "F0F0F0" }, spacing: { after: 100 } }),
      new Paragraph({ text: "或者用 nvm（推荐，兼容性更好）：", spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash\nsource ~/.bashrc\nnvm install --lts", font: "Courier New", size: 22 })], shading: { fill: "F0F0F0" }, spacing: { after: 200 } }),

      // Pit 2
      new Paragraph({ text: "坑 2：缺 Git", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "npm 装 OpenClaw 时报错：npm error path git errno -2。系统没自带 git，一行搞定：", spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "dnf install -y git", font: "Courier New", size: 22 })], shading: { fill: "F0F0F0" }, spacing: { after: 200 } }),

      // Install
      new Paragraph({ text: "安装和配置", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ children: [new TextRun({ text: "npm install -g openclaw@latest\nopenclaw onboard", font: "Courier New", size: 22 })], shading: { fill: "F0F0F0" }, spacing: { after: 200 } }),
      new Paragraph({ text: "会弹出交互式菜单，主要填四个东西：", spacing: { after: 100 } }),
      new Paragraph({ text: "1. 模型和 API Key — 选模型，填 Anthropic 的 Key", indent: { left: 360 } }),
      new Paragraph({ text: "2. Telegram Bot Token — BotFather 给你的那串", indent: { left: 360 } }),
      new Paragraph({ text: "3. Telegram 用户 ID — @userinfobot 查到的数字", indent: { left: 360 } }),
      new Paragraph({ text: "4. 工作目录 — 默认就行", indent: { left: 360 }, spacing: { after: 200 } }),

      // Model table
      new Paragraph({ text: "模型怎么选？", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ children: [new TextRun({ text: "建议：先拿 Sonnet 4.5 跑通流程，确认没问题再换 Opus。", bold: true, color: "E67E22" })], spacing: { after: 100 } }),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [
          new TableRow({ children: [
            new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "模型", bold: true })] })] }),
            new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "价格", bold: true })] })] }),
            new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "体验", bold: true })] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ children: [new Paragraph("Opus 4.6")] }),
            new TableCell({ children: [new Paragraph("$5 / $25")] }),
            new TableCell({ children: [new Paragraph("最强，需高等级账户")] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ children: [new Paragraph("Opus 4.5")] }),
            new TableCell({ children: [new Paragraph("$5 / $25")] }),
            new TableCell({ children: [new Paragraph("旗舰，性价比最高")] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ children: [new Paragraph("Sonnet 4.5")] }),
            new TableCell({ children: [new Paragraph("$3 / $15")] }),
            new TableCell({ children: [new Paragraph("日常够用，推荐起步")] }),
          ]}),
        ],
      }),

      // Pit 3
      new Paragraph({ text: "坑 3：API Key 404", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "配好之后给 Bot 发消息，回了个 HTTP 404。折腾了半天，发现是 Key 的问题。用 curl 直接测最快：", spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: 'curl -X POST https://api.anthropic.com/v1/messages \\\n  -H "x-api-key: 你的KEY" \\\n  -H "content-type: application/json" \\\n  -H "anthropic-version: 2023-06-01" \\\n  -d \'{"model":"claude-sonnet-4-5-20250929","max_tokens":100,\n       "messages":[{"role":"user","content":"hello"}]}\'', font: "Courier New", size: 20 })], shading: { fill: "F0F0F0" }, spacing: { after: 200 } }),
      new Paragraph({ text: "返回 authentication_error 就是 Key 有问题，去 console.anthropic.com 重新生成。", spacing: { after: 200 } }),

      // Pairing
      new Paragraph({ text: "配对 Telegram", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "第一次给 Bot 发消息，它会回一串配对码。回到服务器上跑：", spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "openclaw pairing approve telegram KW39NZUZ", font: "Courier New", size: 22 })], shading: { fill: "F0F0F0" }, spacing: { after: 200 } }),

      // Commands
      new Paragraph({ text: "常用命令速查", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ children: [new TextRun({ text: "openclaw status          # 看运行状态\nopenclaw gateway restart # 重启\nopenclaw logs --follow   # 实时日志\nopenclaw doctor          # 出问题先跑这个\nnpm update -g openclaw   # 更新版本", font: "Courier New", size: 22 })], shading: { fill: "F0F0F0" }, spacing: { after: 200 } }),

      // Limits
      new Paragraph({ text: "已知限制", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ children: [new TextRun({ text: "微信公众号文章读不了。", bold: true }), new TextRun("AI 用浏览器访问会被微信拦截。目前只能手动复制内容给它处理。")] }),
      new Paragraph({ children: [new TextRun({ text: "Telegram 默认英文。", bold: true }), new TextRun("搜索 setlanguage/zh-hans-raw 一键切换简体中文。")], spacing: { after: 200 } }),

      // Summary
      new Paragraph({ text: "总结", heading: HeadingLevel.HEADING_2, spacing: { before: 400 } }),
      new Paragraph({ text: "整个过程顺利的话 30 分钟，算上踩坑两三个小时。主要卡在四个地方：", spacing: { after: 100 } }),
      new Paragraph({ text: "1. 系统兼容 — OpenCloudOS 得手动装 Node.js 和 Git", indent: { left: 360 } }),
      new Paragraph({ text: "2. API Key — 先用 curl 测一下，别瞎猜", indent: { left: 360 } }),
      new Paragraph({ text: "3. 模型权限 — 不是所有 Key 都能用 Opus，先拿 Sonnet 试", indent: { left: 360 } }),
      new Paragraph({ text: "4. 配对 — 别忘了在服务器上跑 approve 命令", indent: { left: 360 }, spacing: { after: 200 } }),
      new Paragraph({ text: "部署好之后，你就有了一个 24 小时在线、随叫随到的 AI 助手。", spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "值得折腾。", bold: true, size: 28 })] }),
    ],
  }],
});

const buffer = await Packer.toBuffer(doc);
writeFileSync("/root/.openclaw/workspace/content/OpenClaw部署踩坑实录.docx", buffer);
console.log("Done!");

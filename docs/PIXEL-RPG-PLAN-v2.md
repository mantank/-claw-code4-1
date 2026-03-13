# xiaolongxia.app 像素RPG版 · 完整执行计划 v2

> 制定：004 | 审核修订：001 | 日期：2026-03-13
> 基于现有 Astro + Tailwind 代码库，保证每一步可执行
> 当前已有：Press Start 2P 字体 ✅ | --font-pixel 变量 ✅ | 品牌色系 ✅

---

## 与 v1 的主要变更

| 变更项 | v1 | v2 |
|--------|----|----|
| Zpix字体 | 直接加载完整字体（~2MB） | subset裁剪到≤100KB，仅保留标题/按钮用字 |
| 数据补全（任务7.1） | 第11-14天执行 | **提前到第1天**，与样式基础并行 |
| 等级体系（3.5） | 第一期做 | **砍掉，移到第二期**（无用户系统支撑） |
| 灰度策略 | 一口气全站换皮 | **分两批上线**：首页+副本页先上，看数据再铺开 |
| 移动端适配 | 仅底部Tab栏 | **新增1.4子任务**，专门处理移动端像素风适配 |
| 工时估算 | 33小时 | **45小时**（含buffer） |
| 牧场模块 | 60小时 | **20小时** |

---

## 前置说明

### 现有代码已完成的部分（不用重复做）

| 已完成 | 文件位置 |
|--------|---------|
| Press Start 2P 英文像素字体已加载 | `src/layouts/BaseLayout.astro` |
| VT323 字体已加载 | `src/layouts/BaseLayout.astro` |
| `--font-pixel` CSS 变量已定义 | `src/styles/global.css` |
| 品牌龙虾红色系已定义 | `src/styles/global.css` |
| 技能秘籍页面（15个）已上线 | `/skills/[slug]` |
| 套装页面（5套）已上线 | `/skills/combos` |
| 教程详情页（22章）已上线 | `/tutorials/[slug]` |
| 副本/场景案例（221个）已上线 | `/cases/[slug]` |

### 关键文件路径

```
src/config.ts          ← 导航栏名称（改这里）
src/styles/global.css  ← 全局样式（加像素风CSS）
src/layouts/BaseLayout.astro ← HTML骨架
src/pages/index.astro  ← 首页
src/pages/cases/index.astro  ← 副本列表
src/pages/skills/index.astro ← 秘籍总览
src/pages/tutorials/index.astro ← 新手村
src/data/site-content.ts ← 页面数据
```

---

## 灰度上线策略（重要）

**不一口气全站换皮。分两批，降低风险：**

### 第一批（第1-6天）
- 像素风基础样式 + 首页 + 副本列表/详情页
- 上线后观察3天：跳出率、页面停留时间、副本点击率
- 数据OK → 启动第二批
- 数据差 → 用CSS开关回滚（`body.pixel-mode` 类名控制）

### 第二批（第7-12天）
- 秘籍页 + 新手村 + 套装页
- 内容补充收尾

### CSS回滚开关
在 `BaseLayout.astro` 的 `<body>` 上加 `class="pixel-mode"`，所有像素风样式都写在 `.pixel-mode` 作用域下：
```css
.pixel-mode .pixel-card { ... }
.pixel-mode .pixel-btn { ... }
```
去掉这个class，瞬间回到旧版。零风险。

---

## 任务〇：数据补全（与任务一并行，第1天启动）

> **目标：确保前端页面有数据可展示，不做空壳**
> **预计耗时：3小时**

### 任务 0.1：批量补全案例RPG字段

**文件：** `src/content/cases/*.md` 的 frontmatter

为现有 221 个案例补充：
- `timeSaved: "X小时/天"` 字段（掉落显示用）
- `difficulty: 1-3` 字段（星级难度）
- 补全空的 `tools` 字段（用于关联秘籍）

**执行方式：**
1. Python脚本扫描所有案例，根据 category 和 description 自动推断默认值
2. 重点案例（首页TOP5展示的）人工精修
3. 其余用默认值（difficulty=2, timeSaved="1小时/次"），后续迭代修正

**耗时：2小时**（脚本批量+人工审核TOP20）
**前置：无，第1天立即启动**

### 任务 0.2：补充P2技能（13个）

**文件：** `src/content/skills/*.md`（新建）

每个技能需要：
- 一句话描述
- 踩坑提醒（2-3条）
- 常见搭配（1-2组）

**耗时：3小时**（脚本生成框架+手动补内容）
**前置：无，可与0.1并行**
**注意：** 第一批上线不强依赖P2技能，优先级低于0.1

---

## 任务一：像素风基础样式体系

> **目标：建立统一的像素风视觉语言，后续所有页面依赖这一套**
> **预计总耗时：6小时**

### 任务 1.1：引入 Zpix 中文像素字体（subset版）

**文件：**
- `public/fonts/zpix-subset.woff2`（裁剪后≤100KB）
- `src/styles/global.css`（添加 @font-face）

**操作：**
```bash
# 1. 下载完整 Zpix 字体
# https://github.com/SolidZORO/zpix-pixel-font/releases

# 2. 用 fonttools 裁剪，只保留网站用到的汉字
pip install fonttools brotli
cat > subset-chars.txt << 'EOF'
大本营龙虾副本秘籍新手村养一只你的龙虾副本攻略秘籍书库套装配方从新手到虾皇
从新手村开始直接挑副本热门掉落已验证待验证内容矿洞效率竞技场日常任务代码熔炉
情报暗哨学会一招变强一分几本秘籍凑一套威力翻倍每个龙虾养成之路的起点主线任务
进阶修炼任务奖励上一个下一个输入你想解决的问题打一个省一天被个副本引用
安装查看详情返回列表搜索全部分类难度时间技能组合推荐踩坑提醒常见搭配
本秘籍个副本套套装位虾农星小时天次分钟周月年节省提效自动化
EOF

pyftsubset zpix.ttf \
  --text-file=subset-chars.txt \
  --output-file=zpix-subset.woff2 \
  --flavor=woff2
# 预计输出 50-100KB
```

在 `global.css` 顶部添加：
```css
@font-face {
  font-family: 'Zpix';
  src: url('/fonts/zpix-subset.woff2') format('woff2');
  font-display: swap;
}
```

更新 `--font-pixel` 变量：
```css
--font-pixel: 'Zpix', 'Press Start 2P', 'VT323', monospace;
```

**耗时：1小时**（含字体裁剪调试）
**前置：无**
**验证：** 中文标题渲染出像素点阵效果，字体文件≤100KB

---

### 任务 1.2：创建像素风 CSS 组件库

**文件：** `src/styles/pixel.css`（新建，在 global.css 中 @import）

**所有样式必须在 `.pixel-mode` 作用域下，支持一键回滚：**

```css
/* ── 像素风颜色变量 ──────────────────────── */
.pixel-mode {
  --px-green: #4CAF50;
  --px-brown: #8D6E63;
  --px-blue: #64B5F6;
  --px-red: #EF5350;
  --px-gold: #FFD54F;
  --px-cream: #FFF8E1;
  --px-black: #212121;
  --px-border: 3px solid #212121;
  --px-shadow: 4px 4px 0px #212121;
  --px-shadow-gold: 4px 4px 0px #B8860B;
  --px-shadow-red: 4px 4px 0px #8B0000;
}

/* ── 像素风按钮 ──────────────────────────── */
.pixel-mode .pixel-btn {
  font-family: var(--font-pixel);
  font-size: 0.7rem;
  padding: 10px 20px;
  border: var(--px-border);
  box-shadow: var(--px-shadow);
  cursor: pointer;
  transition: none; /* 像素风不要平滑过渡 */
}
.pixel-mode .pixel-btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px #212121;
}
.pixel-mode .pixel-btn:active {
  transform: translate(3px, 3px);
  box-shadow: none;
}
.pixel-mode .pixel-btn-primary { background: #212121; color: #FFF8E1; }
.pixel-mode .pixel-btn-danger  { background: #EF5350; color: #fff; }
.pixel-mode .pixel-btn-gold    { background: #FFD54F; color: #212121; }

/* ── 像素风卡片 ──────────────────────────── */
.pixel-mode .pixel-card {
  border: var(--px-border);
  box-shadow: var(--px-shadow);
  background: var(--px-cream);
}
.pixel-mode .pixel-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px #212121;
}

/* ── 像素风徽章/标签 ─────────────────────── */
.pixel-mode .pixel-badge {
  font-family: var(--font-pixel);
  font-size: 0.6rem;
  padding: 2px 8px;
  border: 2px solid #212121;
}
.pixel-mode .pixel-badge-green  { background: #4CAF50; color: white; }
.pixel-mode .pixel-badge-gold   { background: #FFD54F; color: #212121; }
.pixel-mode .pixel-badge-red    { background: #EF5350; color: white; }
.pixel-mode .pixel-badge-blue   { background: #64B5F6; color: white; }

/* ── 像素风血条/进度条 ───────────────────── */
.pixel-mode .pixel-bar-wrap {
  border: var(--px-border);
  height: 20px;
  background: #e0e0e0;
}
.pixel-mode .pixel-bar-fill { height: 100%; image-rendering: pixelated; }
.pixel-mode .pixel-bar-hp   { background: #EF5350; }
.pixel-mode .pixel-bar-mp   { background: #64B5F6; }
.pixel-mode .pixel-bar-xp   { background: #AB47BC; }

/* ── 像素风分割线 ────────────────────────── */
.pixel-mode .pixel-divider { border: none; border-top: 3px solid #212121; }
.pixel-mode .pixel-divider-gold { border-top: 3px solid #FFD54F; }

/* ── 星级难度 ────────────────────────────── */
.pixel-mode .pixel-stars { font-family: var(--font-pixel); letter-spacing: 2px; }

/* ── 掉落物标签 ──────────────────────────── */
.pixel-mode .pixel-drop {
  background: var(--px-cream);
  border: 2px solid var(--px-gold);
  color: #5D4037;
}
```

**耗时：3小时**
**前置：1.1 完成**
**验证：** 在临时测试页能看到所有组件正常渲染

---

### 任务 1.3：更新全局 body 背景

**文件：** `src/styles/global.css`

把现有渐变背景改为像素风米色纹理（仅在 pixel-mode 下生效）：
```css
body.pixel-mode {
  background-color: #f5f0e8; /* 羊皮纸米色 */
  background-image:
    radial-gradient(circle, rgba(33,33,33,0.03) 1px, transparent 1px);
  background-size: 24px 24px; /* 像素格子底纹 */
}
```

**耗时：30分钟**
**前置：无，可与 1.2 并行**
**注意：** 格子底纹透明度控制在 3% 以内，不影响可读性

---

### 任务 1.4：移动端像素风适配（v2新增）

**文件：** `src/styles/pixel.css` 底部添加响应式规则

**核心问题：** 像素风的粗边框、小字号在手机上会很难看。

```css
/* ── 移动端适配（<768px） ────────────────── */
@media (max-width: 767px) {
  .pixel-mode {
    --px-border: 2px solid #212121;  /* 边框减细 */
    --px-shadow: 3px 3px 0px #212121; /* 阴影缩小 */
  }

  .pixel-mode .pixel-btn {
    font-size: 0.65rem;
    padding: 8px 14px;
  }

  .pixel-mode .pixel-badge {
    font-size: 0.5rem;
    padding: 1px 6px;
  }

  .pixel-mode .pixel-card {
    margin-bottom: 12px;
  }

  /* 卡片列表强制单列 */
  .pixel-mode .card-grid {
    grid-template-columns: 1fr !important;
  }

  /* 像素字体标题在手机上放大一点，否则看不清 */
  .pixel-mode h1 { font-size: 1.2rem; }
  .pixel-mode h2 { font-size: 1rem; }
  .pixel-mode h3 { font-size: 0.85rem; }
}
```

**耗时：1.5小时**
**前置：1.2 完成**
**验证：** 在Chrome DevTools模拟iPhone SE/iPhone 14两个尺寸，卡片不溢出、文字可读

---

## 任务二：导航栏重命名 + 像素风改造

> **目标：把网站的游戏感第一时间传达给用户**
> **预计总耗时：3小时**

### 任务 2.1：修改导航栏名称

**文件：** `src/config.ts`

```typescript
// 改前
nav: [
  { name: '首页', href: '/' },
  { name: '场景案例', href: '/cases' },
  { name: '技能商店', href: '/skills' },
  { name: '教程中心', href: '/tutorials' },
],

// 改后
nav: [
  { name: '🏠 大本营', href: '/' },
  { name: '⚔️ 龙虾副本', href: '/cases' },
  { name: '📜 龙虾秘籍', href: '/skills' },
  { name: '🌱 新手村', href: '/tutorials' },
],
```

同步更新 `SITE_CONFIG.title` 和 `description`：
```typescript
title: '🦞 小龙虾 · OpenClaw 中文实战站',
description: '养一只你的 AI 龙虾——副本攻略、秘籍书库、套装配方，从新手到虾皇',
```

**耗时：20分钟**
**前置：无**

---

### 任务 2.2：改造 Header 组件为像素风

**文件：** `src/components/Header.astro`

核心改动：
- 导航链接字体改为 `font-pixel`
- Logo 文字加像素风样式
- hover 效果改为像素位移（不用圆角渐变）
- 背景改为米白色 + 黑色粗边框底部线

```css
.pixel-mode .nav-link {
  font-family: var(--font-pixel);
  font-size: 0.6rem;
  letter-spacing: 0.05em;
  border: 2px solid transparent;
  padding: 6px 10px;
}
.pixel-mode .nav-link:hover {
  border-color: #212121;
  box-shadow: 2px 2px 0 #212121;
  transform: translate(-1px, -1px);
}
.pixel-mode .nav-link.active {
  background: #212121;
  color: #FFF8E1;
}
```

**耗时：1.5小时**
**前置：1.2 完成**

---

### 任务 2.3：手机端底部 Tab 栏

**文件：** 在 `BaseLayout.astro` 底部添加移动端 Tab

```html
<!-- 手机端固定底部导航（仅pixel-mode） -->
<nav class="pixel-bottom-tab md:hidden">
  <a href="/">🏠<span>大本营</span></a>
  <a href="/cases">⚔️<span>副本</span></a>
  <a href="/skills">📜<span>秘籍</span></a>
  <a href="/tutorials">🌱<span>新手村</span></a>
</nav>
```

```css
.pixel-mode .pixel-bottom-tab {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; background: #FFF8E1;
  border-top: 3px solid #212121;
  z-index: 50;
  padding-bottom: env(safe-area-inset-bottom); /* iOS安全区 */
}
.pixel-mode .pixel-bottom-tab a {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; padding: 8px 4px;
  font-family: var(--font-pixel); font-size: 0.45rem;
}
```

**耗时：1小时**（含 iOS 安全区适配）
**前置：2.2 完成**
**注意：** 底部Tab存在时，页面底部需要加 `padding-bottom: 60px` 防止内容被遮挡

---

## 任务三：首页像素RPG改版

> **目标：首页变成游戏大厅，用户一眼看懂这是个游戏化网站**
> **预计总耗时：5小时**

### 任务 3.1：Hero 区域改版

**文件：** `src/pages/index.astro` Hero 部分

改动内容：
- 背景改为像素格子 + 米色
- 标题字体改为像素风
- 副标题保持正文字体（保证可读性）
- CTA 按钮改为像素风按钮（黑边 + 阴影下沉效果）
- 用大 emoji 🦞 临时占位（等真实像素画）

```html
<section class="pixel-hero">
  <div class="pixel-mascot">🦞</div>
  <h1 class="pixel-title">养一只你的 AI 龙虾</h1>
  <p class="pixel-subtitle">
    副本攻略 · 秘籍书库 · 套装配方 · 从新手到虾皇
  </p>
  <div class="pixel-cta-row">
    <a href="/tutorials" class="pixel-btn pixel-btn-primary">
      🌱 从新手村开始
    </a>
    <a href="/cases" class="pixel-btn pixel-btn-danger">
      ⚔️ 直接挑副本
    </a>
  </div>
</section>
```

**耗时：2小时**
**前置：1.2 完成**

---

### 任务 3.2：「农场数据」统计模块

**文件：** `src/pages/index.astro` 数据区域

用像素风卡片替换现有数字统计：

```
╔══════════╦══════════╦══════════╦══════════╗
║ 📜 15   ║ ⚔️ 221  ║ 🎒 5    ║ 📖 22   ║
║ 本秘籍   ║ 个副本   ║ 套套装   ║ 章教程   ║
╚══════════╩══════════╩══════════╩══════════╝
```

每个数字格子用 `.pixel-card` 样式，标题用像素字体。
数字从 `getCollection()` 动态获取，不硬编码。

**耗时：1小时**
**前置：3.1 完成**

---

### 任务 3.3：「热门副本 TOP5」模块

**文件：** `src/pages/index.astro`
**数据来源：** 从 `getCollection('cases')` 取 `order` 最小的 5 条

像素风排行榜样式：
```
🔥 热门副本
──────────────────────────────────
1. ⚔️ 公众号全自动写稿  ★★★  掉落：3小时/天
2. ⚔️ 飞书日报自动生成  ★★☆  掉落：1小时/天
3. ⚔️ GitHub Issues自动修复  ★★★  掉落：2小时/次
──────────────────────────────────
```

每行用像素风行样式，hover 时左侧出现 `▸` 光标。

**耗时：1.5小时**
**前置：3.2 完成**
**依赖：** 任务0.1的数据补全（difficulty和timeSaved字段）

---

### 任务 3.4：「副本地图」六大区域入口

**文件：** `src/pages/index.astro`
**数据来源：** 复用现有 cases 的 category 分类

6个区域入口卡片（像素风，emoji 占位区域图）：

| 区域 | 原分类 | Emoji | 链接 |
|------|--------|-------|------|
| ⛏️ 内容矿洞 | 社交与内容 | ⛏️ | /cases?category=社交与内容 |
| ⚡ 效率竞技场 | 办公效率 | ⚡ | /cases?category=办公效率 |
| 🏡 日常任务 | 生活助手 | 🏡 | /cases?category=生活助手 |
| 🔥 代码熔炉 | 开发工具 | 🔥 | /cases?category=开发工具 |
| 🕵️ 情报暗哨 | 数据与监控 | 🕵️ | /cases?category=数据与监控 |
| 🌱 新手村 | 入门上手 | 🌱 | /tutorials |

**耗时：1.5小时**
**前置：3.2 完成**
**注意：** 现有 cases 的 category 字段已分好类，直接复用筛选 URL

---

## ── 第一批上线节点 ──

> **完成任务0-4后，部署上线，观察3天数据。**
> **观察指标：首页跳出率、副本页点击率、平均停留时间。**
> **数据OK → 继续第二批。数据差 → 去掉 body 的 `pixel-mode` class 回滚。**

---

## 任务四：龙虾副本页改版（场景案例）

> **目标：把技术性的「场景案例」改造为 RPG 副本风格**
> **预计总耗时：5小时**

### 任务 4.1：副本列表页改版

**文件：** `src/pages/cases/index.astro`

改动：
- 页头改为 `⚔️ 龙虾副本` + 副标题「打一个，省一天」
- 分类筛选改为六大区域（内容矿洞/效率竞技场等）
- 搜索框保留，placeholder 改为「输入你想解决的问题...」
- 副本卡片改为像素风（见 4.2）

**耗时：2小时**
**前置：1.2 完成**

---

### 任务 4.2：副本卡片像素风化

**文件：** `src/pages/cases/index.astro` 中的卡片部分

```html
<div class="pixel-card case-dungeon-card">
  <div class="dungeon-bar bar-{difficulty}"></div>
  <div class="dungeon-body">
    <div class="dungeon-badges">
      <span class="pixel-badge pixel-badge-green">🟢 已验证</span>
      <span class="pixel-stars">★★☆</span>
      <span class="pixel-badge">⛏️ 内容矿洞</span>
    </div>
    <h3 class="dungeon-title">{title}</h3>
    <p class="dungeon-desc">{description}</p>
    <div class="dungeon-footer">
      <span class="pixel-drop">🎁 掉落：{timeSaved}</span>
      <span>→</span>
    </div>
  </div>
</div>
```

**耗时：2小时**
**前置：4.1 完成**
**依赖：** 任务0.1的数据补全

---

### 任务 4.3：副本详情页 RPG 元素添加

**文件：** `src/pages/cases/[slug].astro`

在现有页面基础上添加：
1. 「副本信息」速览面板（难度/耗时/掉落/所需秘籍）
2. 「所需秘籍」模块（从 tools 字段自动关联到 /skills/[slug]）
3. 「Boss 提醒」区域（用黄色像素风盒子展示踩坑）
4. 底部CTA：「查看更多副本 →」

**耗时：1.5小时**
**前置：1.2 + 4.2 完成**

---

## 任务五：龙虾秘籍页改版（第二批）

> **目标：把技能页改成秘籍书库风格**
> **预计总耗时：3小时**
> **⚠️ 第一批上线数据OK后再启动**

### 任务 5.1：秘籍总览页改版

**文件：** `src/pages/skills/index.astro`

改动：
- 页头改为 `📜 龙虾秘籍` + 副标题「学会一招，变强一分」
- 技能卡片改为像素风（`.pixel-card`）
- 分类标签改为像素徽章
- 案例引用数改为「被 XX 个副本引用」

**耗时：1.5小时**
**前置：1.2 完成**

---

### 任务 5.2：秘籍详情页改版

**文件：** `src/pages/skills/[slug].astro`

改动：
- 「踩坑提醒」盒子改为黄色像素风样式（标题加 `⚠️ Boss攻略`）
- 「常见搭配」改为「🔗 套装搭配」
- 安装按钮改为像素风按钮
- 关联案例改为「可刷副本」

**耗时：1小时**
**前置：5.1 完成**

---

### 任务 5.3：套装页改版

**文件：** `src/pages/skills/combos.astro`

改动：
- 页头改为 `🎒 龙虾套装` + 副标题「几本秘籍凑一套，威力翻倍」
- 套装卡片加「技能数」展示
- 效果改为「掉落」字段格式

**耗时：30分钟**
**前置：5.2 完成**

---

## 任务六：新手村改版（第二批）

> **目标：把线性教程改成主线任务+支线任务结构**
> **预计总耗时：4小时**
> **⚠️ 第一批上线数据OK后再启动**

### 任务 6.1：新手村首页改版

**文件：** `src/pages/tutorials/index.astro`

```
🌱 新手村
「每个龙虾养成之路的起点」

📋 主线任务（必做，按顺序）
→ 任务 1：孵化你的龙虾（安装 OpenClaw）
→ 任务 2：学第一本秘籍
→ 任务 3：挑战第一个副本
→ 任务 4：配你的第一套装备

📖 进阶修炼（按需跳读）
→ 避坑指南系列（11 章）
```

**耗时：2小时**
**前置：1.2 完成**

---

### 任务 6.2：「主线任务」进度条组件

**文件：** 在 pixel.css 中新增

```css
.pixel-mode .quest-card.completed { border-left: 4px solid #4CAF50; }
.pixel-mode .quest-card.current   { border-left: 4px solid #FFD54F; animation: pixel-blink 1s step-end infinite; }
.pixel-mode .quest-card.locked    { opacity: 0.5; }

@keyframes pixel-blink {
  0%, 100% { border-left-color: #FFD54F; }
  50%      { border-left-color: #FFF8E1; }
}
```

**耗时：1小时**
**前置：6.1 完成**

---

### 任务 6.3：教程详情页添加「任务完成感」

**文件：** `src/pages/tutorials/[slug].astro`

- 加像素风奖励盒子（「🎖️ 任务奖励」）
- 底部导航改为「← 上一个任务 / 下一个任务 →」
- 加章节编号标题像素风样式

**耗时：1小时**
**前置：6.2 完成**

---

## 任务七：龙虾牧场 MVP（第二期，独立排期）

> **目标：实现最简单的本地 Agent 状态看板**
> **预计总耗时：20小时**
> **⚠️ 独立产品模块，不绑定内容站第一期**

### 任务 7.1：牧场页面框架（1天）

**文件：** `src/pages/farm/index.astro`（新建）

- Gateway 地址输入框
- localStorage 存储 Gateway URL
- 轮询 `/api/sessions` 获取 Agent 状态

### 任务 7.2：Agent 状态卡片（2天）

- Agent 名称 + 当前状态（在线/忙碌/离线）
- 像素风动画（CSS，不需要手绘图）
- 最近一条消息预览

### 任务 7.3：命令栏（1天）

- POST 到 Gateway `/api/sessions/:id/send` 发送指令
- 简单的命令历史（localStorage）

---

## 任务八：等级体系（第二期，依赖用户系统）

> **v1中的任务3.5，移到第二期**
> 需要：用户注册/登录 → 记录完成的副本/教程 → 计算等级
> 没有后端支撑做出来就是假的，不做空壳

---

## 执行顺序（修订版）

```
第 1 天（数据 + 样式基础，并行）：
  0.1（数据补全脚本） + 1.1（字体subset） + 1.3（背景）

第 2-3 天（样式 + 导航）：
  1.2 → 1.4（移动端适配） → 2.1 → 2.2 → 2.3

第 4-5 天（首页）：
  3.1 → 3.2 → 3.3 → 3.4

第 6 天（副本页）：
  4.1 → 4.2 → 4.3

────── 第一批上线，观察3天 ──────

第 7-8 天（秘籍+套装，数据OK才启动）：
  5.1 → 5.2 → 5.3

第 9-10 天（新手村）：
  6.1 → 6.2 → 6.3

第 11-12 天（P2技能补充）：
  0.2

────── 第二批上线 ──────

第二期（独立排期）：
  7.1 → 7.2 → 7.3（牧场）
  8（等级体系）
```

---

## 关键约束

| 约束 | 说明 |
|------|------|
| CSS回滚开关 | 所有像素风在 `.pixel-mode` 作用域下，去掉class秒回滚 |
| 不破坏现有功能 | 叠加样式，不删已有逻辑 |
| 字体≤100KB | Zpix 做 subset，只保留网站用字 |
| 移动端优先检查 | 每个任务完成后必须在手机模拟器上验证 |
| 素材临时方案 | 像素图位置用大 emoji 占位，不阻塞进度 |
| SEO不降级 | title/description 同步更新，URL不变 |
| 分批上线 | 首页+副本先上，看数据再铺开 |

---

## 总工时估算（修订版）

| 阶段 | 任务 | 工时 |
|------|------|------|
| 第一批 | 任务0.1 + 1-4 | 25小时 |
| 第二批 | 任务0.2 + 5-6 | 10小时 |
| 第一期合计 | | **35小时**（含buffer约45小时） |
| 第二期 | 牧场 + 等级体系 | 20小时 + 待定 |

---

*执行人：004 | 审核：001 | 等旭确认后立刻开始 Task 0.1 + 1.1*

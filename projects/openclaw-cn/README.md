# OpenClaw 中文站

面向中文用户的 OpenClaw 社区入口，当前聚焦三个核心页面：

- 首页：解释 OpenClaw 能做什么，给出最快上手路径。
- 技能商店：按场景浏览技能，支持一键复制安装命令。
- 教程中心：按入门、进阶、实战三段式整理学习路径。

## 技术栈

- Astro 5
- Tailwind CSS 4
- 静态站点输出

## 本地开发

```bash
npm install
npm run dev
```

## 常用命令

```bash
npm run build
npm run check
npm run preview
```

## 项目结构

```text
src/
├── components/     # Header、Footer、SkillCard 等公共组件
├── data/           # 首页、技能页、教程页共享内容数据
├── layouts/        # BaseLayout
├── pages/          # 路由页面
└── styles/         # 全局主题与响应式样式
```

## 当前实现重点

- 统一了首页、技能页、教程页的视觉语言和内容结构。
- 完成了 PC、平板、手机三端响应式适配。
- 去掉空 `src/content` 目录导致的 Astro 构建 warning。
- 补齐 `astro check` 所需依赖，便于后续持续检查。

## 后续可扩展方向

- 把 `src/data/site-content.ts` 迁移为 Markdown 或内容集合。
- 补充技能详情页、教程详情页和真实案例详情页。
- 接入真实社区入口、二维码和内容更新流程。

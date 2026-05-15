export const SITE_CONFIG = {
  title: 'OpenClaw 中文站',
  description: '国内用户获取 OpenClaw 玩法、教程、技能和应用案例的第一入口',
  lang: 'zh-CN',
  author: '零零壹 × 旭',
  nav: [
    { name: '首页', href: '/' },
    { name: '技能商店', href: '/skills' },
    { name: '教程中心', href: '/tutorials' },
  ],
  social: {
    github: 'https://github.com/openclaw',
    wechat: '社区微信群筹备中',
  },
  skillCategories: [
    {
      name: '内容创作',
      emoji: '📱',
      slug: 'content',
      description: '笔记、脚本、配图和多平台分发',
    },
    {
      name: '办公提效',
      emoji: '💼',
      slug: 'office',
      description: '邮件、日程、文档和会议整理',
    },
    {
      name: '电商运营',
      emoji: '🛒',
      slug: 'ecommerce',
      description: '商品文案、客服、竞品与复盘',
    },
    {
      name: '开发工具',
      emoji: '🔧',
      slug: 'dev',
      description: '代码审查、部署和调试辅助',
    },
    {
      name: '生活助手',
      emoji: '🏠',
      slug: 'life',
      description: '提醒、资讯、日常计划和整理',
    },
    {
      name: '数据分析',
      emoji: '📊',
      slug: 'data',
      description: '报告搜索、趋势分析和结构化输出',
    },
    {
      name: '创意设计',
      emoji: '🎨',
      slug: 'design',
      description: '视觉灵感、品牌草案和演示内容',
    },
  ],
} as const;

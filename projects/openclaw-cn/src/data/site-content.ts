export interface MetricItem {
  value: string;
  label: string;
  description: string;
}

export interface FeaturedResource {
  title: string;
  description: string;
  tag: string;
  meta: string;
  href: string;
}

export interface SkillItem {
  name: string;
  nameEn: string;
  description: string;
  category: string;
  difficulty: 1 | 2 | 3;
  installCommand: string;
  href: string;
  highlights: string[];
}

export interface CaseStudy {
  title: string;
  subtitle: string;
  description: string;
  tag: string;
  metric: string;
  initials: string;
  href: string;
}

export interface TutorialItem {
  title: string;
  description: string;
  duration: string;
  outcome: string;
  href: string;
}

export interface TutorialTrack {
  level: string;
  icon: string;
  title: string;
  description: string;
  audience: string;
  items: TutorialItem[];
}

export const siteMetrics: MetricItem[] = [
  {
    value: '30+',
    label: '种子技能方向',
    description: '覆盖内容创作、电商运营、办公自动化和开发工具。',
  },
  {
    value: '3',
    label: '核心入口页面',
    description: '首页、技能商店、教程中心构成当前 MVP 主链路。',
  },
  {
    value: '5 min',
    label: '建议起步时间',
    description: '先看入门教程，再复制命令，最后跑通第一个场景。',
  },
];

export const featuredResources: FeaturedResource[] = [
  {
    title: '如何用 OpenClaw 自动发小红书',
    description: '从选题、草稿、配图到定时发布，拆成零基础也能照做的四个步骤。',
    tag: '玩法教程',
    meta: '8 分钟读完',
    href: '/tutorials',
  },
  {
    title: '跨境电商客服自动化实战',
    description: '把多语种回复、售后状态追踪和日报汇总收敛到同一套 Agent 流程里。',
    tag: '实战案例',
    meta: '适合卖家团队',
    href: '/skills',
  },
  {
    title: '零基础发布第一个 Claw Skill',
    description: '用最短路径理解技能安装、配置和调试，不再被英文文档卡住。',
    tag: '新手必读',
    meta: '安装路径清晰',
    href: '/tutorials',
  },
];

export const topSkills: SkillItem[] = [
  {
    name: '小红书发布助手',
    nameEn: 'xhs-publisher',
    description: '自动生成标题、正文和封面提示词，再按发布时间表完成分发。',
    category: '内容创作',
    difficulty: 1,
    installCommand: 'clawhub install xhs-publisher',
    href: '/tutorials',
    highlights: ['适合个人 IP', '支持批量草稿', '复制即装'],
  },
  {
    name: '邮件智能助理',
    nameEn: 'email-manager',
    description: '自动分类收件箱、提炼待办重点，并为常见邮件生成回复草案。',
    category: '办公提效',
    difficulty: 1,
    installCommand: 'clawhub install email-manager',
    href: '/tutorials',
    highlights: ['会议纪要联动', '待办自动归档', '适合上班族'],
  },
  {
    name: '多平台商品文案',
    nameEn: 'product-copywriter',
    description: '根据卖点和参数生成淘宝、京东、抖音等平台可直接使用的文案。',
    category: '电商运营',
    difficulty: 2,
    installCommand: 'clawhub install product-copywriter',
    href: '/skills',
    highlights: ['平台化输出', '适合爆品测试', '节省改稿时间'],
  },
  {
    name: '代码审查助手',
    nameEn: 'code-reviewer',
    description: '在提交前检查常见 bug、可维护性问题和接口边界，减少返工。',
    category: '开发工具',
    difficulty: 2,
    installCommand: 'clawhub install code-reviewer',
    href: '/skills',
    highlights: ['适合小团队', '聚焦风险项', '便于 PR 复核'],
  },
  {
    name: '深度研报搜索',
    nameEn: 'deep-researcher',
    description: '抓取行业报告、清洗要点、输出结构化摘要，适合调研和方案对比。',
    category: '数据分析',
    difficulty: 3,
    installCommand: 'clawhub install deep-researcher',
    href: '/tutorials',
    highlights: ['适合市场调研', '支持归纳摘要', '节省检索时间'],
  },
  {
    name: '晨间资讯播报',
    nameEn: 'morning-briefing',
    description: '聚合你关注的科技、产品和行业信息，生成单页简报推送到常用渠道。',
    category: '生活助手',
    difficulty: 1,
    installCommand: 'clawhub install morning-briefing',
    href: '/tutorials',
    highlights: ['每日定时', '单页速读', '适合团队同步'],
  },
  {
    name: '品牌灵感生成器',
    nameEn: 'brand-ideator',
    description: '围绕产品定位生成 slogan、视觉关键词和首页文案，适合冷启动阶段。',
    category: '创意设计',
    difficulty: 2,
    installCommand: 'clawhub install brand-ideator',
    href: '/skills',
    highlights: ['适合新项目', '统一品牌语气', '输出提案更快'],
  },
  {
    name: '竞品监控日报',
    nameEn: 'competitor-tracker',
    description: '自动抓取竞品上新、价格和活动变化，并生成一页可读日报。',
    category: '电商运营',
    difficulty: 2,
    installCommand: 'clawhub install competitor-tracker',
    href: '/skills',
    highlights: ['适合运营复盘', '固定节奏汇总', '输出结构稳定'],
  },
];

export const caseStudies: CaseStudy[] = [
  {
    title: '个人 IP 孵化',
    subtitle: '自媒体创作者把日更流程压缩到 40 分钟内',
    description: '从选题池、草稿、配图到多平台排期，交给同一套工作流接力完成。',
    tag: '自媒体',
    metric: '内容产能提升约 3 倍',
    initials: 'IP',
    href: '/tutorials',
  },
  {
    title: '出海电商自动化',
    subtitle: '独立站卖家把客服和竞品复盘做成日报机制',
    description: '多语言回复、售后状态追踪和竞品价格监控统一在一个面板里查看。',
    tag: '电商',
    metric: '订单处理效率提升约 5 倍',
    initials: 'EC',
    href: '/skills',
  },
  {
    title: '独立开发者工作流',
    subtitle: '全栈开发者用 AI 把评审、监控和发布前检查串起来',
    description: '把日常重复检查前置到提交前，减少上线后的低级回滚和沟通成本。',
    tag: '开发',
    metric: '上线前检查时间下降约 60%',
    initials: 'DEV',
    href: '/tutorials',
  },
];



export const onboardingSteps = [
  {
    title: '先看入门教程',
    description: '把安装和首个任务跑通，不在命令行细节里打转。',
    href: '/tutorials',
  },
  {
    title: '复制一个最接近业务的技能',
    description: '优先选能立刻看到结果的场景，不要一开始就搭复杂工作流。',
    href: '/skills',
  },
  {
    title: '再扩展到定时任务和多 Agent',
    description: '等单点能力稳定后，再做自动化编排和团队协作。',
    href: '/tutorials',
  },
];

export const marketplaceHighlights = [
  '所有技能卡片都保留一键复制命令入口。',
  '分类先按使用场景组织，减少非技术用户的理解成本。',
  '页面优先服务手机访问，再逐步扩展到平板和 PC 阅读体验。',
];

export const tutorialTracks: TutorialTrack[] = [
  {
    level: '入门',
    icon: '🟢',
    title: '从零到能用',
    description: '先搞定安装环境，连上第一个聊天渠道，跑通第一条指令。',
    audience: '适合第一次接触 OpenClaw 的新用户',
    items: [
      {
        title: 'OpenClaw 官方快速开始指南',
        description: '官方权威安装手册，三步完成 Gateway 网关部署与基础配对。',
        duration: '10 分钟',
        outcome: '能成功启动网关并连接第一个聊天渠道（如 WhatsApp/Telegram）',
        href: '/tutorials',
      },
      {
        title: 'Windows 系统一键部署保姆级教程',
        description: '针对 Windows 用户的图形化引导，涵盖 Node.js 环境及一键脚本使用。',
        duration: '15 分钟',
        outcome: '在 Windows 电脑上完成 OpenClaw 的完整初始化与运行环境配置',
        href: '/tutorials',
      },
      {
        title: 'OpenClaw 核心概念与基础命令',
        description: '理清常用斜杠命令用法，搞懂 Gateway、Agent、Skill 的关系。',
        duration: '5 分钟',
        outcome: '能熟练使用 /status、/model 等基础命令管理 AI 助手状态',
        href: '/tutorials',
      },
      {
        title: 'ClawBox 硬件开箱即用指南',
        description: '专为 NVIDIA Jetson 硬件定制的部署手册，实现 100% 本地化且 24/7 在线。',
        duration: '5 分钟',
        outcome: '在不依赖云端 API 的情况下，建立一个完全私有的硬件 AI 助手',
        href: '/tutorials',
      },
    ],
  },
  {
    level: '进阶',
    icon: '🟡',
    title: '从能用到好用',
    description: '配置个性化人格、安装技能、建定时任务，让助手真正融入你的工作流。',
    audience: '适合已经安装完成、想深度定制和提升效率的用户',
    items: [
      {
        title: '7 天掌握 OpenClaw：从安装到定制 Skill',
        description: 'DataWhale 出品的结构化课程，包含工作空间配置与记忆系统深度设置。',
        duration: '1 周',
        outcome: '能通过修改 SOUL.md 和 USER.md 打造具有特定人格的助手',
        href: '/tutorials',
      },
      {
        title: 'Skills 实战：用 ClawHub 扩展助手能力',
        description: '教授如何从 13,000+ 社区技能中筛选并使用 clawhub CLI 进行一键安装。',
        duration: '20 分钟',
        outcome: '能独立安装 Web 搜索、文件处理等 3 个核心业务技能',
        href: '/tutorials',
      },
      {
        title: '自动化工作流：Cron 定时任务与 Heartbeat 配置',
        description: '教授如何让助手 24 小时主动运行，执行定时推送与任务检查。',
        duration: '30 分钟',
        outcome: '能编写第一个定时执行的 AI 日报推送任务',
        href: '/tutorials',
      },
      {
        title: '人格养成：SOUL 与 MEMORY 深度设计',
        description: '深度解析 5 个核心配置文件的协同逻辑，让助手有记忆、有个性、有判断。',
        duration: '30 分钟',
        outcome: '能通过 openclaw doctor 优化 Agent 的底层决策质量',
        href: '/tutorials',
      },
      {
        title: 'n8n 编排：通过 Webhook 实现 Agent 离链操作',
        description: '高阶玩法：让 OpenClaw 调用 n8n 自定义工作流，实现 credential 零暴露。',
        duration: '50 分钟',
        outcome: '能通过 OpenClaw 发送指令触发 n8n 复杂自动化流程',
        href: '/tutorials',
      },
      {
        title: '可靠性运维：生产环境监控与故障排查',
        description: '针对大规模部署的加固教程，包含 API 限流、安全加固及 doctor 深度诊断。',
        duration: '40 分钟',
        outcome: '能建立基本的 Agent 运行监控体系并快速排查 500/403 报错',
        href: '/tutorials',
      },
      {
        title: 'OpenClaw 源码架构深度剖析',
        description: '深入 Gateway 控制平面、通道适配器及路由算法的原理级教程。',
        duration: '120 分钟',
        outcome: '能看懂 OpenClaw 运行链路并解决高级配置层面的连接故障',
        href: '/tutorials',
      },
    ],
  },
  {
    level: '实战',
    icon: '🔴',
    title: '从好用到生产力',
    description: '真实业务场景完整落地，复制即用，不用从零摸索。',
    audience: '适合已经明确场景目标、想直接跑通业务的进阶用户',
    items: [
      {
        title: '超级个体：一个人顶一个团队的 70+ 实战案例',
        description: '涵盖财务报销、内容创作、代码修复等 70 多个开箱即用的工作流。',
        duration: '60 分钟',
        outcome: '能直接复刻一套针对个人自媒体或外包开发的自动化流程',
        href: '/tutorials',
      },
      {
        title: '多 Agent 协作：配置主助理与技术专家',
        description: '教授如何在同一个 Gateway 下配置多个不同模型的 Agent 协同工作。',
        duration: '40 分钟',
        outcome: '能在聊天界面根据任务性质无缝切换多位专业助手',
        href: '/tutorials',
      },
      {
        title: 'YouTube/Reddit 自动简报管家',
        description: '配置专门的采集 Agent 每天汇总最爱的频道与论坛内容并推送到手机。',
        duration: '30 分钟',
        outcome: '能实现每天早晨准时收到一份 AI 过滤后的行业高质量摘要',
        href: '/tutorials',
      },
      {
        title: '远程办公黑科技：一句话找回办公室文件',
        description: '利用 OpenClaw 执行权限跨越内网搜寻特定文件并发送至手机。',
        duration: '20 分钟',
        outcome: '能身在室外通过飞书/Telegram 让家里电脑发送指定文件',
        href: '/tutorials',
      },
      {
        title: 'Coding Agent：AI 自动编写并部署网页',
        description: '演示从代码生成到本地部署再到内网穿透映射公网的全闭环流程。',
        duration: '45 分钟',
        outcome: '能让 AI 独立完成「写代码-建文件夹-本地跑-发公网链接」所有步骤',
        href: '/tutorials',
      },
      {
        title: '24/7 AI 电话客服：OpenClaw 语音网关落地',
        description: '通过 Vapi 或自带语音网关实现电话拨打与自动应答、访客确认。',
        duration: '60 分钟',
        outcome: '能搭建一个能接打电话并自动记录关键信息的 AI 前台',
        href: '/tutorials',
      },
      {
        title: '自愈式家庭服务器：监控、提醒与自修复',
        description: '展示如何让 OpenClaw 作为 SSH 运维官，自动检测 SSL 到期及磁盘报警。',
        duration: '50 分钟',
        outcome: '能建立「监控-汇报-自动执行脚本」的闭环服务器管理工作流',
        href: '/tutorials',
      },
      {
        title: '智能家居：Home Assistant + MQTT 声控中心',
        description: '打通 OpenClaw 与米家/HomeKit，实现自然语言控制全屋家电。',
        duration: '30 分钟',
        outcome: '能实现「睡觉了」一句话联动关闭全屋灯光并设置次日闹钟',
        href: '/tutorials',
      },
      {
        title: '龙虾三万：一个会自我修补的桌面 Cowork 日记',
        description: '记录了一个具身智能 Agent 如何从报错中自愈并主动管理 600+ 人拜年流程。',
        duration: '15 分钟',
        outcome: '学会通过日志分析与自我博弈让 Agent 具备初步的「常识」与「记性」',
        href: '/tutorials',
      },
      {
        title: '一人公司：公众号全自动运营流',
        description: '从选题、写作、图片到定时发布，用 OpenClaw 跑通完整内容工厂。',
        duration: '45 分钟',
        outcome: '能搭出公众号内容生产的全自动流水线',
        href: '/tutorials',
      },
      {
        title: '自动化内容工厂：Discord 多 Agent 协作流',
        description: '展示写手 Agent + 审核 Agent + 发布 Agent 如何在 Discord 频道内流水作业。',
        duration: '50 分钟',
        outcome: '能在 Discord 里部署一套内容生产团队并自动完成发布',
        href: '/tutorials',
      },
      {
        title: '三万养成记：Agent 错误自愈与保密制度设计',
        description: '记录 Agent 如何从报错中自愈，以及如何设置信息隔离保障隐私安全。',
        duration: '20 分钟',
        outcome: '能让 Agent 自动检测异常并执行恢复动作，同时保护敏感数据不泄露',
        href: '/tutorials',
      },
      {
        title: '自建 AI 助手：Claw123 技能导航实操案例',
        description: '以 Claw123 技能站为素材，演示如何快速筛选并落地一个业务场景技能。',
        duration: '25 分钟',
        outcome: '能在 15 分钟内找到并跑通一个适合自己场景的社区技能',
        href: '/tutorials',
      },
    ],
  },
];

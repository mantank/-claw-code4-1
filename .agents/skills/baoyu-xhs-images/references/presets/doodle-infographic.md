---
name: doodle-infographic
category: handdrawn
---

# Doodle Infographic Style（手绘涂鸦信息图）

Sketchnote-style hand-drawn infographic with warm paper texture, ink outlines, and soft Morandi color fills. Visual notes aesthetic meets data visualization.

## Element Combination

```yaml
canvas:
  ratio: portrait-3-4
  grid: single | freeform

image_effects:
  cutout: hand-drawn-outline
  stroke: ink-outline
  filter: warm-paper | paper-texture

typography:
  decorated: handwritten-bold
  tags: round-rect | ribbon-banner
  direction: horizontal
  chinese_limit: 50_chars_total | 12_title | 6_per_node
  bilingual: chinese-above-english-below

decorations:
  emphasis: hand-drawn-star | radiant-lines | circle-mark
  background: white-paper | dotted-grid | notebook-texture
  doodles: arrows-curvy | small-stars | dot-dash-lines | laurel-branch
  frames: ink-border | watercolor-edge
```

## Color Palette（莫兰迪色系）

| Role | Colors | Hex |
|------|--------|-----|
| AI / Brain / Smart | Soft yellow | #FFF3CD / #F5DEB3 |
| Core / Gateway | Mint green | #D4EDDA |
| Storage / Memory | Soft blue | #D6E6F2 |
| Communication | Soft orange | #F9DCC4 |
| Tools / Execution | Soft pink / coral | #F4C2C2 |
| Device / Terminal | Soft purple | #E8D5F5 |
| Auxiliary | Gray-blue | #E8ECF1 |
| Ink lines / Borders | Black / dark brown | #1A1A1A / #3D2B1F |
| Background | White / off-white | #FFFFFF / #FAFAF5 |

## Visual Elements

- All outlines hand-drawn ink style with natural line weight variation
- Color fill: colored pencil / light watercolor strokes — do NOT fill completely, leave breathing room and visible pencil stroke direction
- Cards: round-rect with ink border + Morandi pastel fill
- Icons: hand-drawn doodle style (bulb, gear, rocket, cloud, brain, folder, speech-bubble, wrench, etc.)
- Connections: hand-drawn curved arrows, bidirectional (←→) or one-way (→)
- Decorations: 4-point stars (✦), radiant lines, dot-dash lines, small clouds, laurel branches
- Paper feel: real paper texture warmth, notebook-like handmade quality

## Typography

- Titles: large bold handwritten font, black or deep Morandi color (coral/blue)
- Key numbers: large bold dark or gold handwritten
- Node labels: bilingual format "中文名/(English)" — Chinese on top, English in parentheses
- Total Chinese: ≤50 chars per image | Title: ≤12 chars | Each node/card: ≤6 chars
- Prefer icons + English numbers over dense Chinese text (more reliable rendering)

## Page Type Templates

### 数据概览页 (Data Overview)
Top bold title banner → multiple Morandi color cards (icon + label + big number) → doodle decorations scattered around.
Best for: product data, revenue analysis, monthly summaries.

### 概念解释页 (Concept Explanation)
Large colored title → central hand-drawn object → radiating arrows to surrounding explanation cards.
Best for: product concepts, business models, feature introductions.

### 流程辐射页 (Flow Radiation)
Title → central node (cloud/server/gear) → curved arrows radiating to 4-6 modules.
Best for: one-click deployment, platform capabilities, ecosystem overview.

### 架构拓扑图 (Architecture Topology)
Title → 5-7 colored circular nodes interconnected with bidirectional arrows. Color semantics: yellow=AI brain, green=gateway, blue=storage, orange=sessions, pink=tools, purple=devices.
Best for: system architecture, AI agent structure, platform components.

### 金字塔分层页 (Pyramid Tiers)
Banner title → hand-drawn pyramid (4-5 tiers, each different Morandi color) → icons flanking each tier.
Best for: revenue tiers, user tiers, product pricing ladder.

### 排行榜页 (Leaderboard)
Title with laurel decoration → hand-drawn table (5 rows, alternating Morandi fill) → icons in each row.
Best for: product rankings, TOP lists, performance charts.

### 对比分析页 (Comparison)
Title → left/right split with VS divider → different color sets per side → 3-4 data points each.
Best for: A/B comparison, before/after, competitive analysis.

## Chinese Text Rendering Rules（中文渲染铁律）

1. All Chinese must be correct, legible simplified Chinese — NO garbled text, NO Japanese kana, NO distorted characters
2. Strict character limits (see Typography above)
3. Use English/numbers for amounts ($), percentages (%), brand names, abbreviations (SaaS, MRR, API, etc.)
4. Bilingual labels: "网关/(Gateway)" format — most reliable approach
5. When in doubt: use icons + numbers, add minimal Chinese only for titles
6. If Chinese renders incorrectly: generate full-English layout first, then replace titles with Chinese

## Best Layout Pairings

| Layout | Compatibility | Use Case |
|--------|---------------|----------|
| sparse | ✓✓ | Concept covers, key stat highlights |
| balanced | ✓✓ | Standard content cards |
| dense | ✓✓ | Data overview, architecture diagrams |
| list | ✓✓ | Rankings, feature lists, step-by-step |
| comparison | ✓✓ | Before/after, A vs B |
| flow | ✓✓ | Process flows, deployment steps |
| mindmap | ✓✓ | Architecture topology, radial structure |
| quadrant | ✓ | Four-quadrant analysis |

## Best For

- OpenClaw / AI tool concept explanations
- System architecture diagrams
- Data reports and product overviews
- Knowledge-sharing content for developers
- Tutorial infographics with warm, approachable aesthetic
- Any content benefiting from "hand-crafted notebook" visual feel

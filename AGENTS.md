# Agent 指令（Codex / Cursor / 其他 AI Agent 入口）

本仓库是一个**八字命理深度分析技能包**。如果你是在本目录下启动的 AI Agent（Codex CLI、Cursor 等），请按以下规则工作：

## 核心指令

1. **完整阅读并严格遵循 [`SKILL.md`](SKILL.md)** —— 它是本技能的全部工作流程定义（信息收集 → 精确排盘 → 19章分析 → 合婚 → 部署分享）。
2. 当用户提到「算八字 / 排盘 / 看命盘 / 合婚 / 批八字」等任何命理请求时，立即按 SKILL.md 的五个阶段执行。

## 关键纪律（不可违反）

- **排盘必须运行 `scripts/paipan.py`**，禁止心算干支。脚本就在本仓库内：
  ```bash
  python3 scripts/paipan.py <公历年> <月> <日> <时0-23> <m/f>
  ```
- **农历输入必须先转公历**（需要 `pip3 install lunardate`，见 SKILL.md 第一阶段）。
- **每个关键判断必须标注经典出处**（九部典籍摘要在 `references/classical-texts.md`）。
- **生成 HTML 报告前必须先读 `templates/report-example.html`**，沿用其结构与样式。

## Codex CLI 用户注意

- Codex 默认沙箱可能**禁止网络访问**。以下步骤需要联网，请在需要时批准网络权限（或以允许网络的模式运行）：
  - `pip3 install lunardate`（仅农历输入需要，装一次即可）
  - 节气边界日（出生日在节气日 ±2 天内）查询当年真实节气时刻
  - Cloudflare 隧道分享报告（可选功能）
- 本文件中的路径均相对于仓库根目录。请在仓库根目录下工作，或使用绝对路径调用脚本。

## 文件地图

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 完整工作流程（主指令，必读） |
| `scripts/paipan.py` | 排盘计算器（必须用它排盘） |
| `references/` | 五行/十神/时辰/大运规则 + 九部经典论命摘要 |
| `templates/report-example.html` | 19章报告样例（生成报告的结构基准） |
| `USAGE.md` / `usage-guide.pdf` | 面向最终用户的操作指南 |

# bazi-master-skill

Claude Code 八字命理深度分析 Skill。

## 核心能力

1. **精确排盘** — 使用 `scripts/paipan.py` 代码计算四柱，非 LLM 推算（已验证 1949-10-01 = 甲子日）
2. **19章深度报告** — 含调候用神（穷通宝典）、经典引用（9部典籍）、历史校准（千里命稿）
3. **精美 HTML 可视化** — 单文件自包含，移动端适配，支持打印
4. **合婚配对** — 五维雷达评分，调候互补分析
5. **一键部署分享** — Cloudflare 隧道生成微信可直接打开的链接

## 目录结构

```
bazi-master-skill/
├── SKILL.md                    # Skill 入口（Claude Code 自动识别）
├── USAGE.md                    # 详细使用操作指南
├── scripts/
│   └── paipan.py               # 精确排盘计算器
├── references/
│   ├── classical-texts.md      # 九本经典核心论命规则
│   ├── dayun-rules.md          # 大运排法
│   ├── shichen-table.md        # 时辰对照表
│   └── wuxing-tables.md        # 五行/天干地支/十神参考表
└── templates/
    ├── report-example.html     # 完整19章报告样例
    └── report-style.css        # HTML 报告组件清单
```

## 安装与使用

**详细操作指南见 [USAGE.md](USAGE.md)**（安装步骤、使用流程、FAQ、已知精度限制）。

快速安装：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/secret04725-coder/bazi-master-skill.git ~/.claude/skills/bazi-master
pip3 install lunardate   # 农历转换依赖
```

之后在 Claude Code 对话中说"算八字"即可触发。

### 排盘示例

```bash
python3 scripts/paipan.py 2002 8 2 10 f
# 输出：壬午年 丁未月 壬寅日 乙巳时
python3 scripts/paipan.py 1999 3 30 - m   # 时辰未知用 - 占位
```

## 与其他八字 Skill 的区别

| 特性 | 本 Skill | 纯 LLM Skill |
|------|----------|--------------|
| 排盘方式 | Python 代码计算 | LLM 推算（易出错） |
| 输出格式 | 精美 HTML 页面 | 纯文本 |
| 调候用神 | 穷通宝典逐月查表 | 可能遗漏 |
| 经典引用 | 每章标注出处 | 无 |
| 历史校准 | 推导已发生事件验证 | 无 |
| 分享部署 | Cloudflare 隧道一键分享 | 不支持 |

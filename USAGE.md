# bazi-master 使用操作指南

> 面向第一次拿到这个 Skill 的人。照着做即可，全程不需要懂代码。

---

## 一、这是什么

一个 Claude Code 的八字命理分析 Skill。装好之后，你在 Claude Code 对话框里说一句"帮我算八字"，它会：

1. 收集你的出生信息（自动处理农历转换、真太阳时校正）
2. 用 Python 脚本精确排盘（不是 AI 猜的，是代码算的）
3. 生成一份 19 章的深度分析 HTML 报告（手机可看、可打印、可分享）
4. 可选：两人合婚配对、一键生成微信可打开的分享链接

---

## 二、安装（5分钟）

### 前提条件

| 需要 | 说明 |
|------|------|
| Claude Code | 已安装并能正常对话（`npm install -g @anthropic-ai/claude-code`） |
| Python 3 | macOS 自带；Windows 到 python.org 安装，勾选 "Add to PATH" |
| git | 用于克隆本仓库（也可以直接下载 zip 解压） |

### 安装步骤

**第 1 步：把 Skill 放到 Claude Code 的 skills 目录**

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
git clone https://github.com/secret04725-coder/bazi-master-skill.git ~/.claude/skills/bazi-master
```

```powershell
# Windows (PowerShell)
mkdir -Force "$env:USERPROFILE\.claude\skills"
git clone https://github.com/secret04725-coder/bazi-master-skill.git "$env:USERPROFILE\.claude\skills\bazi-master"
```

> 注意：目录名用 `bazi-master`（与 SKILL.md 里的 name 一致），不要用仓库原名 `bazi-master-skill`。
>
> 不会用 git？直接在 GitHub 页面点 Code → Download ZIP，解压后把整个文件夹改名为 `bazi-master`，放进 `~/.claude/skills/` 即可。

**第 2 步：安装农历转换库（处理农历生日必需）**

```bash
pip3 install lunardate
```

**第 3 步：验证安装**

新开一个 Claude Code 会话，输入：

```
帮我排个八字：2002年8月2日上午10点，女
```

如果 Claude 调用了 `paipan.py` 并返回 `壬午年 丁未月 壬寅日 乙巳时`，说明安装成功。

---

## 三、日常使用

### 3.1 触发方式

对话中说任意一句即可：
- "算八字" / "排八字" / "看八字" / "批八字"
- "帮我看看命盘" / "命理分析"
- "合婚" / "我俩匹配度怎么样"

### 3.2 你需要准备的信息

| 信息 | 必须 | 备注 |
|------|------|------|
| 出生日期 | ✅ | **说清楚是公历还是农历**，农历会自动转换 |
| 出生时间 | 推荐 | 精确到分钟最好；不知道就说"时辰未知"（报告会少时柱相关内容） |
| 性别 | ✅ | 影响大运排法 |
| 出生地（省市） | 推荐 | 用于真太阳时校正，边界时辰会影响时柱 |

### 3.3 标准流程示例

```
你：帮我算八字。农历2001年十月二十五早上7点，男，汕尾出生。

Claude 会依次：
1. 农历 → 公历（2001-12-09）并和你确认
2. 真太阳时校正（汕尾7:00 → 真太阳时6:42，提示你这是卯/辰边界，
   请确认出生时间精度）
3. 运行排盘脚本，给出四柱、十神、藏干、纳音、大运
4. 问你是否需要完整19章HTML报告
5. 生成报告并在浏览器打开
```

### 3.4 报告里有什么

19 章：排盘总览 → 调候用神（穷通宝典） → 天干/地支/藏干 → 十二长生 → 神煞 → 五行用神 → 十神性格 → 六亲 → 财运 → 事业 → 感情 → 健康 → 大运 → 流年逐月 → 未来9年 → 转运建议 → 命盘叙事 → **历史校准**。

**第19章"历史校准"是本 Skill 的特色**：报告会推测 3-5 件你过去已经发生的事，你对照实际经历反馈准确度。3/5 以上准确说明排盘和用神判断正确；偏差大则可能时辰有误，需要重排。

### 3.5 合婚配对

把两个人的出生信息一起给出：

```
你：帮我看看这两人的匹配度：
男：2001年12月9日（公历）早上7点，汕尾
女：2002年8月2日（公历）上午10点，哈尔滨
```

输出五维评分（日主配对/五行互补/地支关系/十神互看/大运同步）+ 综合分。

### 3.6 分享报告给朋友

```
你：把这份报告生成一个微信能打开的链接
```

Claude 会启动本地服务 + Cloudflare 隧道，生成 `https://xxx.trycloudflare.com` 临时链接。
**注意**：链接在你关闭终端后失效。长期分享需部署到 GitHub Pages 或其他静态托管。

---

## 四、已知精度限制（重要，请阅读）

本 Skill 的排盘脚本有两个近似，Claude 会按 SKILL.md 的指引自动修正，但你应该知道：

| 限制 | 影响 | Claude 的处理方式 |
|------|------|------------------|
| 节气用固定近似日期 | 出生日在节气日 ±2 天内，月柱/年柱可能偏差 | 自动联网查询该年真实节气时刻确认 |
| 起运年龄默认 9 岁 | 大运干支序列准确，年龄区间可能偏移 | 按节气天数÷3规则重新计算修正 |
| 真太阳时 | 出生时间在时辰边界 ±30 分钟内，时柱可能差一位 | 按经度校正并和你确认，必要时出两版对照 |

如果你发现报告与实际经历严重不符，优先怀疑：① 时辰记错/边界 ② 农历公历搞混 ③ 节气边界日。

---

## 五、常见问题（FAQ）

**Q1：报错 `ModuleNotFoundError: No module named 'lunardate'`**
A：运行 `pip3 install lunardate`。只在输入农历生日时需要。

**Q2：Claude 没有自动触发这个 Skill**
A：检查目录是否为 `~/.claude/skills/bazi-master/SKILL.md`（注意层级，SKILL.md 必须直接在 bazi-master 目录下）。重启 Claude Code 会话再试。

**Q3：生成的报告样式和示例不一样**
A：提醒 Claude："参考 templates/report-example.html 的结构和样式生成"。

**Q4：23点后出生算哪一天？**
A：本 Skill 采用"夜子时"规则——23点后按次日日柱排。脚本自动处理并会提示。

**Q5：不知道出生时间怎么办？**
A：照常分析，但时柱、部分大运细节、子女宫分析会缺失。可以用第19章历史校准反推时辰（报错最少的版本大概率是真实时辰）。

**Q6：Windows 上 cloudflared 怎么装？**
A：`winget install Cloudflare.cloudflared`，然后 `cloudflared tunnel --url http://localhost:8234`。

**Q7：报告内容可信吗？**
A：排盘部分是确定性计算，可验证。分析部分基于《穷通宝典》《滴天髓》等经典规则推演，属传统文化参考体系，不构成任何决策依据。健康相关请以医学诊断为准。

---

## 六、目录结构速查

```
bazi-master/
├── SKILL.md                    # Skill 入口，Claude 的工作指令
├── USAGE.md                    # 本文档
├── README.md                   # 项目简介
├── scripts/
│   └── paipan.py               # 排盘计算器（可独立命令行使用）
├── references/
│   ├── classical-texts.md      # 九本经典论命规则摘要
│   ├── dayun-rules.md          # 大运顺逆与起运年龄规则
│   ├── shichen-table.md        # 时辰对照、五鼠遁元
│   └── wuxing-tables.md        # 五行/十神/藏干/十二长生表
└── templates/
    ├── report-example.html     # 完整19章报告样例（生成报告的结构基准）
    └── report-style.css        # CSS 组件清单
```

### 脚本独立使用（不经过 Claude）

```bash
python3 scripts/paipan.py 2002 8 2 10 f    # 年 月 日 时 性别
python3 scripts/paipan.py 1999 3 30 - m    # 时辰未知用 - 占位
```

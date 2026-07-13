# Humanizer-zh-next

> **声明：**
> - 本项目继承并参考了 [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh) 的中文语境、安装说明和早期 Skill 形态。
> - 本项目吸收了 [blader/humanizer](https://github.com/blader/humanizer) `2.8.2` 的规则结构、维护思路和最新检测模式。
> - 本项目吸收了 [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) 中适合中文语境的结构套路、快速检查和质量自检思路。
> - 本项目参考了 Wikipedia 的 [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 与 [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) 相关资料。


---

## 项目简介
Humanizer-zh-next 是 中文 AI 写作去痕 Skill。用于编辑、审阅和改写中文文本，帮助你将 AI 生成的内容改写得更自然、更像人类书写的文本。

本项目以 `op7418/humanizer-zh` 为基础，吸收 `blader/humanizer` 英文版持续更新的规则。考虑到 `blader/humanizer` 一直在更新，但是中文版本 `op7418/humanizer-zh` 缺乏长期维护，因此单独建立该仓库，用于长期维护 Humanizer 的中文版本。如果你认为该 Skill 有任何值得优化的地方或者不足之处，欢迎提出 issue 或 pull request，希望该 Skill 能够得到长期的维护以提供更好的用户体验。

## 安装

### 让 AI 帮你安装

把下面这段话发给你正在使用的 AI 编程助手：

```text
请帮我安装 humanizer-zh-next Skill。

仓库地址是：https://github.com/Hyacehila/humanizer-zh-next

请根据当前 Agent 或编辑器的 Skill 目录规则安装它。如果支持 skills CLI，请优先运行：

npx skills add https://github.com/Hyacehila/humanizer-zh-next

如果不支持，请把仓库中的 SKILL.md 安装到当前环境可识别的 skills 目录，并确认 Skill 名称是 humanizer-zh-next。
```

### Skills CLI 一键安装

```bash
npx skills add https://github.com/Hyacehila/humanizer-zh-next
```

这是最简单的安装方式，会自动把 Skill 安装到当前工具支持的位置。

### Git 克隆

不同 Agent 的 skills 目录可能不同，请把下面的 `<SKILLS_DIR>` 替换为你的实际目录。

```bash
git clone https://github.com/Hyacehila/humanizer-zh-next <SKILLS_DIR>/humanizer-zh-next
```

示例：

```bash
git clone https://github.com/Hyacehila/humanizer-zh-next ~/.codex/skills/humanizer-zh-next
```

### 手动安装

1. 下载本仓库。
2. 找到 `SKILL.md`。
3. 将 `SKILL.md` 放入你的 Agent 支持的 skills 目录。
4. 确认 Skill 元数据可以被读取，名称为 `humanizer-zh-next`。

## 使用

### 常规用法

安装后，可以这样调用：

```text
请用 humanizer-zh-next 帮我改写下面这段文案，降低 AI 腔，但保留事实和语气：

……
```

也可以用于审阅：

```text
请用 humanizer-zh-next 检查下面这段 README，指出最明显的 AI 写作痕迹，并给出自然版本：

……
```

### 语气校准

如果你希望它贴近自己的写法，可以先提供一段写作样本：

```text
下面是我平时的写作样本，请先学习语气，再改写目标文本。

写作样本：
……

目标文本：
……
```

humanizer-zh-next 会尽量保留你的句子长短、正式程度、节奏、用词偏好和表达习惯，而不是套用统一的“自然中文”模板。

## 概述

humanizer-zh-next 检测并修复 33 类常见 AI 写作模式，覆盖内容、语言、风格、交流痕迹、填充词和回避表达。

它尤其关注中文语境中的问题：

- “赋能、生态、闭环、抓手、底层逻辑、价值沉淀”等中文 AI/营销高频词。
- “让我们深入探讨”“下面我们来拆解”“值得注意的是”等导览式开场和填充短语。
- “真正的问题是”“归根结底”“核心在于”等权威姿态和伪洞察话术。
- “未来可期”“广阔前景”“机遇与挑战并存”等通用积极结论。
- 技术文档和 README 中常见的 diff 叙述，例如“新增了……用于替代旧方案”。

AI 腔通常不是单个词造成的，而是多个模式叠加后的效果：抽象名词太多、判断太满、来源太虚、结构太整齐、结尾太积极、语气太像助手。

所以本 Skill 不会把正式、学术、专业、语法干净本身当作 AI 痕迹。它会优先修复那些让文本变得空泛、虚高、模板化或不像当前作者的地方。

除了模式词表，本 Skill 还吸收了英文版的几条方法论：**改写而非删除、等量覆盖**（原文有五段，改写也有五段，不靠压缩去痕）；**初稿 → 自检“是什么让它一眼像 AI” → 终稿**的工作流；以及**个性与灵魂的适用范围护栏**（只对博客、随笔、观点类加个性，技术和参考类文本中性平实就是正确的人类声音）。

## 参考文献

- [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh) commit `91f3d39`，中文语境和早期中文 Skill 基线。
- [blader/humanizer](https://github.com/blader/humanizer) version `2.8.2`，英文规则和 README 结构基线。
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)，结构套路、虚假行动者、快速检查和质量自检参考。
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Wikipedia: WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)

## 版本历史

- `1.1.0`：进一步对齐 `blader/humanizer` `2.8.2` 的方法论与文件结构。吸收“改写而非删除 / 等量覆盖”原则、“初稿→自检→终稿”工作流、“个性与灵魂”的适用范围护栏；把完整示例重构为完整循环；强化 #14 破折号规则（强化但不归零，尊重中文标点习惯）；补充尾部否定示例、人类写作迹象清单和“信号成簇才是自白”的判断收束。同时按英文原版重排章节：Your Task 收敛为 4 条，合并“检测指南”（误判保护 + 人类迹象）与“处理流程与输出”，移除英文版没有的“核心规则速查”，把质量自检表折叠进处理流程。全面扩写 33 类模式：补全每条的触发词清单、加深“问题”诊断（解释 LLM 为什么这么写），并为大多数模式补上 `op7418/Humanizer-zh` 与 `blader/humanizer` 的百科式案例中译，与本地化中文例子形成双例；语言特定的 #17/#19/#26 保留单例并说明中文对应表现。补齐“检测指南”一节：对齐英文 DETECTION GUIDANCE 的全部条目（新增语域混用、书信体、无来源主张、学术词汇细分、年代感引用、可辩护的编辑选择、ChatGPT 发布前文本等），并把光秃清单升级为“要点 + 解释”的阐述式。把“完整示例”补成与英文原版等长的里斯本随笔（六段原文 → 六段终稿），完整演示 原文→初稿→自检→终稿→改动说明 的循环。
- `1.0.0`：参考 `blader/humanizer` `2.8.2` 和 `op7418/humanizer-zh` commit `91f3d39` 为基线发布。吸收英文版 33 类模式，并按中文写作习惯重写触发词、示例、误判保护和输出流程。同时吸收 `stop-slop` 中适合中文语境的结构套路、虚假行动者和质量自检思路。

## 许可

MIT

# Humanizer-zh-next

编辑已有中文文本中的空话、重复和模板化表达，保留原意、事实、确定程度和作者声音。通用模式、中文表达、体裁判断、原有的作者样本方法和文件保护都集中在主 [SKILL.md](SKILL.md)，商务营销、学术写作和基金提案分别按需加载三个专用分支。

当前版本为 **2.0.0**，版本日期为 **2026-10-07**。本次承接原项目的完整通用模式和 1.3.0 的学术能力，更新语义保真规则，并选择性整合中文适配与商务审阅的新来源。结构于 2026-10-06 调整，上游审阅日期为 2026-10-03。

这是一份由 Agent 读取执行的编辑技能，无独立模型或在线运行服务。辅助检查脚本使用 Python 3.10+ 标准库；普通文本编辑不依赖 Python。它不判断作者身份，也不承诺通过检测器或移除水印。

## 本次调整

- 普通编辑不再补造个人经历、情绪和细节；所有教学示例的改写只使用示例原文的信息。
- 保留独立信息和语义关系，允许合理拆合段落，取消段落数量、标点和列举配额。
- 主 `SKILL.md` 保留旧版 33 类模式，补充回复上下文和段落重复两类规则；35 类模式均有中文示例与适用边界。
- 中文句法、弱动词、无主句、连接词、作者声音、体裁、文件保护与完整示例一并放在主文件，不拆成额外 reference。
- 保留学术模式，分离基金申请的目标、方法、前期基础与可行性检查。
- 文件模式保护代码、公式、数据、链接、标题和步骤关系，并提供只读结构检查。
- 提供固定提交的上游记录、包检查和行为评测材料；取消质量自评分阈值。

## 安装

在支持 Agent Skills 的环境中运行：

```bash
npx skills add https://github.com/Hyacehila/humanizer-zh-next
```

仓库安装命令取得远端当前版本，并保留完整技能目录。

也可以克隆远端后，按目标环境的技能目录要求放置：

```bash
git clone https://github.com/Hyacehila/humanizer-zh-next <SKILLS_DIR>/humanizer-zh-next
```

安装时保留主文件、完整的三个 `references/`、`LICENSE` 和 `THIRD_PARTY_NOTICES.md`；只复制主文件会丢失体裁分支。`docs/` 保存来源记录，`scripts/` 和 `tests/` 提供验证材料，不是普通编辑运行的必需依赖。维护者应保留完整目录。

本次升级没有自动修改其他已安装副本。技能目录的名称应为 `humanizer-zh-next`，与元数据 `name` 一致；源码仓库可以使用其他本地目录名。

## 使用

普通润色默认只返回终稿：

```text
请用 humanizer-zh-next 润色这段中文。减少空话和重复，保留原意、全部信息和语气：
……
```

可以指定轻度调整、标准去 AI 腔或深入重写；没有要求时，不自动扩大成摘要、事实核查或补充论据。

作者样本只用于匹配声音：

```text
参考下面的写作样本，润色目标文本。不要把样本的经历和立场移入目标稿。
写作样本：……
目标文本：……
```

文件任务区分审阅与写回：

```text
审阅 docs/intro.md，指出表达问题，暂时不要修改文件。
```

```text
润色 docs/intro.md 并写回。保护代码、链接、标题和数据，不提交。
```

学术文本按对应模式处理：

```text
润色这段论文摘要，保留全部数字、公式、引用、限定和主张。
```

```text
审阅这段基金申请的论证，检查问题、目标、方法与前期基础的关系。不要补写数据和经历，缺少的依据列在正文之外。
```

主张校准或外部核查需要任务明确要求；普通润色不会把作者的判断静默改弱或改强。

## 主文件与三个 reference

普通文本直接使用主文件的完整规则，不需要额外加载通用模式或中文表达文档。`references/` 目录只有以下三个专用文件：

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 公共约束、35 类通用模式、中文表达、体裁矩阵、作者声音、文件保护、流程与完整示例 |
| [commercial-editing.md](references/commercial-editing.md) | 商务与营销文案的分维度审阅 |
| [academic-writing.md](references/academic-writing.md) | 数字引用、学术语体、证据与审稿回复 |
| [grant-proposals.md](references/grant-proposals.md) | 研究计划、基金模板和目标与可行性 |

商务文案的分维度审阅独立保存；学术与基金分支分别处理研究结果和拟开展工作。基金材料涉及既有研究结果时，可同时读取学术分支。

维护材料放在运行 reference 目录之外：

| 文件或目录 | 用途 |
| --- | --- |
| [docs/upstream-sources.md](docs/upstream-sources.md) | 来源相关性、固定提交和采纳取舍 |
| [docs/upstreams.json](docs/upstreams.json) | 可检查的上游版本、目标文件与分支记录 |
| [scripts/validate_package.py](scripts/validate_package.py) | 离线检查元数据、链接、三分支结构与来源归属 |
| [scripts/check_structure.py](scripts/check_structure.py) | 只读比较 Markdown 的受保护内容 |
| [tests/README.md](tests/README.md) | 结构检查和语义行为案例的执行方法 |

普通编辑任务无需读取维护记录或所有来源。

## 上游与新的参考项目

原有四项来源继续保留，采用版本详见 [上游整合记录](docs/upstream-sources.md)：

- [blader/humanizer](https://github.com/blader/humanizer)：通用基线更新至 3.1.0。
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)：采用 2026-09-23 的语义保真与中文修订。
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)：保留适合中文的编辑思路，采用提交未变。
- [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)：承接 1.3.0 的 0.3.3 学术基线，采用提交未变。

本次新增两项来源：

- [jiji262/humanizer-chinese](https://github.com/jiji262/humanizer-chinese)：选择性引用中文句式、弱动词、无主句、语域和防假口语，全部融入主文件，不创建独立 reference。
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)：选择性适配 copy-editing 的分维度审阅。

没有把这些项目的规则全部叠加：模型指纹、检测准确率、统一禁词、固定句式配额、无依据的数字和承诺不纳入本项目。已审阅但没有新增价值的候选保留在整合记录中，便于之后复查。

## 验证

维护者在仓库根目录运行：

```bash
python scripts/validate_package.py
python -B -m unittest discover -s tests -p "test_*.py"
```

Markdown 文件的原稿与改稿可作只读结构检查：

```bash
python scripts/check_structure.py original.md edited.md
```

语义与声音需要实际执行 [行为案例](tests/behavior-cases.json) 并人工核对，方法见 [评测说明](tests/README.md)。结构检查、字数下降和单次样例通过均不代表稳定的编辑质量或检测能力。

## 版本历史

- **2.0.0（2026-10-07）**：完整通用模式与中文表达集中在主文件，只保留商务营销、学术写作、基金提案三个 reference；以英文 3.1.0 和中文 2026-09-23 修订更新规则，新增中文适配与商务审阅两项来源；收紧事实、主张和文件保护，将来源记录移至 docs，增加可执行检查。
- **1.3.0**：增加按需加载的中文学术写作 reference，覆盖论文、学位论文、审稿回复和中国基金申请；加入论断与证据、目标与可行性检查，保护数字、公式、结果和引用。
- **1.2.0**：增加体裁决策矩阵和事实新增边界；个人叙事新增内容逐项提示核实，专业体裁禁止补写事实；新增第三方版权声明并修正完整目录安装方式。2.0.0 进一步取消普通个人叙事补写细节的例外。
- **1.1.0**：对齐英文 2.8.2 的 33 类模式、声音护栏、误判保护和改写循环，扩写中文及百科式示例。
- **1.0.0**：以英文 2.8.2 和中文 `91f3d39` 为基线，适配中文规则并吸收 stop-slop 的结构检查思路。

## 许可

MIT，见 [LICENSE](LICENSE)。采用的固定版本、原始版权和许可文本见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

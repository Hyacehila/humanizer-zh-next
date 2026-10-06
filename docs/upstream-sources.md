# 上游整合记录

维护记录，普通润色无需加载。上游审阅日期为 2026-10-03，结构修订日期为 2026-10-06；精确提交、采用路径和目标文件见 [upstreams.json](upstreams.json)，第三方版权见 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)。来源是规则和方法参考，不是需要在线调用的运行依赖。

## 本次升级基线

升级开发最初基于本地 1.2.0（`cf08ea33910a094f6738cec01ed9c6fc19acc2f9`），并吸收远端 1.3.0（`10795c2964cec5d1f4bc4c7830b51adaa5eca33c`）的中文学术模式。2.0.0 保留这一能力，拆出基金提案分支，并重构通用编辑契约。版本提交承接 1.3.0 的历史；`upstreams.json` 中的基线字段记录研究开发起点，不表示发布后的 HEAD。

通用模式、中文句式、原项目的样本匹配方法、体裁判断和文件保护均集中在主 `SKILL.md`。35 类通用模式保留中文示例与适用边界；`references/` 只包含商务营销、学术写作和基金提案三个分支。来源记录移至 `docs/`，不作为第四个编辑分支。

## 已整合来源

| 项目与固定提交 | 相关性与采纳范围 | 适配后的边界 |
| --- | --- | --- |
| [blader/humanizer 3.1.0](https://github.com/blader/humanizer/tree/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8) | 信息优先、禁止编造、假想反对意见、回复上下文、文件保护 | 保留中文语法和用户声音；普通粘贴默认终稿；不照搬强信号判定 |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh/tree/f4518a8eab97b8bfebc66a89d34320a89bef6930) | 2026-09-23 修订：事实与限定、中文反例、归因、结构核对与行为用例 | 原文主张与风格调整分开；结构通过不能替代语义核对 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/tree/8da1f030185bdfe8471220585162991eaeb970e9) | 抽象行动者、无信息铺垫和收尾检查；当前采用提交仍为 HEAD | 不禁止全部副词、被动句或破折号；不规定两项优于三项 |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer/tree/94b88b23703bed7df507acae7d6d5876209a0cdf) | 0.3.3：学术声音、数字引用、论断与证据、提案可行性；当前提交未变 | 保留 1.3.0 中文适配；实质主张调整按用户范围进行；年度模板按任务核对 |
| [jiji262/humanizer-chinese](https://github.com/jiji262/humanizer-chinese/tree/1d6c08e10fbfe0e1b36ac784834451c6aae0a92c) | 新来源：中文无主句、欧化句法、弱动词和防过度纠偏，直接融入主 SKILL.md | 不创建独立 reference；未采用模型指纹、检测准确率、词频配额和补造细节的示例 |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills/tree/26f7342b26670e5581b48cd64e9dba3eb8a0c3aa/skills/copy-editing) | 新来源：copy-editing 2.1.0 的分维度审阅、利益与证据检查 | 只处理已有商务文案；不自动补指标、担保、品牌故事和紧迫感 |

## 已审阅但未整合

- [RobinZorro86/humanizer-zh-plus](https://github.com/RobinZorro86/humanizer-zh-plus/tree/f450953d241cb40c7bcc9ccc9b82a56ffa21a088)：提供中文模式库和调用模式，但与本次基线高度重叠；部分无条件适用于所有输出的要求和重复入口不适合合并。
- [richyuh/claude-skills](https://github.com/richyuh/claude-skills/tree/77b048bd8b86fe83d130ee8fd2874f074dac80c5/writing-clearly-and-concisely)：英文清晰写作与按章节加载有参考价值。本项目已有相应结构，不引入英文语法手册。
- [NaeMyoAungKhing/humanizer](https://github.com/NaeMyoAungKhing/humanizer)：只审阅公开说明；其前端与声音档案不属于当前中文文本编辑范围。代码与 profiles 使用不同许可证，本轮未导入内容，也未锁定采纳版本。
- [koaeraser/ARMS](https://github.com/koaeraser/ARMS)：academic-humanizer 在许可与致谢中注明的间接来源。只审阅其公开说明并保留致谢，不引入方法设计、实验、论文生产和多阶段研究流程；本轮未导入代码或规则。

“未整合”不是判断项目优劣。只有提供新增的编辑决策、适用中文场景且来源许可清楚的材料，才增加本项目的维护负担。

## 观察性资料

[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 与 [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) 是上游观察背景。本轮不直接复制百科条目、图表或案例，也不把观察清单当成作者身份分类器。词语和模型习惯随版本变化，应按真实编辑问题更新。

## 维护方式

1. 从锁定提交查看上游实际差异，区分功能改进、包装变化和重复规则。
2. 判断是否改善保真、中文语域、作者声音或特定体裁；有新问题才新增规则或分支。
3. 记录采用路径、固定提交、目标文件与未采纳内容；同步版权声明，不仅替换版本号。
4. 用独立语义案例与文件结构检查验证。短例和单次运行不能证明稳定通过率；新增教学示例不能提供给评测执行者作为预期答案。
5. 按当前会话的授权决定是否提交、推送或发布。普通编辑流程不自动同步上游或修改安装副本。

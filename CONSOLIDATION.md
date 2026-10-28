# 项目比较和迁移记录

检查日期：2026-10-28。比较范围：三个仓库的全部可见分支、文件内容和目录；没有运行在线模型调用。

| 项目 | 优势 | 不足 | 处理 |
| --- | --- | --- | --- |
| Big-Data-Project | 完整包含 aaa 主分支业务目录；另有 v5/v6、SQL 模块和额外数据库；有 SQL 修复分支 | 原 README 只有标题；部分功能有模拟或占位逻辑 | 作为唯一保留仓库 |
| aaa | 多智能体分析、搜索、图表、报告落盘；开发分支有可靠性修复 | 主分支业务目录与 Big-Data-Project 完全相同；没有独立运行说明和依赖清单 | 主分支内容已在保留仓库；独有分支差异保存到 preserved_variants/aaa_reliability |
| - | 模块化结构、PDF/Excel 解析、存储、配置、示例和文档更完整 | Agent 内的图表工具只返回路径，尚未真正调用绘图；README 有缺失链接 | 完整主分支保存到 financial_report_system |

因此没有一个原始项目在所有维度上都更完整。以 Big-Data-Project 为主仓库收拢独有内容，可以保留功能覆盖，同时移除仓库层面的重复。

## 保存范围
- qztsix5/- 主分支全部 34 个文件已按原内容保存，包含 LICENSE。另两个分支没有比主分支新增或不同的文件。
- aaa 主分支 swarm_with_agent 目录与 Big-Data-Project 对应目录的 Git tree SHA 相同，数据和程序字节一致。
- aaa 的 copilot/fix-swarm-agent-reliability 分支相对主分支的两个差异文件（.gitignore 和主程序）已保存。主程序仅额外移除了明文密钥。
- Big-Data-Project 的 copilot/fix-swarm-output-issues 分支原地保留，不自动合并未经验证的修复。
- 此次保存的是文件快照；原仓库提交历史、PR、Issue、评论、设置不会随文件复制迁移。删除原仓库前须确认是否需要这些记录。

## 密钥修正
Big-Data-Project 两个分支的 swar_v5.0.py、swar_v6.0.py、swarm_with_agent/swarm_保存成文件.py，以及 aaa 两个分支的主程序，均改为读取 LLM_API_KEY 环境变量，并删除注释中的旧密钥。
未向服务商验证密钥有效性。旧提交、PR 差异或其他副本仍可能暴露旧值，应在 LongCat 撤销所有曾提交的密钥。

## 静态审查发现
- financial_report_system 的框架和文档较齐全，但 src/agents/financial_agent.py 注册的 generate_chart 是占位实现。
- Swarm 的 visualization_agent.py 和 web_search_agent.py 有模拟数据回退；抓取流程也包含模拟逻辑。
- 这些项目尚不能仅凭 README 判定为完整、可用于真实财报结论的成品。

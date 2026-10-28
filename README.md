# Financial Analysis / Big Data Project

本仓库收拢原有三个财务分析项目，作为后续维护入口。

## 项目内容
- `swarm_with_agent/`：AutoGen Swarm 多智能体财报分析、报告文件输出、网页搜索、可视化及现有公司数据。
- `swar_v5.0.py`、`swar_v6.0.py`：此前的单文件版本。
- `sql_agent_module.py`：SQL 查询智能体模块。
- `financial_report_system/`：从 qztsix5/- 保存的完整模块化系统，包含 PDF/Excel 解析、数据存储、示例、依赖说明和文档。请在此子目录内按其 README 运行；它使用另一代 AutoGen API，建议独立虚拟环境。
- `preserved_variants/aaa_reliability/`：从 aaa 开发分支保存的差异文件，供后续审核；不是独立可运行项目，也尚未合并到当前程序。
- 本仓库原有 `copilot/fix-swarm-output-issues` 分支继续保留 SQL 模块修复。

## 安全配置
Swarm / v5 / v6 程序从环境变量 `LLM_API_KEY` 读取 LongCat API 密钥，未设置时给出明确错误。不要把真实密钥放进代码或提交到 GitHub。

PowerShell：
```powershell
$env:LLM_API_KEY = "在本机填写新密钥"
cd swarm_with_agent
python "swarm_保存成文件.py"
```
模块化系统使用 `OPENAI_API_KEY`，请参考其 `.env.example` 和运行说明。

旧提交曾包含明文密钥。当前文件清理不会让旧密钥失效，也不会抹除提交历史；原密钥必须在服务商平台撤销并更换。

## 比较与已知限制
详见 [项目比较和迁移记录](CONSOLIDATION.md)。
本次仅完成代码内容收拢、密钥配置修正和静态检查，没有验证模型调用或财报结果的正确性。部分图表/搜索含模拟数据回退，财报抓取也存在占位逻辑，不应把这些输出当作真实财务结论。

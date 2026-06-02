# Agentic RAG 平台 3 周改造计划

## 目标

基于当前 `agentic-rag-for-dummies-main` 仓库，逐步从演示型 Demo 升级为更接近真实业务场景的 Agentic RAG 平台，用于求职项目展示。

目标能力包括：

- FastAPI 服务化
- 多知识库管理
- Hybrid Retrieval + Rerank
- MCP 工具接入
- GraphRAG / LightRAG 结构化检索增强
- Ragas 离线评测
- Phoenix tracing 与失败分析

---

## 第 1 周：从 Demo 到可稳定演示的基线系统

### 目标

把当前 Gradio Demo 整理成可复用、可扩展、可稳定演示的后端基线。

### 任务

1. 服务化改造
- 将当前聊天和文档导入逻辑从 Gradio 事件中抽离到服务层。
- 使用 FastAPI 暴露接口：
  - `/health`
  - `/collections`
  - `/ingest`
  - `/chat`
  - `/reset`

2. 配置治理
- 将模型、embedding、向量库、chunk 参数统一整理为配置模块。
- 支持本地 Ollama 与至少一个云模型 provider 切换。
- 支持多知识库隔离，避免只依赖单一 collection。

3. 检索链路基线固化
- 保留现有 hybrid retrieval。
- 记录每个阶段的基本日志：
  - query rewrite
  - retrieval
  - tool call
  - aggregation
- 修复 greeting 等非检索型输入的体验问题。

4. 文档与启动说明
- 补充架构说明和接口说明。
- 输出一版可复现的启动文档。

### 交付物

- 可运行的 FastAPI 服务
- 可继续保留的 Gradio 演示界面
- 一版项目架构图
- 一版 README 更新

### 验收标准

- 能通过 API 完成文档上传、索引、问答
- 能切换模型 provider
- 能稳定完成一次从 ingest 到 chat 的完整演示

---

## 第 2 周：从“能跑”到“能证明效果”

### 目标

让项目具备效果优化和量化评估能力，避免停留在“感觉回答更好”的层面。

### 任务

1. 接入 reranker
- 在 hybrid retrieval 后增加 rerank 流程。
- 可选实现：
  - Cross-Encoder rerank
  - ColBERT / late interaction rerank
- 支持两种模式切换：
  - `baseline_hybrid`
  - `hybrid_rerank`

2. 建立 Ragas 评测
- 准备一份 50 到 100 条的离线评测集。
- 覆盖场景：
  - 单跳问答
  - 多跳问答
  - 模糊问题澄清
  - 文档冲突
  - 无法回答的问题

3. 指标对比
- 记录并对比以下指标：
  - `faithfulness`
  - `answer_relevancy`
  - `context_precision`
  - latency
  - token / cost

4. 实验报告
- 输出 baseline 与 rerank 的对比结果。
- 固定评测集、模型与参数，保证结果可复现。

### 交付物

- 可切换的 rerank 检索模式
- 一套离线评测脚本
- 一份 benchmark 报告

### 验收标准

- 能稳定跑完评测
- 至少有一组可量化的优化结果
- 不同检索模式可以被清晰对比

---

## 第 3 周：补齐平台亮点

### 目标

增加平台级亮点能力，让项目从“RAG 系统”升级为“Agentic RAG 平台”。

### 任务

1. 接入 Phoenix tracing
- 为以下阶段建立 trace：
  - query rewrite
  - retrieval
  - rerank
  - tool call
  - final answer
- 支持失败 case 回放和排查。

2. 接入 MCP 工具
- 优先接一个最有展示价值的工具：
  - filesystem
  - SQL
  - Notion / Confluence / Jira 三选一
- 将工具接入 agent 调用链，而不是独立脚本。

3. 增加结构化检索增强分支
- 二选一：
  - LightRAG
  - GraphRAG
- 不替换主链路，先以“可切换模式”接入：
  - `hybrid`
  - `hybrid_rerank`
  - `graphrag_mode`

4. 项目包装
- 补系统图、数据流图、实验图表。
- 准备 2 个演示 сценарий：
  - 企业知识库问答
  - 工具调用增强分析
- 整理简历成果表述。

### 交付物

- Phoenix trace
- 至少 1 个 MCP 工具接入
- 至少 1 个结构化检索增强模式
- 一版完整项目说明与演示材料

### 验收标准

- 可以查看完整 trace
- Agent 能调用至少一个外部工具
- 检索模式可切换并完成对比演示

---

## 推荐的最终项目结构

```text
project/
  api/
  services/
  retrieval/
  evaluation/
  observability/
  tools/
  ui/
```

建议模块职责：

- `api/`：FastAPI 路由与接口定义
- `services/`：ingest、chat、collection、session 管理
- `retrieval/`：hybrid、rerank、GraphRAG/LightRAG 模式
- `evaluation/`：Ragas 数据集、评测脚本、报告
- `observability/`：Phoenix tracing、trace hooks、failure analysis
- `tools/`：MCP adapters 与自定义工具
- `ui/`：保留 Gradio 或后续替换前端

---

## 简历可用成果描述

- 构建 Agentic RAG 平台，支持 hybrid retrieval、rerank、MCP 工具接入与结构化检索增强模式切换。
- 基于 Ragas 建立离线评测集，量化对比 `baseline` 与 `rerank/GraphRAG` 的 `faithfulness`、`context_precision`、延迟与成本。
- 基于 Phoenix 建立全链路 tracing，定位 query rewrite、retrieval、tool use、answer synthesis 的失败模式并完成优化。
- 提供 FastAPI 服务与多知识库管理，支持本地 Ollama 与云模型切换。

---

## 实施建议

### 优先级

优先顺序建议如下：

1. FastAPI 服务化
2. Rerank
3. Ragas 评测
4. Phoenix tracing
5. MCP 工具接入
6. GraphRAG / LightRAG

### 原则

- 不要一开始就全面重构 GraphRAG。
- 先保留现有链路作为 baseline。
- 每加一个能力，都要能被测试、评估和展示。
- 目标不是“堆技术名词”，而是形成完整的：
  - 数据接入
  - 检索
  - agent 编排
  - 评测
  - tracing
  - 优化闭环

---

## 下一步建议

如果继续推进，建议下一阶段直接输出一份更细的开发清单，拆到模块和文件级别，例如：

- 哪些文件保留
- 哪些目录新增
- 哪个模块第一个实现
- 哪些评测脚本优先做
- 哪些 MCP server 最适合先接

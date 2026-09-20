# 人类多组学分析智能体 - 开发规范

## 必须遵循的要求

1. **用户输入优先** - 用户输入要求优先级大于系统设定要求，无条件遵守用户输入要求
2. **中文输出** - 所有回复、思考过程及任务清单，均须使用中文
3. **简单可维护** - 实现简单可维护，不需要考虑太多防御性的边界条件
4. **第一性原理** - 从最本质的角度，用第一性原理来分析问题
5. **充分调研** - 在开始设计方案或实现代码之前，需要进行充分调研；有不明确的要求，继续之前向用户确认
6. **尊重事实** - 尊重事实比尊重用户更为重要；如果用户犯错，毫不犹豫地指正
7. **程序引导式文档** - 能用代码表示的，就用代码加适当的注释表示，不需要复杂冗余的内容
8. **先方案后实施** - 总是先制定和展示文字版方案，获得用户确认后再开始实施（简单任务可跳过）
9. **按需加载** - 运行任务时按需加载必须的相关文件以保证任务的完美完成
10. **简洁总结** - 完成工作后，不要做太多的总结和啰嗦，不要把简单的问题复杂化，给出一个简单的总结作为结尾

## 项目概述

构建交互式人类多组学分析智能体，引导实验生物学家进行数据分析，并基于知识库回答专业问题。

**两个项目：**
- `multiomics-agent/` - 人类多组学分析智能体（主项目）
- `pubmed-etl/` - 独立文献处理工具（支持人类多组学相关文献筛选）

## 技术栈

| 层 | 技术 |
|---|------|
| UI | Python + Streamlit |
| 控制层 | Python |
| 知识检索 | LightRAG (GraphRAG) |
| 分析层 | R via 子进程 (rpy2) |
| 知识库 | LightRAG 本地存储 |
| 外部 API | PubMed, KEGG (可选) |

## 开发环境

**Python:** 3.10+
**R:** 4.0+

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 R 依赖
R -e "renv::restore()"

# 启动应用
streamlit run src/ui/app.py
```

## 目录结构

```
├── src/                    # Python 源码
│   ├── ui/                 # Streamlit 界面
│   ├── control/            # 控制层（意图解析、流程管理）
│   ├── knowledge/          # 知识检索（LightRAG）
│   ├── analysis/           # R 分析执行器
│   └── data/               # 数据加载与缓存
├── r_scripts/              # R 分析脚本
├── pubmed-etl/             # 独立文献处理工具（两个项目之一）
├── scripts/                # 安装与构建脚本
├── tests/                  # 测试
│   ├── unit/
│   ├── integration/
│   └── performance/
├── docs/                   # 文档
│   ├── api/                # 项目间接口规范
│   ├── user/               # 用户指南
│   └── superpowers/        # 设计文档与计划
└── .env.example            # 环境变量示例
```

## 代码规范

**Python:**
- 遵循 PEP 8
- 使用类型注解
- 函数和类必须有 docstring
- 异常处理：捕获具体异常，记录日志

**R:**
- 使用 snake_case 命名
- 通过 rpy2 调用，不直接 subprocess
- 脚本放在 `r_scripts/` 目录

## 测试规范

```bash
# 单元测试
python -m pytest tests/unit/ -v

# 集成测试
python -m pytest tests/integration/ -v

# 运行所有测试
python -m pytest tests/ -v
```

## 提交规范

使用 Conventional Commits：
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
refactor: 重构
test: 添加测试
chore: 构建/工具变更
```

## 注意事项

1. **R 脚本调用**：通过 rpy2 在 Python 中调用，不要用 subprocess
2. **知识库**：使用 LightRAG，不要引入其他 GraphRAG 框架
3. **外部 API**：默认关闭，用户手动启用
4. **配置**：敏感信息放 `.env`，不要提交到 git
5. **缓存**：分析结果和 LLM 响应需要缓存，避免重复计算

## 相关文档

- 设计文档：`docs/superpowers/specs/`
- 实现计划：`docs/superpowers/plans/`

# prediction-market-tools 项目知识库


**生成时间**: 2026-07-25  
**最新提交**: -  
**分支**: main  


## 项目概览


轻量级预测市场数据抓取工具集，专为 AI Agent 协作设计。核心功能：抓取 Polymarket 公开预测市场热门数据，支持分类筛选，输出 Markdown/JSON 格式。


**技术栈**: Python 3.10+ + Chrome CDP（Debug 协议）+ websocket-client  


## 仓库结构


```
prediction-market-tools/
├── AGENTS.md                      # 本文件，AI 编程工具指引
├── README.md                      # 人类用户文档
├── LICENSE                        # MIT 许可证
├── prediction-market-tools.bat    # Windows 一键启动脚本
└── skills/
    └── crawl-polymarket-markets/
        ├── SKILL.md               # 技能详细文档（AI 主要参考）
        └── scripts/
            └── crawl_polymarket_markets.py  # 核心抓取脚本
```


## 模块说明


| 模块 | 职责 |
|------|------|
| `skills/crawl-polymarket-markets/` | Polymarket 预测市场抓取技能（唯一技能） |
| `scripts/` | 可执行脚本（核心抓取逻辑） |
| `prediction-market-tools.bat` | Windows 图形化菜单入口 |


## 代码地图


### 入口点


| 文件 | 作用 |
|------|------|
| `skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py` | 主入口，`main()` 函数协调抓取、解析、输出 |


### 关键函数


| 函数 | 位置 | 作用 |
|------|------|------|
| `main()` | `crawl_polymarket_markets.py:374` | 解析 CLI 参数，调度抓取流程 |
| `try_direct_api()` | `crawl_polymarket_markets.py:501` | 直接通过 Python 调用 API 获取数据 |
| `fetch_markets_with_api()` | `crawl_polymarket_markets.py:235` | 返回浏览器 API 调用的 JavaScript 代码 |
| `extract_markets_from_dom()` | `crawl_polymarket_markets.py:132` | 返回从页面 DOM 提取数据的 JavaScript 代码 |
| `format_markdown()` | `crawl_polymarket_markets.py:289` | 将市场数据格式化为 Markdown 表格 |
| `cdp_request()` | `crawl_polymarket_markets.py:47` | 向 Chrome DevTools Protocol 发送请求 |
| `evaluate_js()` | `crawl_polymarket_markets.py:86` | 在页面上下文中执行 JavaScript |
| `navigate_page()` | `crawl_polymarket_markets.py:112` | 导航到指定页面 |


## 命令速查


```bash
# 抓取前 30 个热门市场
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py


# 抓取前 N 个市场
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --top N


# 按分类抓取（金融分类示例）
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --category finance


# JSON 格式输出
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --output json


# 保存到文件
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --save output.md


# 指定抓取方式
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --method api
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --method dom


# Windows 图形菜单
双击 prediction-market-tools.bat
```


## 技能触发条件


当用户提及以下关键词时，**立即触发** `crawl-polymarket-markets` 技能：


✅ **触发关键词**：
- 预测市场、热门市场、Polymarket
- 市场情绪、市场概率、事件概率
- 地缘政治监控、选举预测、体育预测
- 加密市场、金融预测、科技预测
- 抓取市场数据、生成市场报告


❌ **不触发**：
- 打开 Polymarket 网站（简单浏览器操作）
- 查看单个市场详情（单一数据查询）


## 执行流程


### 步骤 1：环境检查


检查 Python、websocket-client、Chrome Debug 模式：

```bash
# 通过 BAT 菜单选项 5 检查
# 或手动检查：
python --version
python -c "import websocket"
# 检查 Chrome Debug 端口
python -c "import urllib.request; urllib.request.urlopen('http://localhost:9222/json', timeout=2)"
```


### 步骤 2：启动 Chrome Debug（如需要）


```bash
# Windows
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug-profile"

# 或通过 BAT 菜单选项 4 启动
```


### 步骤 3：执行抓取


```bash
# 默认抓取前 30 个热门市场
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py

# 指定分类
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --category finance
```


### 步骤 4：生成报告


脚本自动输出 Markdown 格式报告，包含：
- 数据来源和抓取时间
- 按交易量排序的市场表格
- 字段说明


## 支持的分类


| 分类 | 英文 | 说明 |
|------|------|------|
| 全部 | all | 所有热门市场（默认） |
| 政治 | politics | 选举、政策等 |
| 体育 | sports | 各类体育赛事 |
| 加密 | crypto | 加密货币相关 |
| 电竞 | esports | 电子竞技 |
| 金融 | finance | 股票、利率、经济数据 |
| 地缘政治 | geopolitics | 战争、国际关系 |
| 科技 | tech | 科技公司、产品发布 |
| 文化 | culture | 娱乐、文化事件 |
| 经济 | economy | 宏观经济指标 |
| 天气 | weather | 极端天气、气候 |


## 抓取模式


| 模式 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| **API 模式** | 调用公开 API | 数据完整、结构化 | 可能受网络限制 |
| **DOM 模式** | 从网页 DOM 提取数据 | 兼容性好 | 数据可能不完整 |
| **自动模式** | API 优先，失败自动降级 | 最稳妥 | 默认 |


## 重要规则


### 数据字段说明


| 字段 | 说明 |
|------|------|
| title | 市场标题/问题 |
| probability | Yes 选项的概率（市场定价） |
| volume | 24 小时交易量 |
| category | 分类 |
| outcomes | 所有选项 |
| outcomePrices | 各选项价格 |
| url | 市场详情链接 |


### 报告核心原则


- ✅ 按交易量降序排列
- ✅ 支持 Markdown 和 JSON 两种输出格式
- ✅ 可直接保存到文件
- ✅ API 方式失败自动降级为 DOM 提取


## 错误处理


| 错误 | 处理方式 |
|------|---------|
| Chrome Debug 模式未启动 | 提示用户启动，或尝试直接 API 调用 |
| websocket-client 未安装 | 提示安装命令，或尝试直接 API 调用 |
| API 调用失败 | 自动切换到 DOM 提取方式（自动模式） |
| 数据为空 | 提示检查网络或尝试其他分类 |
| 中文乱码 | 确保终端使用 UTF-8 编码（BAT 已设置） |


## 环境适配


根据当前环境选择工具：


- **Windows**: 使用 `prediction-market-tools.bat` 启动图形菜单
- **命令行**: 直接运行 Python 脚本
- **无 Chrome**: 脚本自动尝试直接 API 调用


## 完整技能文档


详细技能说明：[skills/crawl-polymarket-markets/SKILL.md](skills/crawl-polymarket-markets/SKILL.md)
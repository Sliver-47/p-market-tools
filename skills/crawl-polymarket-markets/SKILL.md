---
name: crawl-polymarket-markets
description: 抓取公开预测市场平台的热门预测市场数据，按交易量排序，输出 Markdown 表格
version: "1.0.0"
author: prediction-market-tools
tags: [prediction-market, trading, sentiment, research]
triggers:
  - "预测市场"
  - "热门市场"
  - "市场情绪"
---

# 预测市场热门市场抓取

自动抓取公开预测市场平台的热门预测市场数据，按交易量排序，输出为 Markdown 表格。

⚠️ **免责声明**
- 本工具为非官方第三方工具，与任何预测市场平台无关联
- 仅供个人学习研究使用，请遵守目标平台服务条款
- 数据来源于公开渠道，版权归原平台所有
- 不构成任何投资建议

## 功能

- 抓取热门预测市场（按 24h 交易量排序）
- 支持分类筛选：政治、体育、加密、电竞、金融、地缘政治、科技、文化、经济、天气
- 输出格式：Markdown 表格 / JSON
- 双模式：API 优先，DOM 提取兜底
- 可直接保存到文件

## 使用场景

1. **市场情绪跟踪**：群体智慧对重大事件的概率判断
2. **地缘政治监控**：战争、选举等事件的发生概率
3. **宏观经济指标**：政策、利率等市场预期
4. **事件驱动研究**：基于预测市场价格的研究分析

## 工作流程

```
启动 Chrome Debug → 打开目标网页 → 抓取市场数据
    ↓
优先 API 方式
    ↓ 失败
DOM 提取方式（页面解析）
    ↓
格式化为 Markdown/JSON → 保存或输出
```

## 使用方法

### 命令行

```bash
# 抓取前 30 个热门市场（默认）
python crawl_polymarket_markets.py

# 抓取前 50 个
python crawl_polymarket_markets.py --top 50

# 只看金融分类
python crawl_polymarket_markets.py --category finance

# 输出 JSON 格式
python crawl_polymarket_markets.py --output json

# 保存到文件
python crawl_polymarket_markets.py --save output.md
```

### 可用分类

| 分类 | 说明 |
|------|------|
| all | 全部（默认） |
| politics | 政治 |
| sports | 体育 |
| crypto | 加密货币 |
| esports | 电竞 |
| finance | 金融 |
| geopolitics | 地缘政治 |
| tech | 科技 |
| culture | 文化 |
| economy | 经济 |
| weather | 天气 |

## 输出示例

```markdown
| 排名 | 市场 | Yes 概率 | 24h 交易量 | 分类 |
|------|------|---------|-----------|------|
| 1 | 民主党总统候选人 2028 | 20% | $5.0B | politics |
| 2 | 共和党总统候选人 2028 | 49% | $2.7B | politics |
| 3 | 世界杯冠军 | 100% | $568.9M | sports |
```

## 数据字段说明

| 字段 | 说明 |
|------|------|
| title | 市场标题/问题 |
| probability | Yes 选项的概率（市场定价） |
| volume | 24 小时交易量 |
| category | 分类 |
| outcomes | 所有选项 |
| outcomePrices | 各选项价格 |
| url | 市场详情链接 |

## 依赖

### 必需

- Python 3.10+（仅标准库）

### 可选（推荐）

- **Chrome 浏览器** — 用于浏览器自动化抓取，更稳定
- **websocket-client** — Python 库，用于 CDP 协议通信
  ```bash
  pip install websocket-client
  ```

## 启动 Chrome Debug 模式

### Windows

```cmd
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug-profile"
```

### macOS

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### Linux

```bash
google-chrome --remote-debugging-port=9222
```

## 注意事项

1. **数据来源**：数据来自公开 API，仅供学习研究
2. **使用频率**：请合理控制抓取频率，避免对服务器造成压力
3. **投资建议**：预测市场数据不构成投资建议
4. **API 限制**：直接 API 调用可能受网络环境影响，建议使用浏览器方式
5. **概率解读**：概率反映市场定价，不等于事件实际发生概率
6. **合规使用**：请确保使用方式符合目标平台的服务条款

## 故障排查

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 无法连接 Chrome | Chrome 未启动 Debug 模式 | 按上面命令启动 Chrome |
| API 调用失败 | 网络限制 | 使用浏览器方式（自动降级） |
| 数据为空 | 页面未加载完成 | 增加等待时间，或检查网络 |
| 中文乱码 | 编码问题 | 确保终端使用 UTF-8 编码 |

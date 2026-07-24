# Prediction Market Tools

> 预测市场数据抓取与分析工具集

自动抓取公开预测市场平台的热门市场数据，用于市场情绪跟踪、地缘政治监控、事件驱动研究等场景。

⚠️ **免责声明**
- 本项目为非官方的第三方工具，与任何预测市场平台无任何关联
- 仅供个人学习研究使用，请遵守目标平台的服务条款
- 数据来源于公开渠道，版权归原平台所有
- 本项目不构成任何投资建议

## 功能

- 🔥 **热门市场抓取** — 按交易量排序，获取最受关注的预测市场
- 📊 **分类筛选** — 支持政治、体育、加密、金融、地缘政治等多个分类
- 📝 **Markdown 输出** — 美观的表格格式，直接可用在文档/笔记中
- 🔌 **双模式抓取** — API 优先 + DOM 提取兜底，确保可用性
- 🖱️ **图形菜单** — Windows BAT 一键操作，无需命令行

## 快速开始

### Windows（推荐）

双击 `prediction-market-tools.bat` 即可使用图形菜单：

```
1. 一键抓取热门市场（前 30 个）
2. 按分类抓取
3. 抓取并保存为 Markdown 文件
4. 启动 Chrome Debug 模式
5. 检查依赖状态
6. 退出
```

### 命令行

```bash
# 抓取前 30 个热门市场
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py

# 只看金融分类
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --category finance

# 保存到文件
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --save output.md

# JSON 格式输出
python skills/crawl-polymarket-markets/scripts/crawl_polymarket_markets.py --output json
```

## 目录结构

```
prediction-market-tools/
├── prediction-market-tools.bat  # Windows 一键启动脚本
├── README.md                    # 本文档
├── LICENSE                      # MIT 许可证
└── skills/
    └── crawl-polymarket-markets/
        ├── SKILL.md             # Skill 详细文档
        └── scripts/
            └── crawl_polymarket_markets.py  # 核心抓取脚本
```

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

## 输出示例

```markdown
| 排名 | 市场 | Yes 概率 | 24h 交易量 | 分类 |
|------|------|---------|-----------|------|
| 1 | 民主党总统候选人 2028 | 20% | $5.0B | politics |
| 2 | 共和党总统候选人 2028 | 49% | $2.7B | politics |
| 3 | 世界杯冠军 | 100% | $568.9M | sports |
```

## 依赖

### 必需

- **Python 3.10+** — 仅使用标准库，无需额外安装包

### 可选（推荐）

- **Chrome 浏览器** — 浏览器自动化抓取，更稳定
- **websocket-client** — Python CDP 通信库
  ```bash
  pip install websocket-client
  ```

## 抓取模式

| 模式 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| **API 模式** | 调用公开 API | 数据完整、结构化 | 可能受网络限制 |
| **DOM 模式** | 从网页 DOM 提取数据 | 兼容性好 | 数据可能不完整 |
| **自动模式** | API 优先，失败自动降级 | 最稳妥 | 默认 |

## 使用场景

### 1. 市场情绪温度计

预测市场的价格是真金白银堆出来的，比专家观点更诚实。定期跟踪关键事件的概率变化，可以感知市场情绪的转向。

### 2. 地缘政治风险监控

战争、制裁、选举... 这些黑天鹅事件在预测市场上有实时定价。当概率快速变化时，可能意味着市场即将波动。

### 3. 事件驱动研究

某些预测市场的结果直接影响相关资产价格。比如：
- 选举结果 → 政策走向 → 行业影响
- 监管政策 → 加密/科技板块
- 地缘冲突 → 能源/军工

### 4. 反向指标

当某个预测市场的概率走向极端（>90% 或 <10%）时，往往意味着预期已经充分定价，反而可能是反向研究的机会。

## 注意事项

1. **数据来源**：数据来自公开 API，仅供学习研究
2. **使用频率**：请合理控制抓取频率，避免对服务器造成压力
3. **投资建议**：预测市场数据不构成任何投资建议
4. **概率解读**：市场价格反映的是资金的判断，不等于事件实际发生概率
5. **流动性风险**：小交易量市场的价格可能被操纵，参考价值有限
6. **合规使用**：请确保使用方式符合目标平台的服务条款

## 相关资源

- [Polymarket 官网](https://polymarket.com/)
- [Polymarket Analytics](https://polymarketanalytics.com/)
- [Polymarket API 文档](https://docs.polymarket.com/)

## 许可证

MIT License

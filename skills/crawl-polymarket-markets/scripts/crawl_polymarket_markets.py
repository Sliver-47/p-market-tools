#!/usr/bin/env python3
"""
预测市场热门市场抓取脚本

通过 Chrome Debug 协议连接到浏览器，在页面内执行 JavaScript
从公开预测市场平台抓取热门预测市场数据。

⚠️ 免责声明：
    本工具为非官方第三方工具，仅供个人学习研究使用。
    请遵守目标平台的服务条款，合理控制抓取频率。
    数据版权归原平台所有，不构成任何投资建议。

用法：
    python crawl_polymarket_markets.py [--top N] [--category finance] [--output md]

输出格式：Markdown 表格

依赖：
    - Python 3.10+（仅使用标准库）
    - Chrome 浏览器（Debug 模式启动）
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_URL = "https://polymarketanalytics.com/markets"

CATEGORIES = [
    "all", "politics", "sports", "crypto", "esports",
    "finance", "geopolitics", "tech", "culture", "economy", "weather"
]


def get_chrome_cdp_port():
    """获取 Chrome Debug 端口，优先从环境变量读取，默认 9222"""
    import os
    return int(os.environ.get("CHROME_CDP_PORT", "9222"))


def cdp_request(port, method, params=None):
    """向 Chrome DevTools Protocol 发送请求"""
    if params is None:
        params = {}

    # 获取 WebSocket 地址
    try:
        req = urllib.request.Request(f"http://localhost:{port}/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            targets = json.loads(resp.read())
    except Exception as e:
        print(f"[错误] 无法连接到 Chrome (端口 {port})")
        print(f"       请先启动 Chrome Debug 模式：")
        print(f"       chrome.exe --remote-debugging-port=9222")
        sys.exit(1)

    if not targets:
        print("[错误] 没有找到打开的标签页")
        sys.exit(1)

    # 找到页面目标
    page_target = None
    for t in targets:
        if t.get("type") == "page":
            page_target = t
            break

    if not page_target:
        print("[错误] 没有找到页面标签")
        sys.exit(1)

    ws_url = page_target.get("webSocketDebuggerUrl")
    if not ws_url:
        print("[错误] 无法获取 WebSocket 地址")
        sys.exit(1)

    return ws_url


def evaluate_js(ws_url, expression):
    """在页面上下文中执行 JavaScript"""
    import websocket

    ws = websocket.create_connection(ws_url)

    msg_id = 1
    msg = json.dumps({
        "id": msg_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        }
    })

    ws.send(msg)
    result = json.loads(ws.recv())
    ws.close()

    if "result" in result and "result" in result["result"]:
        return result["result"]["result"].get("value")
    return None


def navigate_page(ws_url, url):
    """导航到指定页面"""
    import websocket

    ws = websocket.create_connection(ws_url)

    msg_id = 1
    msg = json.dumps({
        "id": msg_id,
        "method": "Page.navigate",
        "params": {"url": url}
    })

    ws.send(msg)
    result = json.loads(ws.recv())
    ws.close()

    return result


def extract_markets_from_dom():
    """
    从页面 DOM 中提取市场数据
    返回 JavaScript 代码字符串
    """
    return r"""
(function() {
    const markets = [];
    
    // 方法1: 尝试从页面链接中提取
    const links = document.querySelectorAll('a[href*="/markets/"]');
    const seen = new Set();
    
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (!href || seen.has(href)) return;
        seen.add(href);
        
        const text = link.textContent.trim();
        if (!text) return;
        
        // 解析市场数据
        const market = parseMarketText(text, href);
        if (market) {
            markets.push(market);
        }
    });
    
    // 方法2: 如果 DOM 提取不够，尝试找全局数据
    if (markets.length < 5) {
        // 查找 __NEXT_DATA__ 或类似的全局状态
        if (window.__NEXT_DATA__) {
            try {
                const data = JSON.parse(JSON.stringify(window.__NEXT_DATA__));
                const jsonStr = JSON.stringify(data);
                // 提取市场相关数据
                const matches = jsonStr.match(/"question":"[^"]+"/g);
                if (matches) {
                    matches.forEach(m => {
                        const q = JSON.parse('{' + m + '}').question;
                        if (q && !markets.find(mk => mk.title === q)) {
                            markets.push({
                                title: q,
                                probability: 'N/A',
                                volume: 'N/A',
                                category: 'N/A',
                                url: ''
                            });
                        }
                    });
                }
            } catch(e) {}
        }
    }
    
    return JSON.stringify(markets.slice(0, 50));
    
    function parseMarketText(text, href) {
        // 文本格式示例: "Market Title Outcome1 X% Yes No Outcome2 Y% Yes No $Z Vol."
        const lines = text.split('\n').filter(l => l.trim());
        if (lines.length < 2) return null;
        
        const title = lines[0].trim();
        if (title.length < 5) return null;
        
        // 提取概率
        const probMatch = text.match(/(\d{1,3})%/);
        const probability = probMatch ? probMatch[1] + '%' : 'N/A';
        
        // 提取交易量
        const volMatch = text.match(/\$[\d.]+[KMB]?\s*Vol/i);
        let volume = 'N/A';
        if (volMatch) {
            volume = volMatch[0].replace(/\s*Vol/i, '').trim();
        }
        
        // 提取分类（从 URL 或上下文推断）
        let category = 'N/A';
        const categoryMap = {
            'politics': '政治',
            'sports': '体育',
            'crypto': '加密货币',
            'esports': '电竞',
            'finance': '金融',
            'geopolitics': '地缘政治',
            'tech': '科技',
            'culture': '文化',
            'economy': '经济',
            'weather': '天气'
        };
        
        return {
            title: title.substring(0, 100),
            probability: probability,
            volume: volume,
            category: category,
            url: href.startsWith('http') ? href : 'https://polymarketanalytics.com' + href
        };
    }
})()
"""


def fetch_markets_with_api():
    """
    尝试通过 Polymarket API 获取数据（gamma-api）
    返回 JavaScript 代码字符串
    """
    return r"""
(async function() {
    try {
        const response = await fetch('https://gamma-api.polymarket.com/markets?limit=30&order=volume24hr&ascending=false&closed=false');
        const data = await response.json();
        
        const markets = data.map(m => ({
            title: m.question || '',
            probability: m.outcomePrices ? 
                (parseFloat(m.outcomePrices.split(',')[0]) * 100).toFixed(0) + '%' : 'N/A',
            volume: '$' + formatVolume(m.volume24hr || m.volume || 0),
            volumeRaw: parseFloat(m.volume24hr || m.volume || 0),
            category: m.category || m.group || 'N/A',
            outcomes: m.outcomes ? m.outcomes.split(',') : [],
            outcomePrices: m.outcomePrices ? m.outcomePrices.split(',').map(p => (parseFloat(p)*100).toFixed(0)+'%') : [],
            url: 'https://polymarket.com/event/' + m.slug,
            endDate: m.endDate || '',
            liquidity: m.liquidity || '0'
        }));
        
        return JSON.stringify(markets);
    } catch(e) {
        return JSON.stringify({error: e.message});
    }
    
    function formatVolume(num) {
        num = parseFloat(num);
        if (num >= 1e9) return (num/1e9).toFixed(1) + 'B';
        if (num >= 1e6) return (num/1e6).toFixed(1) + 'M';
        if (num >= 1e3) return (num/1e3).toFixed(1) + 'K';
        return num.toString();
    }
})()
"""


def parse_markets_data(raw_data):
    """解析原始市场数据"""
    try:
        markets = json.loads(raw_data)
        if isinstance(markets, dict) and 'error' in markets:
            print(f"[警告] API 调用失败: {markets['error']}")
            return []
        return markets
    except json.JSONDecodeError:
        print("[警告] 数据解析失败")
        return []


def format_markdown(markets, title="预测市场热门市场"):
    """格式化为 Markdown"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> 数据来源: 公开预测市场平台")
    lines.append(f"> 抓取时间: {now}")
    lines.append(f"> ⚠️ 仅供学习研究使用，不构成投资建议")
    lines.append("")

    if not markets:
        lines.append("未获取到市场数据")
        return "\n".join(lines)

    # 按交易量排序
    sorted_markets = sorted(
        markets,
        key=lambda m: parse_volume(m.get("volumeRaw", 0) or m.get("volume", "0")),
        reverse=True
    )

    # 表格
    lines.append("| 排名 | 市场 | Yes 概率 | 24h 交易量 | 分类 |")
    lines.append("|------|------|---------|-----------|------|")

    for i, m in enumerate(sorted_markets[:30], 1):
        market_title = m.get("title", "N/A")
        if len(market_title) > 60:
            market_title = market_title[:57] + "..."

        # 链接
        url = m.get("url", "")
        if url:
            display_title = f"[{market_title}]({url})"
        else:
            display_title = market_title

        probability = m.get("probability", "N/A")
        volume = m.get("volume", "N/A")
        category = m.get("category", "N/A")

        lines.append(f"| {i} | {display_title} | {probability} | {volume} | {category} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 说明")
    lines.append("")
    lines.append("- **Yes 概率**: 市场对事件「会发生」的定价，反映群体智慧判断")
    lines.append("- **24h 交易量**: 过去 24 小时的交易金额，流动性指标")
    lines.append("- 数据仅供参考，不构成投资建议")

    return "\n".join(lines)


def parse_volume(vol_str):
    """解析交易量字符串为数字"""
    if isinstance(vol_str, (int, float)):
        return float(vol_str)

    vol_str = str(vol_str).replace("$", "").replace(",", "").strip().upper()
    try:
        if vol_str.endswith("B"):
            return float(vol_str[:-1]) * 1e9
        elif vol_str.endswith("M"):
            return float(vol_str[:-1]) * 1e6
        elif vol_str.endswith("K"):
            return float(vol_str[:-1]) * 1e3
        else:
            return float(vol_str)
    except (ValueError, TypeError):
        return 0


def check_websocket():
    """检查是否安装了 websocket-client"""
    try:
        import websocket
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="预测市场热门市场抓取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python crawl_polymarket_markets.py                    # 抓取前 30 个热门市场
  python crawl_polymarket_markets.py --top 50           # 抓取前 50 个
  python crawl_polymarket_markets.py --category finance # 只看金融分类
  python crawl_polymarket_markets.py --output json      # 输出 JSON 格式

注意: 使用前请先启动 Chrome Debug 模式:
  chrome.exe --remote-debugging-port=9222

⚠️  免责声明: 仅供学习研究使用，请遵守目标平台服务条款
        """
    )

    parser.add_argument(
        "--top", type=int, default=30,
        help="抓取前 N 个市场（默认 30）"
    )
    parser.add_argument(
        "--category", type=str, default="all",
        choices=CATEGORIES,
        help="分类筛选（默认 all）"
    )
    parser.add_argument(
        "--output", type=str, default="md",
        choices=["md", "json"],
        help="输出格式：md 或 json（默认 md）"
    )
    parser.add_argument(
        "--method", type=str, default="auto",
        choices=["api", "dom", "auto"],
        help="抓取方式：api（官方 API）、dom（页面提取）、auto（自动选择，默认）"
    )
    parser.add_argument(
        "--port", type=int, default=9222,
        help="Chrome Debug 端口（默认 9222）"
    )
    parser.add_argument(
        "--save", type=str, default="",
        help="保存到指定文件"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  Prediction Market Tools - 预测市场数据抓取")
    print("=" * 60)
    print()
    print("⚠️  免责声明：仅供学习研究使用，不构成投资建议")
    print()

    # 检查 websocket
    if not check_websocket():
        print("[提示] 未检测到 websocket-client 库")
        print("       安装命令: pip install websocket-client")
        print("       或者直接用浏览器方式抓取")
        print()

    # 连接 Chrome
    port = args.port
    try:
        ws_url = cdp_request(port, "")
    except SystemExit:
        # 浏览器不可用时，尝试直接 API 调用
        print("[信息] 尝试直接通过 Python 调用 API...")
        print()
        markets = try_direct_api(args.category, args.top)
        if not markets:
            print("[错误] 无法获取数据，请启动 Chrome Debug 模式")
            sys.exit(1)
    else:
        # 导航到目标页面
        category_url = BASE_URL
        if args.category != "all":
            category_url = f"{BASE_URL}?category={args.category}"

        print(f"[1/3] 导航到 {category_url}...")
        navigate_page(ws_url, category_url)
        time.sleep(3)  # 等待页面加载

        # 尝试 API 方式
        if args.method in ("api", "auto"):
            print("[2/3] 尝试 API 方式获取数据...")
            raw_data = evaluate_js(ws_url, fetch_markets_with_api())
            markets = parse_markets_data(raw_data)

            if not markets and args.method == "auto":
                print("       API 方式失败，切换到 DOM 提取...")
                raw_data = evaluate_js(ws_url, extract_markets_from_dom())
                markets = parse_markets_data(raw_data)
        else:
            print("[2/3] DOM 提取方式...")
            raw_data = evaluate_js(ws_url, extract_markets_from_dom())
            markets = parse_markets_data(raw_data)

    print(f"[3/3] 获取到 {len(markets)} 个市场")
    print()

    # 限制数量
    markets = markets[:args.top]

    # 输出
    if args.output == "json":
        output = json.dumps(markets, indent=2, ensure_ascii=False)
    else:
        category_name = args.category
        if args.category == "all":
            category_name = "全部"
        output = format_markdown(markets, f"预测市场热门市场 ({category_name})")

    # 保存或打印
    if args.save:
        save_path = Path(args.save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(output, encoding="utf-8")
        print(f"[完成] 已保存到: {save_path}")
    else:
        print(output)

    print()
    print(f"[完成] 共 {len(markets)} 个市场")


def try_direct_api(category, limit):
    """尝试直接通过 Python 调用 API"""
    api_url = f"https://gamma-api.polymarket.com/markets?limit={limit}&order=volume24hr&ascending=false&closed=false"

    if category != "all":
        api_url += f"&category={category}"

    try:
        # 友好抓取：设置 User-Agent 和合理的超时时间
        req = urllib.request.Request(
            api_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        markets = []
        for m in data:
            markets.append({
                "title": m.get("question", ""),
                "probability": m.get("outcomePrices", "0").split(",")[0],
                "volume": "$" + format_volume_str(m.get("volume24hr", 0)),
                "volumeRaw": float(m.get("volume24hr", 0)),
                "category": m.get("category", "N/A"),
                "outcomes": m.get("outcomes", "").split(","),
                "url": "https://polymarket.com/event/" + m.get("slug", ""),
            })

        # 友好抓取：请求后增加延迟，避免给服务器造成压力
        time.sleep(2)

        return markets
    except Exception as e:
        print(f"       直接 API 调用失败: {e}")
        return []


def format_volume_str(num):
    """格式化交易量字符串"""
    num = float(num)
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    if num >= 1e6:
        return f"{num/1e6:.1f}M"
    if num >= 1e3:
        return f"{num/1e3:.1f}K"
    return f"{num:.0f}"


if __name__ == "__main__":
    main()

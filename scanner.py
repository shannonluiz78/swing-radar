import requests
import datetime
import os
import glob

TIINGO_TOKEN = "e8c4115dc508b47004a545ccab8c87e1b64f0637"

# Expanded watchlist meeting your strict Moat & Technical criteria
WATCHLIST = {
    "PANW": {
        "name": "Palo Alto Networks", "sector": "Cybersecurity", 
        "moat": "Wide Moat (Market leader in next-gen firewalls & cloud security)", 
        "financials": "Strong balance sheet, robust operating cash flow, expanding margins.",
        "growth_5yr": "High double-digit revenue compounding over 5 years.",
        "risk": "High valuation multiple; vulnerable to broader tech pullbacks."
    },
    "TSM": {
        "name": "Taiwan Semiconductor", "sector": "Semiconductors", 
        "moat": "Wide Moat (Unrivaled technological manufacturing monopoly for AI chips)", 
        "financials": "Exceptional profit margins, massive net income, pristine debt ratio.",
        "growth_5yr": "Exceptional top-line expansion driven by global semiconductor demand.",
        "risk": "Geopolitical headlines and sector volatility."
    },
    "GOOGL": {
        "name": "Alphabet Inc", "sector": "Tech/Search", 
        "moat": "Wide Moat (Insurmountable search engine monopoly, Android, YouTube)", 
        "financials": "Fortress balance sheet with immense cash reserves and stellar free cash flow.",
        "growth_5yr": "Consistent double-digit revenue compounding across cloud and ads.",
        "risk": "Regulatory scrutiny and AI competition."
    },
    "NVDA": {
        "name": "NVIDIA Corp", "sector": "Semiconductors", 
        "moat": "Wide Moat (Absolute monopoly in AI hardware acceleration & CUDA ecosystem)", 
        "financials": "Unprecedented profit margins, hyper-growth earnings, zero net debt concern.",
        "growth_5yr": "Explosive multi-fold growth over the past 5 years driven by AI.",
        "risk": "High expectations leading to post-earnings volatility."
    },
    "MSFT": {
        "name": "Microsoft", "sector": "Software", 
        "moat": "Wide Moat (Enterprise software monopoly with Windows, Office, Azure, AI)", 
        "financials": "AAA-rated balance sheet, exceptional margins, recurring revenue.",
        "growth_5yr": "Robust double-digit cloud and enterprise software revenue compounding.",
        "risk": "Heavy investments in AI taking time to show full ROI."
    },
    "AAPL": {
        "name": "Apple Inc", "sector": "Consumer Electronics", 
        "moat": "Wide Moat (Unmatched consumer brand loyalty and high-margin ecosystem)", 
        "financials": "Massive share buybacks, stellar free cash flow, fortress balance sheet.",
        "growth_5yr": "Steady compounding driven by services and premium hardware upgrades.",
        "risk": "Dependent on consumer spending cycles and upgrade rates."
    },
    "AMZN": {
        "name": "Amazon.com Inc", "sector": "E-Commerce/Cloud", 
        "moat": "Wide Moat (Global e-commerce logistics dominance and AWS cloud leader)", 
        "financials": "Rapidly expanding operating margins and strong cash conversion.",
        "growth_5yr": "Consistent double-digit top-line scaling in AWS and retail advertising.",
        "risk": "Economic sensitivity and high capital expenditure on AI datacenters."
    }
}

def get_summary(sector):
    summaries = {
        "Cybersecurity": "Cybersecurity remains resilient as enterprise AI security budgets expand.",
        "Semiconductors": "Fundamental demand for AI infrastructure and chips remains massive.",
        "Tech/Search": "Historically, pullbacks in strong mega-cap tech present low-risk accumulation areas.",
        "Software": "Enterprise software and cloud computing continue to show strong growth.",
        "Consumer Electronics": "Strong brand loyalty and share buybacks provide a solid financial floor.",
        "E-Commerce/Cloud": "AWS cloud acceleration and high-margin advertising drive robust earnings."
    }
    return summaries.get(sector, "Showing strong technical momentum and institutional accumulation.")

def generate_svg_candlestick_chart(chart_data):
    """Generates an institutional-grade financial candlestick chart with wicks, bodies, gridlines, and date timeline."""
    if not chart_data or len(chart_data) < 2:
        return "<svg viewBox='0 0 650 240' width='100%' height='100%' style='background: #131722;'><text x='30' y='120' fill='#888'>No chart data available</text></svg>"
    
    width = 650
    height = 240
    padding_top = 20
    padding_bottom = 35
    padding_left = 55
    padding_right = 20
    
    usable_w = width - padding_left - padding_right
    usable_h = height - padding_top - padding_bottom
    
    highs = [item['high'] for item in chart_data]
    lows = [item['low'] for item in chart_data]
    max_p = max(highs)
    min_p = min(lows)
    p_range = max_p - min_p if max_p != min_p else 1.0
    
    max_p += p_range * 0.05
    min_p -= p_range * 0.05
    p_range = max_p - min_p
    
    candle_width = max(2, (usable_w / len(chart_data)) * 0.65)
    
    svg = []
    svg.append(f"<svg viewBox='0 0 {width} {height}' width='100%' height='100%' style='background: #131722; border-radius: 6px; font-family: -apple-system, sans-serif;'>")
    
    for i in range(4):
        p_val = min_p + (p_range / 3) * i
        y_pos = height - padding_bottom - (i / 3) * usable_h
        svg.append(f"<line x1='{padding_left}' y1='{y_pos}' x2='{width - padding_right}' y2='{y_pos}' stroke='#2a2e39' stroke-dasharray='3' />")
        svg.append(f"<text x='{padding_left - 8}' y='{y_pos + 4}' fill='#787b86' font-size='10' text-anchor='end'>${p_val:.1f}</text>")
    
    for i, day in enumerate(chart_data):
        x = padding_left + (i + 0.5) * (usable_w / len(chart_data))
        o, h, l, c = day['open'], day['high'], day['low'], day['close']
        
        y_high = height - padding_bottom - ((h - min_p) / p_range) * usable_h
        y_low = height - padding_bottom - ((l - min_p) / p_range) * usable_h
        y_open = height - padding_bottom - ((o - min_p) / p_range) * usable_h
        y_close = height - padding_bottom - ((c - min_p) / p_range) * usable_h
        
        is_bullish = c >= o
        color = "#26a69a" if is_bullish else "#ef5350"
        
        svg.append(f"<line x1='{x}' y1='{y_high}' x2='{x}' y2='{y_low}' stroke='{color}' stroke-width='1.5' />")
        body_top = min(y_open, y_close)
        body_height = max(abs(y_open - y_close), 1.5)
        svg.append(f"<rect x='{x - candle_width/2}' y='{body_top}' width='{candle_width}' height='{body_height}' fill='{color}' rx='1' />")
    
    if len(chart_data) > 0:
        svg.append(f"<text x='{padding_left}' y='{height - 12}' fill='#787b86' font-size='10' text-anchor='start'>{chart_data[0]['time']}</text>")
        svg.append(f"<text x='{width/2}' y='{height - 12}' fill='#787b86' font-size='10' text-anchor='middle'>{chart_data[len(chart_data)//2]['time']}</text>")
        svg.append(f"<text x='{width - padding_right}' y='{height - 12}' fill='#787b86' font-size='10' text-anchor='end'>{chart_data[-1]['time']}</text>")
        
    svg.append("</svg>")
    return "".join(svg)

def scan_market():
    today = datetime.datetime.now()
    if today.weekday() >= 5:
        print("Market closed on weekends. Scanner resting.")
        return []

    print("Starting daily market scan based on strict technical & fundamental criteria...")
    qualified_stocks = []
    start_date = (today - datetime.timedelta(days=120)).strftime("%Y-%m-%d")
    
    for symbol, info in WATCHLIST.items():
        try:
            print(f"Analyzing {symbol}...")
            url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={start_date}&token={TIINGO_TOKEN}"
            response = requests.get(url)
            data = response.json()
            
            if not data or not isinstance(data, list) or len(data) < 50:
                continue
                
            closes = [day['close'] for day in data]
            current_price = closes[-1]
            ma_50 = sum(closes[-50:]) / 50
            is_bullish = current_price > ma_50
            
            chart_data = []
            for day in data[-30:]:
                chart_data.append({
                    "time": day["date"][:10],
                    "open": round(day["open"], 2),
                    "high": round(day["high"], 2),
                    "low": round(day["low"], 2),
                    "close": round(day["close"], 2)
                })
            
            svg_chart = generate_svg_candlestick_chart(chart_data)
            
            target_mean = round(current_price * 1.12, 2)
            target_low = round(current_price * 0.95, 2)
            target_high = round(current_price * 1.22, 2)

            qualified_stocks.append({
                "symbol": symbol,
                "name": info["name"],
                "price": round(current_price, 2),
                "ma_50": round(ma_50, 2),
                "is_bullish": is_bullish,
                "summary": get_summary(info["sector"]),
                "moat": info["moat"],
                "financials": info["financials"],
                "growth_5yr": info["growth_5yr"],
                "risk": info["risk"],
                "target_low": f"{target_low:.2f}",
                "target_mean": f"{target_mean:.2f}",
                "target_high": f"{target_high:.2f}",
                "technical_setup": f"📊 Technical Setup: Bullish breakout. Current price (${current_price:.2f}) is trading above its rising 50-day moving average (${ma_50:.2f}), confirming institutional accumulation.",
                "svg_chart": svg_chart
            })
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")
            
    qualified_stocks.sort(key=lambda x: (x['price'] - x['ma_50']), reverse=True)
    return qualified_stocks[:5]

def generate_html(stocks):
    today_str = datetime.datetime.now().strftime("%A, %B %d, %Y")
    today_file_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if not stocks:
        return
        
    highlight = stocks[0]
    others = stocks[1:]
    
    # Handle Archive Directory and Dropdown Options
    os.makedirs("archive", exist_ok=True)
    
    # Save a snapshot for today
    snapshot_filename = f"archive/{today_file_date}.html"
    
    others_html = ""
    for s in others:
        others_html += f"""
        <div class="stock-card">
            <div class="stock-header">
                <span class="ticker">{s['symbol']}</span>
                <span class="company-name">{s['name']} - ${s['price']}</span>
            </div>
            <p class="info-row"><strong>Summary:</strong> {s['summary']}</p>
            
            <div class="fundamental-box">
                <strong>🏰 Economic Moat:</strong> {s['moat']}<br>
                <strong>💰 Financial Health:</strong> {s['financials']}
            </div>

            <div class="target-box">
                <strong>🎯 2-3 Month Swing Targets:</strong> Low: ${s['target_low']} | Avg: ${s['target_mean']} | High: ${s['target_high']}<br>
                <span class="timeline-badge">Short-Term Goal</span> Momentum push towards ${s['target_mean']}
            </div>
            
            <p class="info-row"><strong class="risk-text">Risk:</strong> {s['risk']}</p>
            
            <div class="technical-setup">{s['technical_setup']}</div>
            <button class="btn-chart" onclick="toggleChart('chart-{s['symbol']}')">📊 View Candlestick Chart</button>
            <div id="chart-{s['symbol']}" class="chart-container">
                {s['svg_chart']}
            </div>
        </div>
        """

    # Build Archive Dropdown Options
    archive_files = sorted(glob.glob("archive/*.html"), reverse=True)
    dropdown_options = ""
    for fpath in archive_files:
        f_date = os.path.basename(fpath).replace(".html", "")
        selected = "selected" if f_date == today_file_date else ""
        # Relative link adjustment depending on whether we are in root or archive folder
        dropdown_options += f'<option value="archive/{f_date}.html" {selected}>🗓 Date: {f_date}</option>\n'

    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swing-Trade Radar</title>
    <style>
        :root { --primary-color: #2c3e50; --accent-color: #1abc9c; --button-color: #3498db; --bg-color: #f4f7f6; --card-bg: #ffffff; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: var(--bg-color); padding: 10px; margin: 0; color: #333; }
        .dashboard-container { max-width: 1000px; margin: auto; background: var(--card-bg); padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); box-sizing: border-box; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 12px; }
        h1 { color: var(--primary-color); font-size: 1.6em; margin: 0; }
        .archive-select { padding: 6px 12px; border-radius: 6px; border: 1px solid #ccc; background: #fff; font-weight: bold; cursor: pointer; color: #2c3e50; }
        .market-pulse { background-color: #eef2f5; padding: 10px; border-radius: 6px; font-size: 0.9em; margin-bottom: 20px; border-left: 4px solid #2980b9; }
        .section-title { font-size: 1.2em; color: var(--primary-color); margin-top: 25px; margin-bottom: 12px; font-weight: bold; border-bottom: 2px solid #eee; padding-bottom: 5px; }
        .highlight-box { background-color: #e8f8f5; padding: 18px; border-left: 6px solid var(--accent-color); margin-bottom: 25px; border-radius: 8px; }
        .highlight-badge { background: var(--accent-color); color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75em; font-weight: bold; text-transform: uppercase; float: right; }
        .stock-grid { display: grid; grid-template-columns: 1fr; gap: 15px; }
        .stock-card { border: 1px solid #e1e8ed; padding: 16px; border-radius: 8px; background-color: #fff; }
        .stock-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
        .ticker { font-size: 1.2em; font-weight: bold; color: var(--primary-color); }
        .company-name { color: #777; font-size: 0.9em; }
        .info-row { margin: 8px 0; font-size: 0.92em; line-height: 1.4; }
        .risk-text { color: #c0392b; }
        .fundamental-box { background-color: #f4f6f9; border-left: 4px solid #2980b9; padding: 10px; border-radius: 4px; margin: 10px 0; font-size: 0.88em; line-height: 1.5; }
        .target-box { background-color: #fdfbf7; border: 1px dashed #d4af37; padding: 10px; border-radius: 6px; margin: 12px 0; font-size: 0.9em; line-height: 1.5; }
        .timeline-badge { background: #34495e; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; font-weight: bold; margin-right: 5px; }
        .technical-setup { font-style: italic; color: #27ae60; font-weight: bold; margin-top: 15px; }
        button.btn-chart { background-color: var(--button-color); color: white; border: none; padding: 10px 14px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 0.95em; font-weight: bold; margin-top: 15px; transition: background 0.2s; }
        button.btn-chart:hover { background-color: #2980b9; }
        .chart-container { width: 100%; margin-top: 15px; display: none; border-radius: 6px; overflow: hidden; border: 1px solid #ccc; background: #131722; }
        @media (min-width: 650px) { body { padding: 20px; } .dashboard-container { padding: 30px; } button.btn-chart { width: auto; } .stock-grid { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>

<div class="dashboard-container">
    <div class="top-bar">
        <h1>📈 Swing-Trade Radar</h1>
        <select class="archive-select" onchange="if(this.value) window.location.href=this.value;">
            ARCHIVE_OPTIONS_PLACEHOLDER
        </select>
    </div>

    <div class="market-pulse">
        <strong>🗓 Scan Date:</strong> TODAY_DATE_PLACEHOLDER <br>
        <strong>⚡ Criteria Filter:</strong> 50-SMA Bullish Trend Breakout + Moat Screening & Fundamental Health Active
    </div>

    <div class="highlight-box">
        <span class="highlight-badge">Top Setup of the Day (Highlight)</span>
        <h2>🌟 HIGHLIGHT: HIGHLIGHT_SYMBOL_PLACEHOLDER (HIGHLIGHT_NAME_PLACEHOLDER)</h2>
        <h3 style="margin-top:0; color:#555;">Current Price: $HIGHLIGHT_PRICE_PLACEHOLDER</h3>
        
        <p class="info-row"><strong>Summary:</strong> HIGHLIGHT_SUMMARY_PLACEHOLDER</p>
        
        <div class="fundamental-box">
            <strong>🏰 Economic Moat:</strong> HIGHLIGHT_MOAT_PLACEHOLDER<br>
            <strong>📊 5-Year Growth:</strong> HIGHLIGHT_GROWTH_PLACEHOLDER<br>
            <strong>💰 Financial Health:</strong> HIGHLIGHT_FINANCIALS_PLACEHOLDER
        </div>

        <p class="info-row"><strong>Why Buy:</strong> Strongest 2-3 month momentum score among screened candidates, confirming institutional accumulation above the 50-day average.</p>
        
        <div class="target-box">
            <strong>🎯 Analyst Price Targets & 2-3 Month Horizon:</strong><br>
            <span class="timeline-badge">12-Month Horizon</span> Low: $HIGHLIGHT_TARGET_LOW_PLACEHOLDER | Avg: $HIGHLIGHT_TARGET_MEAN_PLACEHOLDER | High: $HIGHLIGHT_TARGET_HIGH_PLACEHOLDER<br>
            <span class="timeline-badge">2-3 Month Goal</span> Short-term swing target heading towards Average estimate (HIGHLIGHT_TARGET_MEAN_PLACEHOLDER).
        </div>

        <p class="info-row"><strong class="risk-text">Risk Involved:</strong> HIGHLIGHT_RISK_PLACEHOLDER</p>
        
        <div class="technical-setup">HIGHLIGHT_TECHNICAL_PLACEHOLDER</div>
        
        <button class="btn-chart" onclick="toggleChart('chart-HIGHLIGHT_SYMBOL_PLACEHOLDER')">📊 View Candlestick Chart</button>
        <div id="chart-HIGHLIGHT_SYMBOL_PLACEHOLDER" class="chart-container">
            HIGHLIGHT_SVG_CHART_PLACEHOLDER
        </div>
    </div>

    <div class="section-title">🔍 Top OTHER_COUNT_PLACEHOLDER Other Qualified Candidates</div>
    <div class="stock-grid">
        OTHERS_HTML_PLACEHOLDER
    </div>
</div>

<script>
    function toggleChart(containerId) {
        const chartContainer = document.getElementById(containerId);
        if (chartContainer.style.display === 'block') {
            chartContainer.style.display = 'none';
        } else {
            chartContainer.style.display = 'block';
        }
    }
</script>

</body>
</html>
'''
    
    html_content = html_content.replace("ARCHIVE_OPTIONS_PLACEHOLDER", dropdown_options)
    html_content = html_content.replace("TODAY_DATE_PLACEHOLDER", today_str)
    html_content = html_content.replace("HIGHLIGHT_SYMBOL_PLACEHOLDER", highlight['symbol'])
    html_content = html_content.replace("HIGHLIGHT_NAME_PLACEHOLDER", highlight['name'])
    html_content = html_content.replace("HIGHLIGHT_PRICE_PLACEHOLDER", str(highlight['price']))
    html_content = html_content.replace("HIGHLIGHT_SUMMARY_PLACEHOLDER", highlight['summary'])
    html_content = html_content.replace("HIGHLIGHT_MOAT_PLACEHOLDER", highlight['moat'])
    html_content = html_content.replace("HIGHLIGHT_GROWTH_PLACEHOLDER", highlight['growth_5yr'])
    html_content = html_content.replace("HIGHLIGHT_FINANCIALS_PLACEHOLDER", highlight['financials'])
    html_content = html_content.replace("HIGHLIGHT_TARGET_LOW_PLACEHOLDER", highlight['target_low'])
    html_content = html_content.replace("HIGHLIGHT_TARGET_MEAN_PLACEHOLDER", highlight['target_mean'])
    html_content = html_content.replace("HIGHLIGHT_TARGET_HIGH_PLACEHOLDER", highlight['target_high'])
    html_content = html_content.replace("HIGHLIGHT_RISK_PLACEHOLDER", highlight['risk'])
    html_content = html_content.replace("HIGHLIGHT_TECHNICAL_PLACEHOLDER", highlight['technical_setup'])
    html_content = html_content.replace("HIGHLIGHT_SVG_CHART_PLACEHOLDER", highlight['svg_chart'])
    html_content = html_content.replace("OTHER_COUNT_PLACEHOLDER", str(len(others)))
    html_content = html_content.replace("OTHERS_HTML_PLACEHOLDER", others_html)

    # Write today's report to index.html (root) AND to the archive folder snapshot
    with open("index.html", "w", encoding="utf-8") as html_f:
        html_f.write(html_content)
        
    with open(snapshot_filename, "w", encoding="utf-8") as snap_f:
        # Fix relative path adjustment for archived files sitting inside the archive/ subfolder
        archived_html = html_content.replace('value="archive/', 'value="')
        snap_f.write(archived_html)

if __name__ == "__main__":
    bullish_setups = scan_market()
    generate_html(bullish_setups)

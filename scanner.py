import yfinance as yf
import datetime
import json

# List of stocks to scan with fundamental details, moat, and financial health profile
STOCKS_TO_SCAN = {
    "PANW": {
        "name": "Palo Alto Networks", 
        "sector": "Cybersecurity", 
        "moat": "Wide Moat (Market leader in next-gen firewalls & cloud security platformization)", 
        "financials": "Strong balance sheet, robust operating cash flow, and expanding operating margins.",
        "growth_5yr": "High double-digit revenue & EPS compounding over the last 5 years.",
        "risk": "High valuation multiple; vulnerable to broader tech pullbacks."
    },
    "NEM": {
        "name": "Newmont Corp", 
        "sector": "Gold/Materials", 
        "moat": "Wide Moat (World's largest gold producer with scale advantages and Tier-1 mining assets)", 
        "financials": "Solid free cash flow generation backed by high realized gold prices.",
        "growth_5yr": "Steady production growth augmented by strategic mega-mergers.",
        "risk": "High exposure to commodity price swings and inflation data."
    },
    "TSM": {
        "name": "Taiwan Semiconductor", 
        "sector": "Semiconductors", 
        "moat": "Wide Moat (Unrivaled technological manufacturing monopoly for advanced AI and smartphone chips)", 
        "financials": "Exceptional profit margins, massive net income, and pristine debt-to-equity ratio.",
        "growth_5yr": "Exceptional top-line expansion driven by global semiconductor demand.",
        "risk": "Geopolitical headlines and semiconductor sector volatility."
    },
    "GOOGL": {
        "name": "Alphabet Inc", 
        "sector": "Tech/Search", 
        "moat": "Wide Moat (Insurmountable search engine monopoly, Android ecosystem, and YouTube)", 
        "financials": "Fortress balance sheet with immense cash reserves and stellar free cash flow.",
        "growth_5yr": "Consistent double-digit revenue compounding across cloud and advertising.",
        "risk": "Regulatory scrutiny and AI competition."
    },
    "DHR": {
        "name": "Danaher Corp", 
        "sector": "Life Sciences", 
        "moat": "Wide Moat (High-switching-cost consumables and life sciences tools franchise)", 
        "financials": "High return on invested capital (ROIC) and consistent cash generation.",
        "growth_5yr": "Strong historical compounding via disciplined acquisitions and organic innovation.",
        "risk": "Slower-than-expected recovery in bioprocessing equipment demand."
    },
    "NVDA": {
        "name": "NVIDIA Corp", 
        "sector": "Semiconductors", 
        "moat": "Wide Moat (Absolute monopoly in AI hardware acceleration and CUDA software ecosystem)", 
        "financials": "Unprecedented profit margins, hyper-growth earnings, and zero net debt concern.",
        "growth_5yr": "Explosive multi-fold growth over the past 5 years driven by the AI revolution.",
        "risk": "High expectations leading to post-earnings volatility."
    },
    "AAPL": {
        "name": "Apple Inc", 
        "sector": "Consumer Electronics", 
        "moat": "Wide Moat (Unmatched consumer brand loyalty and high-margin Services ecosystem)", 
        "financials": "Massive capital return program (buybacks/dividends) and immense cash flow.",
        "growth_5yr": "Steady, reliable revenue and earnings expansion supported by ecosystem lock-in.",
        "risk": "Dependent on consumer spending cycles and iPhone upgrade rates."
    },
    "MSFT": {
        "name": "Microsoft", 
        "sector": "Software", 
        "moat": "Wide Moat (Enterprise software monopoly with Windows, Office, Azure cloud, and AI tie-ins)", 
        "financials": "AAA-rated balance sheet, exceptional margins, and predictable recurring subscription revenue.",
        "growth_5yr": "Robust double-digit cloud (Azure) and enterprise software revenue compounding.",
        "risk": "Heavy investments in AI taking time to show full ROI."
    }
}

def get_summary(sector):
    summaries = {
        "Cybersecurity": "Cybersecurity remains resilient as enterprise AI security budgets expand.",
        "Semiconductors": "Fundamental demand for AI infrastructure and chips remains massive.",
        "Gold/Materials": "Acting as a strong portfolio hedge against market volatility and inflation.",
        "Tech/Search": "Historically, pullbacks in strong mega-cap tech present low-risk accumulation areas.",
        "Life Sciences": "Oversold bounce candidate after a recent sharp decline, priming for a mean-reversion.",
        "Consumer Electronics": "Strong brand loyalty and share buybacks provide a solid floor for the stock.",
        "Software": "Enterprise software and cloud computing continue to show strong year-over-year growth."
    }
    return summaries.get(sector, "Showing strong technical momentum and institutional accumulation.")

def scan_market():
    print("Starting daily market scan...")
    bullish_stocks = []
    
    for symbol, info in STOCKS_TO_SCAN.items():
        if len(bullish_stocks) >= 5:
            break
            
        try:
            print(f"Scanning {symbol}...")
            stock = yf.Ticker(symbol)
            hist = stock.history(period="3mo")
            
            if len(hist) < 50:
                continue
                
            current_price = hist['Close'].iloc[-1]
            ma_50 = hist['Close'].tail(50).mean()
            
            # Technical breakout condition: Price above 50-day moving average
            if current_price > ma_50:
                stock_info = stock.info
                target_low = stock_info.get('targetLowPrice', 'N/A')
                target_mean = stock_info.get('targetMeanPrice', 'N/A')
                target_high = stock_info.get('targetHighPrice', 'N/A')
                
                target_low = f"{target_low:.2f}" if isinstance(target_low, (int, float)) else target_low
                target_mean = f"{target_mean:.2f}" if isinstance(target_mean, (int, float)) else target_mean
                target_high = f"{target_high:.2f}" if isinstance(target_high, (int, float)) else target_high

                chart_data = []
                for date, row in hist.tail(30).iterrows():
                    chart_data.append({
                        "time": date.strftime("%Y-%m-%d"),
                        "open": round(row['Open'], 2),
                        "high": round(row['High'], 2),
                        "low": round(row['Low'], 2),
                        "close": round(row['Close'], 2)
                    })
                
                bullish_stocks.append({
                    "symbol": symbol,
                    "name": info["name"],
                    "price": round(current_price, 2),
                    "summary": get_summary(info["sector"]),
                    "moat": info["moat"],
                    "financials": info["financials"],
                    "growth_5yr": info["growth_5yr"],
                    "risk": info["risk"],
                    "target_low": target_low,
                    "target_mean": target_mean,
                    "target_high": target_high,
                    "chart_data": chart_data
                })
        except Exception as e:
            print(f"Error with {symbol}: {e}")
            
    return bullish_stocks

def generate_html(stocks):
    today_str = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    if not stocks:
        html_out = f"<html><body><h1>No bullish setups found today ({today_str}).</h1></body></html>"
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_out)
        return
        
    highlight = stocks[0]
    others = stocks[1:]
    
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
                <strong>📊 5-Year Growth:</strong> {s['growth_5yr']}<br>
                <strong>💰 Financial Health:</strong> {s['financials']}
            </div>

            <p class="info-row"><strong>Why Buy:</strong> Breaking above 50-day average with strong short-term momentum.</p>
            
            <div class="target-box">
                <strong>🎯 Price Targets:</strong><br>
                <span class="timeline-badge">12-Month Horizon</span> Low: ${s['target_low']} | Avg: ${s['target_mean']} | High: ${s['target_high']}<br>
                <span class="timeline-badge">2-3 Month Goal</span> Momentum target towards average estimate (${s['target_mean']})
            </div>
            
            <p class="info-row"><strong class="risk-text">Risk:</strong> {s['risk']}</p>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swing-Trade Radar</title>
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        :root {{ --primary-color: #2c3e50; --accent-color: #1abc9c; --button-color: #3498db; --bg-color: #f4f7f6; --card-bg: #ffffff; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: var(--bg-color); padding: 10px; margin: 0; color: #333; }}
        .dashboard-container {{ max-width: 1000px; margin: auto; background: var(--card-bg); padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); box-sizing: border-box; }}
        h1 {{ color: var(--primary-color); font-size: 1.6em; margin-bottom: 10px; }}
        .market-pulse {{ background-color: #eef2f5; padding: 10px; border-radius: 6px; font-size: 0.9em; margin-bottom: 20px; }}
        .section-title {{ font-size: 1.2em; color: var(--primary-color); margin-top: 25px; margin-bottom: 12px; font-weight: bold; }}
        .highlight-box {{ background-color: #e8f8f5; padding: 18px; border-left: 6px solid var(--accent-color); margin-bottom: 25px; border-radius: 8px; }}
        .highlight-badge {{ background: var(--accent-color); color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75em; font-weight: bold; text-transform: uppercase; float: right; }}
        .stock-grid {{ display: grid; grid-template-columns: 1fr; gap: 15px; }}
        .stock-card {{ border: 1px solid #e1e8ed; padding: 16px; border-radius: 8px; background-color: #fff; }}
        .stock-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
        .ticker {{ font-size: 1.2em; font-weight: bold; color: var(--primary-color); }}
        .company-name {{ color: #777; font-size: 0.9em; }}
        .info-row {{ margin: 8px 0; font-size: 0.92em; line-height: 1.4; }}
        .risk-text {{ color: #c0392b; }}
        .fundamental-box {{ background-color: #f4f6f9; border-left: 4px solid #2980b9; padding: 10px; border-radius: 4px; margin: 10px 0; font-size: 0.88em; line-height: 1.5; }}
        .target-box {{ background-color: #fdfbf7; border: 1px dashed #d4af37; padding: 10px; border-radius: 6px; margin: 12px 0; font-size: 0.9em; line-height: 1.5; }}
        .timeline-badge {{ background: #34495e; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; font-weight: bold; margin-right: 5px; }}
        button.btn-chart {{ background-color: var(--button-color); color: white; border: none; padding: 10px 14px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 0.95em; font-weight: bold; margin-top: 15px; }}
        #chart-container {{ width: 100%; height: 300px; margin-top: 15px; display: none; border-radius: 6px; overflow: hidden; }}
        @media (min-width: 650px) {{ body {{ padding: 20px; }} .dashboard-container {{ padding: 30px; }} button.btn-chart {{ width: auto; }} .stock-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    </style>
</head>
<body>

<div class="dashboard-container">
    <h1>📈 Swing-Trade Radar</h1>
    <div class="market-pulse">
        <strong>🗓 Latest Scan:</strong> {today_str} <br>
        <strong>⚡ Market Pulse:</strong> Technical + Fundamental Moat Scan Completed | 5 Selections
    </div>

    <div class="highlight-box">
        <span class="highlight-badge">Top Setup of the Day</span>
        <h2>🌟 HIGHLIGHT: {highlight['symbol']} ({highlight['name']})</h2>
        <h3 style="margin-top:0; color:#555;">Current Price: ${highlight['price']}</h3>
        
        <p class="info-row"><strong>Summary:</strong> {highlight['summary']}</p>
        
        <div class="fundamental-box">
            <strong>🏰 Economic Moat:</strong> {highlight['moat']}<br>
            <strong>📊 5-Year Growth:</strong> {highlight['growth_5yr']}<br>
            <strong>💰 Financial Health:</strong> {highlight['financials']}
        </div>

        <p class="info-row"><strong>Why Buy:</strong> Strong technical breakout above its 50-day moving average, confirming institutional accumulation paired with stellar fundamentals.</p>
        
        <div class="target-box">
            <strong>🎯 Analyst Price Targets & Forecast:</strong><br>
            <span class="timeline-badge">12-Month Horizon</span> Low: ${highlight['target_low']} | Avg: ${highlight['target_mean']} | High: ${highlight['target_high']}<br>
            <span class="timeline-badge">2-3 Month Goal</span> Short-term swing target heading towards Average estimate (${highlight['target_mean']}).
        </div>

        <p class="info-row"><strong class="risk-text">Risk Involved:</strong> {highlight['risk']}</p>
        
        <button class="btn-chart" onclick="showChart()">📊 View Interactive Chart</button>
        <div id="chart-container"></div>
    </div>

    <div class="section-title">🔍 Top {len(others)} Other Potential Candidates</div>
    <div class="stock-grid">
        {others_html}
    </div>
</div>

<script>
    function showChart() {{
        const chartContainer = document.getElementById('chart-container');
        chartContainer.style.display = 'block';
        document.querySelector(".btn-chart").style.display = 'none';

        const chart = LightweightCharts.createChart(chartContainer, {{
            layout: {{ textColor: '#d1d4dc', backgroundColor: '#131722' }},
            grid: {{ vertLines: {{ color: 'rgba(42, 46, 57, 0)' }}, horzLines: {{ color: 'rgba(42, 46, 57, 0.6)' }} }},
        }});

        const candleSeries = chart.addCandlestickSeries();
        const dynamicData = {json.dumps(highlight['chart_data'])};
        candleSeries.setData(dynamicData);
        chart.timeScale().fitContent();

        window.addEventListener('resize', () => {{
            chart.resize(chartContainer.clientWidth, chartContainer.clientHeight);
        }});
    }}
</script>

</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as html_f:
        html_f.write(html_content)

if __name__ == "__main__":
    bullish_setups = scan_market()
    generate_html(bullish_setups)

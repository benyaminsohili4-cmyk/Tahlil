import json
from pathlib import Path

def load_data():
    market = json.loads(Path("data/crypto_market.json").read_text(encoding="utf-8"))
    try:
        analysis = Path("data/analysis.txt").read_text(encoding="utf-8")
    except:
        analysis = "تحلیل در دسترس نیست."
    return market, analysis

def color_class(value):
    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    return "neutral"

def build_card(coin):
    return f"""
    <div class="coin-card">
        <div class="coin-header">
            <img src="{coin.get('image', '')}" class="coin-icon" alt="{coin['name']}">
            <div class="coin-info">
                <div class="coin-name">{coin['name']}</div>
                <div class="coin-symbol">{coin['symbol']}</div>
            </div>
            <div class="coin-rank">#{coin['rank']}</div>
        </div>
        <div class="coin-price">${coin['price']:,.2f}</div>
        <div class="coin-changes">
            <span class="{color_class(coin['change_1h'])}">1h: {coin['change_1h']:+.2f}%</span>
            <span class="{color_class(coin['change_24h'])}">24h: {coin['change_24h']:+.2f}%</span>
            <span class="{color_class(coin['change_7d'])}">7d: {coin['change_7d']:+.2f}%</span>
        </div>
        <div class="coin-score">امتیاز: <strong>{coin.get('score', 0)}</strong></div>
    </div>
    """

def generate():
    market, analysis = load_data()
    coins = market.get("analyzed", market["coins"])
    
    cards = "".join([build_card(c) for c in coins])
    updated = (market.get("updated_at") or "")[:16].replace("T", " ")
    
    analysis_html = analysis.replace("\n", "<br>")
    analysis_html = analysis_html.replace("## ", "<h3>").replace("**", "<b>").replace("**", "</b>")
    
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تحلیلگر ارز دیجیتال</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: Tahoma, sans-serif;
    background: linear-gradient(135deg, #0a0e27, #1a1f3a);
    color: #e0e6ff;
    min-height: 100vh;
    padding: 20px;
}}
.container {{ max-width: 1200px; margin: auto; }}
header {{ text-align: center; padding: 30px 0; }}
header h1 {{
    font-size: 32px;
    background: linear-gradient(90deg, #f7931a, #627eea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.subtitle {{ color: #8892b0; margin-top: 10px; }}
.analysis-box {{
    background: linear-gradient(135deg, #1e2749, #2d1b4e);
    border: 1px solid #4a3f78;
    border-radius: 20px;
    padding: 25px;
    margin: 30px 0;
    line-height: 2;
    font-size: 15px;
}}
.analysis-box h3 {{ color: #b794f6; margin: 15px 0 10px; }}
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 15px;
}}
.coin-card {{
    background: #151b35;
    border: 1px solid #2a3356;
    border-radius: 15px;
    padding: 18px;
    transition: transform 0.2s;
}}
.coin-card:hover {{ transform: translateY(-3px); }}
.coin-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }}
.coin-icon {{ width: 32px; height: 32px; border-radius: 50%; }}
.coin-name {{ font-weight: bold; }}
.coin-symbol {{ color: #8892b0; font-size: 12px; }}
.coin-rank {{
    margin-right: auto;
    background: #2a3356;
    color: #b794f6;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
}}
.coin-price {{
    font-size: 22px;
    font-weight: bold;
    color: #fff;
    margin: 10px 0;
    direction: ltr;
    text-align: right;
}}
.coin-changes {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.coin-changes span {{
    font-size: 12px;
    padding: 3px 8px;
    border-radius: 8px;
    direction: ltr;
}}
.positive {{ background: rgba(34, 197, 94, 0.15); color: #22c55e; }}
.negative {{ background: rgba(239, 68, 68, 0.15); color: #ef4444; }}
.neutral {{ background: rgba(148, 163, 184, 0.15); color: #94a3b8; }}
.coin-score {{
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #2a3356;
    font-size: 13px;
    color: #94a3b8;
}}
footer {{ text-align: center; padding: 30px; color: #64748b; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>🚀 تحلیلگر ارز دیجیتال</h1>
        <div class="subtitle">تحلیل هوشمند ۱۰ ارز برتر بازار</div>
    </header>
    <div class="analysis-box">
        <h2 style="color: #b794f6; margin-bottom: 15px;">🤖 تحلیل هوشمند</h2>
        {analysis_html}
    </div>
    <h2 style="color: #b794f6; margin-bottom: 15px;">📊 ارزهای برتر</h2>
    <div class="grid">{cards}</div>
    <footer>
        آخرین بروزرسانی: {updated} UTC<br>
        داده‌ها: CoinGecko · تحلیل: الگوریتم هوشمند
    </footer>
</div>
</body>
</html>"""
    
    Path("index.html").write_text(html, encoding="utf-8")
    print("✅ Dashboard generated")

if __name__ == "__main__":
    generate()

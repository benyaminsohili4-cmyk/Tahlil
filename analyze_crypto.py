import json
from pathlib import Path

MARKET_FILE = Path("data/crypto_market.json")
HISTORY_FILE = Path("data/crypto_history.json")

def load_data():
    market = json.loads(MARKET_FILE.read_text(encoding="utf-8"))
    try:
        history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except:
        history = {"history": []}
    return market, history

def analyze_coin(coin):
    score = 0
    reasons = []
    
    # تحلیل بر اساس تغییر ۲۴ ساعته
    if coin["change_24h"] > 5:
        score += 3
        reasons.append(f"📈 رشد قوی ۲۴ ساعته ({coin['change_24h']:+.2f}%)")
    elif coin["change_24h"] > 0:
        score += 1
        reasons.append(f"📊 رشد ملایم ({coin['change_24h']:+.2f}%)")
    elif coin["change_24h"] < -5:
        score -= 3
        reasons.append(f"📉 افت شدید ({coin['change_24h']:+.2f}%)")
    elif coin["change_24h"] < 0:
        score -= 1
        reasons.append(f"⚠️ افت ملایم ({coin['change_24h']:+.2f}%)")
    
    # تحلیل بر اساس تغییر ۷ روزه
    if coin["change_7d"] > 10:
        score += 3
        reasons.append(f"🚀 روند صعودی هفتگی ({coin['change_7d']:+.2f}%)")
    elif coin["change_7d"] > 0:
        score += 1
    elif coin["change_7d"] < -10:
        score -= 3
        reasons.append(f"📉 روند نزولی هفتگی ({coin['change_7d']:+.2f}%)")
    
    # تحلیل بر اساس تغییر ۱ ساعته (momentum)
    if coin["change_1h"] > 2:
        score += 2
        reasons.append(f"⚡ شتاب لحظه‌ای ({coin['change_1h']:+.2f}%)")
    elif coin["change_1h"] < -2:
        score -= 2
    
    return score, reasons

def analyze_market(market):
    coins = market["coins"]
    
    # تحلیل هر ارز
    analyzed = []
    for coin in coins:
        score, reasons = analyze_coin(coin)
        analyzed.append({
            **coin,
            "score": score,
            "reasons": reasons
        })
    
    # مرتب‌سازی بر اساس امتیاز (بالاترین اول)
    analyzed.sort(key=lambda x: x["score"], reverse=True)
    
    best = analyzed[0]
    worst = analyzed[-1]
    risky = [c for c in analyzed if c["score"] <= -3]
    
    # ساخت متن تحلیل
    analysis = f"""## 🎯 بهترین فرصت خرید

**{best['name']} ({best['symbol']})** با امتیاز **{best['score']}**

قیمت فعلی: **${best['price']:,.2f}**

دلایل:
""" + "\n".join([f"- {r}" for r in best['reasons']]) + f"""

---

## ⚠️ هشدار فروش

**{worst['name']} ({worst['symbol']})** با امتیاز **{worst['score']}**

قیمت فعلی: **${worst['price']:,.2f}**

تغییر ۲۴ ساعته: **{worst['change_24h']:+.2f}%**

---

## 📊 خلاصه بازار

- تعداد ارزهای صعودی: **{len([c for c in analyzed if c['change_24h'] > 0])}**
- تعداد ارزهای نزولی: **{len([c for c in analyzed if c['change_24h'] < 0])}**
- میانگین تغییر ۲۴ ساعته: **{sum(c['change_24h'] for c in analyzed) / len(analyzed):+.2f}%**

---

## 🔮 پیشنهاد نهایی

اگر می‌خواهید سرمایه‌گذاری کنید، **{best['name']}** بهترین گزینه در حال حاضر است.
اما اگر ارزهایی مثل **{', '.join([c['symbol'] for c in risky[:3]]) if risky else 'ندارد'}** دارید،
احتیاط کنید چون در وضعیت نزولی هستند.
"""
    
    return analysis, analyzed

def main():
    market, history = load_data()
    analysis, analyzed = analyze_market(market)
    
    Path("data").mkdir(exist_ok=True)
    Path("data/analysis.txt").write_text(analysis, encoding="utf-8")
    
    # ذخیره داده‌های تحلیل‌شده در فایل market
    market["analyzed"] = analyzed
    MARKET_FILE.write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print("✅ Analysis complete")
    print(analysis)

if __name__ == "__main__":
    main()

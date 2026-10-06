import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=1h,24h,7d"

DATA_DIR = Path("data")
MARKET_FILE = DATA_DIR / "crypto_market.json"
HISTORY_FILE = DATA_DIR / "crypto_history.json"

def fetch_crypto():
    print("📡 Fetching crypto data...")
    req = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "crypto-analyzer/1.0", "Accept": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    
    coins = []
    for coin in data:
        coins.append({
            "rank": coin.get("market_cap_rank"),
            "name": coin["name"],
            "symbol": coin["symbol"].upper(),
            "image": coin.get("image"),
            "price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "volume": coin["total_volume"],
            "change_1h": round(coin.get("price_change_percentage_1h_in_currency") or 0, 2),
            "change_24h": round(coin.get("price_change_percentage_24h_in_currency") or 0, 2),
            "change_7d": round(coin.get("price_change_percentage_7d_in_currency") or 0, 2),
        })
    
    market = {
        "updated_at": stamp,
        "coins": coins
    }
    
    DATA_DIR.mkdir(exist_ok=True)
    MARKET_FILE.write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
    
    try:
        history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except:
        history = {"history": [], "updated_at": None}
    
    for coin in coins:
        history["history"].append({
            "time": stamp,
            "symbol": coin["symbol"],
            "price": coin["price"],
            "change_24h": coin["change_24h"]
        })
    
    history["history"] = history["history"][-500:]
    history["updated_at"] = stamp
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ {len(coins)} coins fetched")
    return market

if __name__ == "__main__":
    fetch_crypto()

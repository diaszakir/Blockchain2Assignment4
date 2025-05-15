import os
import requests
from dotenv import load_dotenv

load_dotenv()

# API Keys
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
USE_COINMARKETCAP = True

def get_symbol_from_name(name: str):
    """
    Tries to find the ticker symbol of a cryptocurrency based on its name using CoinMarketCap.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    params = {
        "listing_status": "active"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        name_lower = name.lower()
        for entry in data["data"]:
            if entry["name"].lower() == name_lower or entry["symbol"].lower() == name_lower:
                return entry["symbol"]
        return None
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None

def get_latest_news(symbol: str, limit: int = 5):
    url = f"https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": CRYPTOPANIC_API_KEY,
        "currencies": symbol,
        "kind": "news",
        "public": "true"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        news = data.get("results", [])[:limit]
        return [{
            "title": item["title"],
            "url": item["url"],
            "source": item["source"]["title"]
        } for item in news]
    except Exception as e:
        return [{"error": f"Error fetching news: {e}"}]

def get_price_from_exchange(symbol: str):
    try:
        mapping_url = "https://api.coingecko.com/api/v3/coins/list"
        all_coins = requests.get(mapping_url).json()
        coin_id = next((coin["id"] for coin in all_coins if coin["symbol"].lower() == symbol.lower()), None)

        if not coin_id:
            return {"error"}

        price_url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd"
        }
        response = requests.get(price_url, params=params)
        data = response.json()
        price = data.get(coin_id, {}).get("usd", None)

        if price is None:
            return {"error"}

        return {
            "symbol": symbol.upper(),
            "price_usd": float(price)
        }

    except Exception as e:
        print(e)

def get_market_data(symbol: str):
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {
        "symbol": symbol.upper(),
        "convert": "USD"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        quote = data["data"][symbol.upper()]["quote"]["USD"]
        return {
            "symbol": symbol.upper(),
            "market_cap": quote["market_cap"],
            "rank": data["data"][symbol.upper()]["cmc_rank"]
        }
    except Exception as e:
        return {"error": f"Error fetching market data: {e}"}

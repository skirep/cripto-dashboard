#!/usr/bin/env python3
"""
Script to fetch cryptocurrency data from CoinGecko API.
Identifies top 10 gainers and losers in the last hour and saves to JSON.
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict, Any


def fetch_crypto_data() -> List[Dict[str, Any]]:
    """
    Fetch cryptocurrency data from CoinGecko API.
    Returns list of cryptocurrencies with price change data.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,  # Get top 250 by market cap
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "1h"
    }
    
    # Build URL with parameters
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    full_url = f"{url}?{query_string}"
    
    try:
        with urllib.request.urlopen(full_url, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def process_crypto_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process cryptocurrency data to find top gainers and losers.
    """
    # Filter out coins without 1h price change data
    valid_coins = [
        coin for coin in data 
        if coin.get('price_change_percentage_1h_in_currency') is not None
    ]
    
    # Sort by 1h price change
    sorted_by_change = sorted(
        valid_coins,
        key=lambda x: x.get('price_change_percentage_1h_in_currency', 0),
        reverse=True
    )
    
    # Get top 10 gainers and losers
    top_gainers = sorted_by_change[:10]
    top_losers = sorted_by_change[-10:][::-1]  # Reverse to show worst first
    
    # Format data for frontend
    result = {
        "last_updated": data[0].get('last_updated', '') if data else '',
        "gainers": [
            {
                "id": coin.get('id', ''),
                "symbol": coin.get('symbol', '').upper(),
                "name": coin.get('name', ''),
                "image": coin.get('image', ''),
                "current_price": coin.get('current_price', 0),
                "price_change_1h": coin.get('price_change_percentage_1h_in_currency', 0),
                "market_cap_rank": coin.get('market_cap_rank', 0)
            }
            for coin in top_gainers
        ],
        "losers": [
            {
                "id": coin.get('id', ''),
                "symbol": coin.get('symbol', '').upper(),
                "name": coin.get('name', ''),
                "image": coin.get('image', ''),
                "current_price": coin.get('current_price', 0),
                "price_change_1h": coin.get('price_change_percentage_1h_in_currency', 0),
                "market_cap_rank": coin.get('market_cap_rank', 0)
            }
            for coin in top_losers
        ]
    }
    
    return result


def save_to_json(data: Dict[str, Any], filename: str = "crypto_data.json") -> None:
    """
    Save processed data to JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")


def main():
    """Main execution function."""
    print("Fetching cryptocurrency data...")
    raw_data = fetch_crypto_data()
    
    if not raw_data:
        print("Failed to fetch data. Exiting.")
        return
    
    print(f"Fetched {len(raw_data)} cryptocurrencies")
    
    print("Processing data...")
    processed_data = process_crypto_data(raw_data)
    
    print(f"Top 10 gainers and losers identified")
    
    save_to_json(processed_data)
    print("Done!")


if __name__ == "__main__":
    main()

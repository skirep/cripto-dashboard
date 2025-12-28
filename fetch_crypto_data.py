#!/usr/bin/env python3
"""
Script to fetch cryptocurrency data from CoinGecko API.
Identifies top 10 gainers and losers in the last hour and saves to JSON.
Maintains historical tracking of cryptocurrencies with daily averages after 2 days.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
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


def load_historical_data(filename: str = "crypto_historical.json") -> Dict[str, Any]:
    """Load historical data from JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"cryptos": {}}


def save_historical_data(data: Dict[str, Any], filename: str = "crypto_historical.json") -> None:
    """Save historical data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string to datetime object."""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))


def update_historical_tracking(
    gainers: List[Dict[str, Any]], 
    losers: List[Dict[str, Any]], 
    timestamp: str
) -> Dict[str, Any]:
    """
    Update historical tracking for cryptocurrencies.
    - Track hourly data for each crypto
    - Mark as inactive if not in ranking for 2+ days
    - Calculate daily averages after 2 days
    - Keep data for maximum 10 days
    """
    historical = load_historical_data()
    cryptos = historical.get("cryptos", {})
    current_time = parse_timestamp(timestamp)
    two_days_ago = current_time - timedelta(days=2)
    cutoff_time = current_time - timedelta(days=10)
    
    # Get all currently ranked cryptos
    current_ranked = {}
    for crypto in gainers + losers:
        crypto_id = crypto['id']
        current_ranked[crypto_id] = {
            "id": crypto_id,
            "symbol": crypto['symbol'],
            "name": crypto['name'],
            "image": crypto['image'],
            "current_price": crypto['current_price'],
            "price_change_1h": crypto['price_change_1h'],
            "market_cap_rank": crypto['market_cap_rank'],
            "timestamp": timestamp
        }
    
    # Update or add cryptos
    for crypto_id, crypto_data in current_ranked.items():
        if crypto_id not in cryptos:
            # New crypto - initialize tracking
            cryptos[crypto_id] = {
                "info": {
                    "id": crypto_id,
                    "symbol": crypto_data['symbol'],
                    "name": crypto_data['name'],
                    "image": crypto_data['image']
                },
                "first_seen": timestamp,
                "last_seen": timestamp,
                "is_active": True,
                "hourly_data": [],
                "daily_averages": []
            }
        
        # Update last seen
        cryptos[crypto_id]["last_seen"] = timestamp
        cryptos[crypto_id]["is_active"] = True
        
        # Add hourly data point
        cryptos[crypto_id]["hourly_data"].append({
            "timestamp": timestamp,
            "price": crypto_data['current_price'],
            "change_1h": crypto_data['price_change_1h'],
            "market_cap_rank": crypto_data['market_cap_rank']
        })
    
    # Process all tracked cryptos
    for crypto_id, crypto_info in cryptos.items():
        last_seen = parse_timestamp(crypto_info['last_seen'])
        days_since_seen = (current_time - last_seen).total_seconds() / 86400
        
        # Mark as inactive if not seen for 2+ days
        if days_since_seen > 2:
            crypto_info["is_active"] = False
        
        # Clean up hourly data older than 10 days
        crypto_info["hourly_data"] = [
            point for point in crypto_info["hourly_data"]
            if parse_timestamp(point['timestamp']) > cutoff_time
        ]
        
        # Calculate daily averages for data older than 2 days
        first_seen = parse_timestamp(crypto_info['first_seen'])
        
        if (current_time - first_seen).total_seconds() > 2 * 86400:
            # Group hourly data by day
            daily_groups = {}
            for point in crypto_info["hourly_data"]:
                point_time = parse_timestamp(point['timestamp'])
                if point_time < two_days_ago:
                    day_key = point_time.strftime('%Y-%m-%d')
                    if day_key not in daily_groups:
                        daily_groups[day_key] = []
                    daily_groups[day_key].append(point)
            
            # Calculate averages for each day
            new_daily_averages = []
            for day, points in sorted(daily_groups.items()):
                if points:
                    avg_price = sum(p['price'] for p in points) / len(points)
                    avg_change = sum(p['change_1h'] for p in points) / len(points)
                    new_daily_averages.append({
                        "date": day,
                        "avg_price": avg_price,
                        "avg_change_1h": avg_change,
                        "num_samples": len(points)
                    })
            
            crypto_info["daily_averages"] = new_daily_averages
            
            # Remove hourly data points that are now in daily averages
            crypto_info["hourly_data"] = [
                point for point in crypto_info["hourly_data"]
                if parse_timestamp(point['timestamp']) >= two_days_ago
            ]
    
    historical["cryptos"] = cryptos
    return historical


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
    last_updated = ''
    if data:
        # Try to find the most recent timestamp
        for coin in data[:10]:  # Check first 10 coins
            if coin.get('last_updated'):
                last_updated = coin.get('last_updated')
                break
    
    gainers_list = [
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
    ]
    
    losers_list = [
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
    
    # Update historical tracking
    historical = update_historical_tracking(gainers_list, losers_list, last_updated)
    
    # Get all tracked cryptos with their latest data
    tracked_cryptos = []
    for crypto_id, crypto_info in historical['cryptos'].items():
        latest_data = None
        
        # Get most recent data point
        if crypto_info.get('hourly_data'):
            latest_hourly = crypto_info['hourly_data'][-1]
            latest_data = {
                "price": latest_hourly['price'],
                "change_1h": latest_hourly['change_1h'],
                "market_cap_rank": latest_hourly['market_cap_rank'],
                "data_type": "hourly"
            }
        elif crypto_info.get('daily_averages'):
            latest_daily = crypto_info['daily_averages'][-1]
            latest_data = {
                "price": latest_daily['avg_price'],
                "change_1h": latest_daily['avg_change_1h'],
                "market_cap_rank": None,
                "data_type": "daily_average"
            }
        
        if latest_data:
            tracked_cryptos.append({
                "id": crypto_info['info']['id'],
                "symbol": crypto_info['info']['symbol'],
                "name": crypto_info['info']['name'],
                "image": crypto_info['info']['image'],
                "current_price": latest_data['price'],
                "price_change_1h": latest_data['change_1h'],
                "market_cap_rank": latest_data['market_cap_rank'],
                "is_active": crypto_info['is_active'],
                "data_type": latest_data['data_type']
            })
    
    # Save historical data
    save_historical_data(historical)
    
    result = {
        "last_updated": last_updated,
        "gainers": gainers_list,
        "losers": losers_list,
        "tracked_cryptos": tracked_cryptos
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

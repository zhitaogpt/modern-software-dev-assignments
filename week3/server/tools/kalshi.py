import httpx
import json
from typing import List, Dict, Any

# Kalshi Public API Endpoint
KALSHI_API_URL = "https://api.elections.kalshi.com/trade-api/v2"

import httpx
import json
import time
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi

# Kalshi Public API Endpoint
KALSHI_API_URL = "https://api.elections.kalshi.com/trade-api/v2"

# In-memory cache
_MARKET_CACHE = {
    "data": [],
    "timestamp": 0.0
}
CACHE_TTL = 300  # 5 minutes

def simple_tokenize(text: str) -> List[str]:
    """
    Simple tokenizer that splits by whitespace and removes non-alphanumeric chars.
    """
    return [word.lower() for word in text.split()]

async def _get_all_markets(limit: int = 1000) -> List[Dict[str, Any]]:
    """Helper to get all open markets with caching."""
    global _MARKET_CACHE
    current_time = time.time()
    
    if _MARKET_CACHE["data"] and (current_time - _MARKET_CACHE["timestamp"] < CACHE_TTL):
        return _MARKET_CACHE["data"]
        
    fetch_params = {"limit": limit, "status": "open"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{KALSHI_API_URL}/markets", params=fetch_params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            markets = data.get("markets", [])
            
            # Update cache
            _MARKET_CACHE = {
                "data": markets,
                "timestamp": current_time
            }
            return markets
        except Exception as e:
            print(f"Error fetching Kalshi markets: {e}")
            return []

async def search_markets(query: str = "", limit: int = 10) -> str:
    """
    Search for markets on Kalshi using BM25 ranking.
    """
    all_markets = await _get_all_markets()
    
    if not all_markets:
        return json.dumps({"error": "No market data available."}, ensure_ascii=False)

    # 1. If query is empty, just return trending by volume
    if not query.strip():
        sorted_by_volume = sorted(all_markets, key=lambda x: x.get("volume", 0) or 0, reverse=True)
        return _format_results(sorted_by_volume[:limit])

    # 2. Use BM25 for search
    # Prepare corpus: combine relevant fields into a single text for each market
    corpus = []
    for m in all_markets:
        # Give more weight to Title by repeating it? Or just combine fields.
        text = f"{m.get('title', '')} {m.get('ticker', '')} {m.get('category', '')} {m.get('subtitle', '')}"
        corpus.append(simple_tokenize(text))

    tokenized_query = simple_tokenize(query)
    bm25 = BM25Okapi(corpus)
    
    # Get top N documents
    # get_top_n returns the actual documents (lists of tokens)
    # But we need the indices to get the original market objects.
    # So we use get_scores and sort manually.
    scores = bm25.get_scores(tokenized_query)
    
    # Pair scores with markets
    scored_markets = []
    for i, score in enumerate(scores):
        if score > 0: # Only include relevant results
            scored_markets.append((score, all_markets[i]))
            
    # Sort by score desc
    scored_markets.sort(key=lambda x: x[0], reverse=True)
    
    top_markets = [item[1] for item in scored_markets[:limit]]
    
    if not top_markets:
         return json.dumps({"message": f"No active markets found matching '{query}'."}, ensure_ascii=False)

    return _format_results(top_markets)

def _format_results(markets: List[Dict[str, Any]]) -> str:
    """Helper to format the output JSON."""
    results = []
    for m in markets:
        price = m.get("last_price", 0)
        prob = f"{price}¢" if price else "N/A"
        results.append({
            "ticker": m.get("ticker"),
            "title": m.get("title"),
            "price": prob,
            "volume": m.get("volume"),
            "yes_bid": m.get("yes_bid"),
            "yes_ask": m.get("yes_ask"),
            "close_time": m.get("close_time")
        })
    return json.dumps(results, ensure_ascii=False, indent=2)

async def get_market_details(ticker: str) -> str:
    """
    Get detailed data for a specific market by Ticker.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{KALSHI_API_URL}/markets/{ticker}", timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # The structure might be nested under 'market'
            market = data.get("market", data)
            
            return json.dumps(market, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Kalshi details failed: {str(e)}"})

import httpx  # for asynchronous HTTP requests to fetch market news data

# this function is using for the get the current market data for the given sector.
async def fetch_market_news(sector: str):
    return f"Latest market trends, regulatory updates, and trade news for the {sector} sector in India for 2026."
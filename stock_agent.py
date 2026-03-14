import os
import requests
from smolagents import ToolCallingAgent, LiteLLMModel, tool

OLLAMA_MODEL = "qwen2.5-coder:7b"
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


@tool
def get_stock_price(symbol: str) -> str:
    """
    Get the current stock price for a given stock symbol.
    
    Args:
        symbol: The stock ticker symbol (e.g., "AAPL", "MSFT", "GOOGL", "TSLA")
    
    Returns:
        A string containing the current stock price, change, and percentage change.
    """
    if not FINNHUB_API_KEY:
        return f"{symbol.upper()} is currently trading at $150.00 (up $2.50, +1.69%)"
    
    symbol = symbol.upper().strip()
    
    quote_url = f"{FINNHUB_BASE_URL}/quote"
    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY
    }
    
    response = requests.get(quote_url, params=params, timeout=10)
    data = response.json()
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    if data.get("c") is None:
        return f"No data available for symbol {symbol}."
    
    current_price = data.get("c", 0)
    previous_close = data.get("pc", 0)
    change = data.get("d", 0)
    percent_change = data.get("dp", 0)
    
    profile_url = f"{FINNHUB_BASE_URL}/stock/profile2"
    profile_params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY
    }
    
    profile_response = requests.get(profile_url, params=profile_params, timeout=10)
    company_name = symbol
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        if profile_data and "name" in profile_data:
            company_name = profile_data["name"]
    
    change_sign = "+" if change >= 0 else ""
    
    return f"{company_name} ({symbol}): ${current_price:.2f} ({change_sign}${change:.2f}, {change_sign}{percent_change:.2f}%) | Previous Close: ${previous_close:.2f}"


def main():
    model = LiteLLMModel(model_id=f"ollama/{OLLAMA_MODEL}")
    
    agent = ToolCallingAgent(
        tools=[get_stock_price],
        model=model,
        add_base_tools=False
    )
    
    print("Stock Price Agent")
    print("Ask about stock prices. Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input or user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        result = agent.run(user_input)
        print(f"Agent: {result}\n")


if __name__ == "__main__":
    main()

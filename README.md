# Stock-AI-Agent

A conversational stock price agent powered by **smolagents** and **Ollama**. Ask questions in natural language (e.g. “What’s Apple’s stock price?”) and get live quotes via the Finnhub API.

## Features

- **Natural language** – Ask about any stock by name or ticker (e.g. AAPL, MSFT, GOOGL, TSLA).
- **Live data** – Uses [Finnhub](https://finnhub.io) for current price, change, percent change, and previous close.
- **Local LLM** – Runs with Ollama (default model: `qwen2.5-coder:7b`) so you can keep everything on your machine.

## Prerequisites

- **Python 3.8+**
- **Ollama** – [Install Ollama](https://ollama.ai), then pull the model:
  ```bash
  ollama pull qwen2.5-coder:7b
  ```
- **Finnhub API key** – Free tier is enough for development (see below).

## Environment variables

Create a `.env` file in the project root (or set these in your shell). **Do not commit `.env`** — add it to `.gitignore`.

| Variable           | Required | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `FINNHUB_API_KEY`  | Yes*     | API key from Finnhub for real-time stock quotes. |

\*If `FINNHUB_API_KEY` is missing, the agent still runs but returns placeholder data for demo purposes.

### Example `.env`

```env
FINNHUB_API_KEY=your_finnhub_api_key_here
```

## Getting your Finnhub API key

1. Go to [Finnhub](https://finnhub.io).
2. Sign up (free) or log in.
3. Open **Dashboard** (or [API Keys](https://finnhub.io/dashboard)).
4. Copy your **API key**.
5. Paste it into `.env` as `FINNHUB_API_KEY=...`.

Free tier includes a generous number of API calls per minute; no credit card needed for basic use.

## Installation

1. Clone the repo and go into the project folder:
   ```bash
   cd Stock-AI-Agent
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install smolagents requests
   ```

4. Ensure Ollama is running and the model is pulled:
   ```bash
   ollama serve
   ollama pull qwen2.5-coder:7b
   ```

## Usage

1. Set your environment (e.g. load `.env` or export `FINNHUB_API_KEY`).
2. Run the agent:
   ```bash
   python stock_agent.py
   ```
3. Type your questions and press Enter. Type `quit`, `exit`, or `q` to exit.

Example prompts:

- “What’s the stock price for AAPL?”
- “How is Tesla (TSLA) doing?”
- “Get me the price of Microsoft.”

## Project structure

- `stock_agent.py` – Main script: defines the `get_stock_price` tool, wires it to the smolagents `ToolCallingAgent`, and runs the chat loop with Ollama.

## License

Use and modify as you like. Finnhub and Ollama have their own terms; ensure your usage complies with them.

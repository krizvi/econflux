from strands import tool
import datetime as dt
import random
from typing import Any, Dict


def _normalize_ticker(ticker: str) -> dict:
    """
    Convert raw ticker input into a normalized dict with mock data.
    """
    t = ticker.upper()

    # generate random but realistic numbers
    current = round(random.uniform(50, 500), 2)
    previous = round(current * random.uniform(0.97, 0.999), 2)

    return {
        "symbol": t,
        "currentPrice": current,
        "previousClose": previous,
        "currency": "USD",
        "exchange": "NASDAQ",
    }


@tool
def get_stock_price(ticker: str) -> Dict[str, Any]:
    """
    Return a mock latest stock quote (price, currency, previous close, exchange).

    Use when you need an example quote without calling real market data. Values are
    randomly generated per call and unsuitable for trading/analysis.

    Args:
        ticker: Stock symbol (case-insensitive). It is uppercased for the response.

    Returns:
        Dict with:
        - ticker: Uppercased symbol
        - price: Mock latest price (float)
        - currency: Quotation currency (string)
        - previous_close: Mock previous close (float)
        - exchange: Mock exchange code (string)
        - timestamp: ISO-8601 UTC timestamp with trailing "Z"

    Notes:
        - Values are synthetic and change on every call
        - No external APIs are contacted; this is a local mock
    """
    quote = _normalize_ticker(ticker)

    return {
        "ticker": quote["symbol"],
        "price": quote["currentPrice"],
        "currency": quote["currency"],
        "previous_close": quote["previousClose"],
        "exchange": quote["exchange"],
        "timestamp": dt.datetime.utcnow().isoformat() + "Z",
    }


@tool
def get_price_history(
    ticker: str, period: str = "5d", interval: str = "1d"
) -> Dict[str, Any]:
    """
    Return a mock OHLCV (Open, High, Low, Close, Volume) history with five synthetic periods.

    Use for placeholder history when real data is unavailable. `period` and `interval`
    are informational only; five entries are always generated to keep payloads small.

    Args:
        ticker: Stock symbol (case-insensitive). It is uppercased for the response.
        period: Label for the requested period (informational only).
        interval: Label for the requested interval (informational only).

    Returns:
        Dict with:
        - ticker: Uppercased symbol
        - period: Echoed input period
        - interval: Echoed input interval
        - history: Mapping of period keys to OHLCV fields (open, high, low, close, volume)

    Notes:
        - All values are randomly generated and will differ on each call
        - Exactly five entries are returned to simplify downstream handling
    """
    t = ticker.upper()

    # Produce 5 random daily candles
    history = {}
    for i in range(5):
        base = round(random.uniform(50, 500), 2)
        history_key = f"day_{i + 1}"

        history[history_key] = {
            "open": base,
            "high": round(base * random.uniform(1.00, 1.03), 2),
            "low": round(base * random.uniform(0.97, 1.00), 2),
            "close": round(base * random.uniform(0.98, 1.02), 2),
            "volume": random.randint(1_000_000, 5_000_000),
        }

    return {
        "ticker": t,
        "period": period,
        "interval": interval,
        "history": history,
    }


@tool
def get_earnings(ticker: str) -> Dict[str, Any]:
    """
    Return a mock earnings snapshot and next earnings date for a ticker.

    Use for placeholder fundamentals without hitting external services. All values are
    synthetic and intended for demos/testing.

    Args:
        ticker: Stock symbol (case-insensitive). It is uppercased for the response.

    Returns:
        Dict with:
        - ticker: Uppercased symbol
        - calendar: {next_earnings_date: ISO date string}
        - earnings: {eps_actual, eps_estimate, revenue_actual, revenue_estimate}

    Notes:
        - Values are synthetic and change on every call
        - Calendar dates are forward-looking but not linked to real schedules
    """
    t = ticker.upper()

    earnings = {
        "eps_actual": round(random.uniform(0.5, 4.0), 2),
        "eps_estimate": round(random.uniform(0.5, 4.0), 2),
        "revenue_actual": random.randint(5_000_000_000, 50_000_000_000),
        "revenue_estimate": random.randint(5_000_000_000, 50_000_000_000),
    }

    calendar = {
        "next_earnings_date": (
            dt.datetime.utcnow() + dt.timedelta(days=random.randint(10, 60))
        )
        .date()
        .isoformat()
    }

    return {
        "ticker": t,
        "calendar": calendar,
        "earnings": earnings,
    }


@tool
def generate_stock_report(ticker: str, period: str = "5d") -> Dict[str, Any]:
    """
    Generate a compact mock stock report combining quote, history, and earnings.

    Use when you want one payload summarizing the mock market data tools
    (`get_stock_price`, `get_price_history`, `get_earnings`).

    Args:
        ticker: Stock symbol (case-insensitive). It is uppercased for the response.
        period: Label passed through to `get_price_history` to tag the history payload.

    Returns:
        Dict with:
        - ticker: Uppercased symbol
        - summary: Latest price, previous close, currency, exchange
        - history: OHLCV series from `get_price_history`
        - earnings: Earnings fields from `get_earnings`
        - calendar: Next earnings date from `get_earnings`
        - generated_at: ISO-8601 UTC timestamp with trailing "Z"

    Notes:
        - All values are synthetic and differ per call
        - Because each mock is invoked once per request, values stay internally consistent
          within a single response but not across separate invocations
    """
    price = get_stock_price(ticker)
    history = get_price_history(ticker, period=period)
    earnings = get_earnings(ticker)

    return {
        "ticker": ticker.upper(),
        "summary": {
            "latest_price": price["price"],
            "previous_close": price["previous_close"],
            "currency": price["currency"],
            "exchange": price["exchange"],
        },
        "history": history["history"],
        "earnings": earnings["earnings"],
        "calendar": earnings["calendar"],
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
    }

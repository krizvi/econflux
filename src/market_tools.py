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
    Return the latest stock price along with currency and previous close.
    (Mock implementation using random data.)
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
    Return mock OHLCV series for a ticker.
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
    Return mock earnings calendar and earnings fields.
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
    Generate a compact stock report combining mock latest price, history, and earnings snapshot.
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

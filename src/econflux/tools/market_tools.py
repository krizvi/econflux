from strands import tool

import datetime as dt
from typing import Any, Dict

import yfinance as yf


def _normalize_ticker(ticker: str) -> yf.Ticker:
    """
    Internal helper to construct and validate a yfinance Ticker instance.
    """
    normalized_ticker = ticker.strip().upper()
    print(f"Passed in ticker: {ticker}: Normalized Ticker:{normalized_ticker}")
    if not normalized_ticker:
        raise ValueError("Ticker symbol must not be empty.")
    return yf.Ticker(normalized_ticker)


@tool
def get_stock_price(ticker: str) -> Dict[str, Any]:
    """
    Return the latest stock price along with currency and previous close.
    """
    t = _normalize_ticker(ticker)
    info = t.info  # yfinance dict
    return {
        "ticker": ticker.upper(),
        "price": info.get("currentPrice"),
        "currency": info.get("currency"),
        "previous_close": info.get("previousClose"),
        "exchange": info.get("exchange"),
        "timestamp": dt.datetime.now().isoformat() + "Z",
    }


@tool
def get_price_history(
    ticker: str, period: str = "5d", interval: str = "1d"
) -> Dict[str, Any]:
    """
    Return historical OHLCV series for a ticker over the given period and interval.
    """
    t = _normalize_ticker(ticker)
    hist = t.history(period=period, interval=interval)
    return {
        "ticker": ticker.upper(),
        "period": period,
        "interval": interval,
        "history": hist.to_dict(orient="index"),
    }


@tool
def get_earnings(ticker: str) -> Dict[str, Any]:
    """
    Return earnings calendar and basic earnings-related fields for a ticker.
    """
    t = _normalize_ticker(ticker)
    calendar = getattr(t, "calendar", None)
    earnings = getattr(t, "earnings", None)
    return {
        "ticker": ticker.upper(),
        "calendar": calendar.to_dict() if calendar is not None else None,
        "earnings": earnings.to_dict() if earnings is not None else None,
    }


@tool
def generate_stock_report(ticker: str, period: str = "5d") -> Dict[str, Any]:
    """
    Generate a compact stock report combining latest price, recent history, and earnings snapshot.
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

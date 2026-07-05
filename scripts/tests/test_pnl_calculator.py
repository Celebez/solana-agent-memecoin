"""Test pnl_calculator.py — FIFO P&L calculation."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pnl_calculator


def test_fifo_pnl_simple_profit():
    """Buy then sell higher = profit."""
    trades = [
        {"timestamp": "2026-07-01T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "buy", "amount": 100, "price_usd": 1.0, "fee_usd": 0.0},
        {"timestamp": "2026-07-02T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "sell", "amount": 100, "price_usd": 2.0, "fee_usd": 0.0},
    ]
    results = pnl_calculator.fifo_pnl(trades)
    assert results["M1"]["realized_pnl"] == 100.0  # Bought at $1, sold at $2 = +$100
    assert results["M1"]["position_amount"] == 0


def test_fifo_pnl_loss():
    """Buy then sell lower = loss."""
    trades = [
        {"timestamp": "2026-07-01T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "buy", "amount": 100, "price_usd": 2.0, "fee_usd": 0.0},
        {"timestamp": "2026-07-02T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "sell", "amount": 100, "price_usd": 1.0, "fee_usd": 0.0},
    ]
    results = pnl_calculator.fifo_pnl(trades)
    assert results["M1"]["realized_pnl"] == -100.0


def test_fifo_pnl_partial_sell():
    """Sell partial position = remaining lot tracked."""
    trades = [
        {"timestamp": "2026-07-01T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "buy", "amount": 100, "price_usd": 1.0, "fee_usd": 0.0},
        {"timestamp": "2026-07-02T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "sell", "amount": 40, "price_usd": 2.0, "fee_usd": 0.0},
    ]
    results = pnl_calculator.fifo_pnl(trades)
    assert results["M1"]["realized_pnl"] == 40.0  # 40 * (2-1) = 40
    assert results["M1"]["position_amount"] == 60  # 100 - 40 remaining


def test_fifo_pnl_multiple_lots():
    """FIFO tracks multiple buy lots."""
    trades = [
        {"timestamp": "2026-07-01T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "buy", "amount": 50, "price_usd": 1.0, "fee_usd": 0.0},
        {"timestamp": "2026-07-02T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "buy", "amount": 50, "price_usd": 3.0, "fee_usd": 0.0},
        {"timestamp": "2026-07-03T10:00:00Z", "symbol": "TOK", "mint": "M1",
         "side": "sell", "amount": 50, "price_usd": 5.0, "fee_usd": 0.0},
    ]
    results = pnl_calculator.fifo_pnl(trades)
    # First lot: 50 * (5 - 1) = 200
    assert results["M1"]["realized_pnl"] == 200.0
    assert results["M1"]["position_amount"] == 50  # second lot remains


def test_empty_trades():
    """Empty trade list returns empty dict."""
    results = pnl_calculator.fifo_pnl([])
    assert results == {}

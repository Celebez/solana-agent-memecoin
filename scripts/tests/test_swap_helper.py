"""Test swap_helper.py — quote parsing & formatting."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import swap_helper


def test_token_label_unknown():
    """Unknown mint returns shortened version (deterministic, no network)."""
    import swap_helper
    swap_helper._token_cache = {}  # force empty cache
    mint = "UnknownMintAddress12345678901234567890"
    label = swap_helper.token_label(mint)
    # Format: mint[:6] + "..." + mint[-4:]
    expected = mint[:6] + "..." + mint[-4:]
    assert label == expected, f"Expected {expected!r}, got {label!r}"


def test_format_quote_empty():
    """Empty quote returns error message."""
    msg = swap_helper.format_quote({}, "input", "output")
    assert "❌" in msg


def test_format_quote_valid():
    """Valid quote formats correctly."""
    quote = {
        "inAmount": "1000000000",
        "outAmount": "100000000",
        "priceImpactPct": "0.01",
        "routePlan": [{"swapInfo": {"label": "Raydium"}}],
    }
    msg = swap_helper.format_quote(quote, "So11111111111111111111111111111111111111112", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    assert "INPUT" in msg
    assert "OUTPUT" in msg
    assert "PRICE IMPACT" in msg
    assert "Raydium" in msg

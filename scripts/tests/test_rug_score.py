"""Test rug_score.py — composite scoring logic."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# We mock the network calls
import rug_score


def test_score_token_with_all_safe(monkeypatch):
    """All checks pass → score >= 80."""
    def mock_rpc(method, params):
        if method == "getAccountInfo":
            return {"value": {"data": {"parsed": {"info": {
                "mintAuthority": None,
                "freezeAuthority": None,
                "supply": "1000000000000",
            }}}}}
        if method == "getTokenLargestAccounts":
            return {"value": [
                {"uiAmount": 100_000_000},  # 10%
                {"uiAmount": 100_000_000},
                {"uiAmount": 100_000_000},
                {"uiAmount": 50_000_000},
            ] * 3}  # total 1B, top 10 = ~20%
        return {}

    def mock_dex(mint):
        return {
            "liquidity": {"usd": 100_000},
            "volume": {"h24": 50_000},
        }

    monkeypatch.setattr(rug_score, "_rpc", mock_rpc)
    monkeypatch.setattr(rug_score, "_dex", mock_dex)

    result = rug_score.score_token("dummy_mint")
    assert result["score"] >= 80
    assert "AMAN" in result["verdict"]


def test_score_token_with_active_authorities(monkeypatch):
    """Mint authority aktif → score rendah."""
    def mock_rpc(method, params):
        if method == "getAccountInfo":
            return {"value": {"data": {"parsed": {"info": {
                "mintAuthority": "SomeActivePubkey",
                "freezeAuthority": "SomeActivePubkey",
                "supply": "1000000000000",
            }}}}}
        if method == "getTokenLargestAccounts":
            return {"value": [{"uiAmount": 900_000_000}]}  # 1 holder 90%
        return {}

    def mock_dex(mint):
        return {"liquidity": {"usd": 1_000}, "volume": {"h24": 100}}

    monkeypatch.setattr(rug_score, "_rpc", mock_rpc)
    monkeypatch.setattr(rug_score, "_dex", mock_dex)

    result = rug_score.score_token("dummy_mint")
    assert result["score"] < 40
    assert "TINGGI" in result["verdict"] or "JANGAN" in result["verdict"]


def test_score_token_handles_empty(monkeypatch):
    """Empty data → score very low, no crash."""
    def mock_rpc(method, params):
        return {}

    def mock_dex(mint):
        return {}

    monkeypatch.setattr(rug_score, "_rpc", mock_rpc)
    monkeypatch.setattr(rug_score, "_dex", mock_dex)

    result = rug_score.score_token("nonexistent_mint")
    assert "score" in result
    assert "verdict" in result

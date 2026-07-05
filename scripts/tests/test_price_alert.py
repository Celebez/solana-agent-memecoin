"""Test price_alert.py — alert detection logic."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import price_alert


def test_check_alert_above_triggered(monkeypatch):
    """Alert fires when price >= above target."""
    monkeypatch.setattr(price_alert, "get_price", lambda mint: 0.0015)
    msg = price_alert.check_alert({
        "mint": "dummy", "label": "TEST",
        "above": 0.001, "below": None
    })
    assert msg is not None
    assert "ABOVE" in msg
    assert "TEST" in msg


def test_check_alert_below_triggered(monkeypatch):
    """Alert fires when price <= below target."""
    monkeypatch.setattr(price_alert, "get_price", lambda mint: 0.0003)
    msg = price_alert.check_alert({
        "mint": "dummy", "label": "TEST",
        "above": None, "below": 0.0005
    })
    assert msg is not None
    assert "BELOW" in msg


def test_check_alert_no_trigger(monkeypatch):
    """No alert when price within range."""
    monkeypatch.setattr(price_alert, "get_price", lambda mint: 0.0007)
    msg = price_alert.check_alert({
        "mint": "dummy", "label": "TEST",
        "above": 0.001, "below": 0.0005
    })
    assert msg is None


def test_check_alert_handles_zero_price(monkeypatch):
    """No alert when price fetch fails (returns 0)."""
    monkeypatch.setattr(price_alert, "get_price", lambda mint: 0.0)
    msg = price_alert.check_alert({
        "mint": "dummy", "label": "TEST",
        "above": 0.001, "below": None
    })
    assert msg is None


def test_detect_webhook_type():
    """Webhook type detection."""
    assert price_alert.detect_webhook_type("https://discord.com/api/webhooks/xxx") == "discord"
    assert price_alert.detect_webhook_type("https://api.telegram.org/bot/xxx") == "telegram"
    assert price_alert.detect_webhook_type("https://example.com") == "discord"  # default

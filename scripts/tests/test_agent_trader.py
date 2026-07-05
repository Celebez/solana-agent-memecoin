"""Test agent_trader.py — guardrails, strategy logic, state persistence."""
import sys, os, json, tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import agent_trader


# ============================================================
# Fixtures
# ============================================================
def setup_function(function):
    """Redirect state files to tempdir."""
    tmp = Path(tempfile.mkdtemp())
    agent_trader.STATE_DIR = tmp
    agent_trader.STATE_FILE = tmp / "agent_state.json"
    agent_trader.PAUSE_FILE = tmp / ".agent_paused"


def make_config(**overrides):
    """Create test config from conservative preset."""
    cfg = dict(agent_trader.STRATEGIES["conservative"])
    cfg.update(overrides)
    return cfg


def make_token(**overrides):
    """Create test token."""
    token = {
        "mint": "TokenMint111111111111111111111111111111",
        "symbol": "TEST",
        "liquidity_usd": 100_000,
        "volume_24h": 50_000,
        "market_cap": 500_000,
        "price_usd": 0.001,
        "price_change_24h": 5.0,
        "pair_age_ms": int(datetime.utcnow().timestamp() * 1000) - 3600_000,
        "url": "https://dexscreener.com/solana/test",
    }
    token.update(overrides)
    return token


def make_state(capital=1000):
    """Create fresh agent state."""
    return agent_trader.AgentState(capital=capital)


# ============================================================
# Strategy logic
# ============================================================
def test_should_buy_rug_score_pass():
    """Buy when rug score passes threshold."""
    state = make_state()
    config = make_config(min_rug_score=70)
    token = make_token()
    should, size, reason = agent_trader.should_buy(token, 85, state, config)
    assert should is True
    assert size == 50.0  # 5% of 1000
    assert "All checks passed" in reason


def test_should_buy_rug_score_fail():
    """Reject when rug score too low."""
    state = make_state()
    config = make_config(min_rug_score=70)
    token = make_token()
    should, size, reason = agent_trader.should_buy(token, 50, state, config)
    assert should is False
    assert size == 0
    assert "Rug score" in reason


def test_should_buy_liquidity_fail():
    """Reject when liquidity too low."""
    state = make_state()
    config = make_config(min_liquidity_usd=50_000)
    token = make_token(liquidity_usd=10_000)
    should, _, reason = agent_trader.should_buy(token, 85, state, config)
    assert should is False
    assert "Liquidity" in reason


def test_should_buy_volume_fail():
    """Reject when volume too low."""
    state = make_state()
    config = make_config(min_volume_24h=10_000)
    token = make_token(volume_24h=1_000)
    should, _, reason = agent_trader.should_buy(token, 85, state, config)
    assert should is False
    assert "Volume" in reason


def test_should_buy_already_in_position():
    """Reject when already holding this token."""
    state = make_state()
    token = make_token()
    state.positions[token["mint"]] = {"entry_price": 0.001, "amount_usd": 50, "entry_time": "now"}
    config = make_config()
    should, _, reason = agent_trader.should_buy(token, 85, state, config)
    assert should is False
    assert "Already in position" in reason


def test_should_buy_max_positions_reached():
    """Reject when max open positions reached."""
    state = make_state()
    config = make_config(max_open_positions=2)
    # Fill positions
    state.positions["mint1"] = {"entry_price": 1, "amount_usd": 10, "entry_time": "now"}
    state.positions["mint2"] = {"entry_price": 1, "amount_usd": 10, "entry_time": "now"}
    token = make_token(mint="newtoken")
    should, _, reason = agent_trader.should_buy(token, 85, state, config)
    assert should is False
    assert "Max open positions" in reason


def test_should_buy_cooldown_active():
    """Reject during cooldown period."""
    state = make_state()
    config = make_config(cooldown_seconds=300)
    state.last_trade_time = datetime.utcnow() - timedelta(seconds=10)
    token = make_token()
    should, _, reason = agent_trader.should_buy(token, 85, state, config)
    assert should is False
    assert "Cooldown" in reason


def test_should_buy_cooldown_expired():
    """Allow trade after cooldown."""
    state = make_state()
    config = make_config(cooldown_seconds=300)
    state.last_trade_time = datetime.utcnow() - timedelta(seconds=400)
    token = make_token()
    should, size, _ = agent_trader.should_buy(token, 85, state, config)
    assert should is True


# ============================================================
# Sell logic — stop loss & take profit
# ============================================================
def test_should_sell_stop_loss_triggered():
    """Sell when price drops below stop loss threshold."""
    state = make_state()
    config = make_config(stop_loss_pct=30)
    state.positions["mint"] = {"entry_price": 1.0, "amount_usd": 100, "entry_time": "now"}
    should, reason = agent_trader.should_sell("mint", 0.6, state, config)  # -40%
    assert should is True
    assert "STOP LOSS" in reason


def test_should_sell_take_profit_triggered():
    """Sell when price rises above take profit threshold."""
    state = make_state()
    config = make_config(take_profit_pct=100)
    state.positions["mint"] = {"entry_price": 1.0, "amount_usd": 100, "entry_time": "now"}
    should, reason = agent_trader.should_sell("mint", 2.5, state, config)  # +150%
    assert should is True
    assert "TAKE PROFIT" in reason


def test_should_sell_hold():
    """Hold when price within range."""
    state = make_state()
    config = make_config(stop_loss_pct=30, take_profit_pct=100)
    state.positions["mint"] = {"entry_price": 1.0, "amount_usd": 100, "entry_time": "now"}
    should, reason = agent_trader.should_sell("mint", 1.2, state, config)  # +20%
    assert should is False
    assert "Hold" in reason


def test_should_sell_no_position():
    """No action if no position."""
    state = make_state()
    config = make_config()
    should, reason = agent_trader.should_sell("mint", 1.0, state, config)
    assert should is False
    assert "No position" in reason


# ============================================================
# State persistence
# ============================================================
def test_state_save_load(tmp_path=None):
    """State persists across AgentState instances."""
    state1 = agent_trader.AgentState(capital=500)
    state1.positions["test_mint"] = {"entry_price": 1.0, "amount_usd": 50, "entry_time": "now"}
    state1.save()

    # Load in new instance
    state2 = agent_trader.AgentState(capital=1000)  # capital overridden by saved
    assert state2.capital == 500
    assert "test_mint" in state2.positions


def test_state_record_trade():
    """Trade recording works."""
    state = make_state()
    state.record_trade("mint", "buy", 50.0, 1.0, "test reason")
    assert len(state.trade_log) == 1
    assert state.trade_log[0]["side"] == "buy"
    assert state.trade_log[0]["amount_usd"] == 50.0


def test_state_daily_pnl_reset():
    """Daily P&L resets on new day."""
    state = make_state()
    state.daily_pnl = -100.0
    state.daily_reset_date = (datetime.utcnow() - timedelta(days=1)).date()
    state.reset_daily_pnl()
    assert state.daily_pnl == 0.0


def test_state_pause_file_check(tmp_path=None):
    """Pause file detection works."""
    state = make_state()
    assert state.paused is False
    agent_trader.PAUSE_FILE.touch()
    state.check_pause_file()
    assert state.paused is True
    agent_trader.PAUSE_FILE.unlink()
    state.check_pause_file()
    assert state.paused is False


# ============================================================
# Strategy presets
# ============================================================
def test_all_strategies_defined():
    """All expected strategy presets exist."""
    expected = {"ultra_safe", "conservative", "moderate", "aggressive", "yolo"}
    assert set(agent_trader.STRATEGIES.keys()) == expected


def test_yolo_most_aggressive():
    """YOLO has highest max_position_pct."""
    yolo_pos = agent_trader.STRATEGIES["yolo"]["max_position_pct"]
    ultra_pos = agent_trader.STRATEGIES["ultra_safe"]["max_position_pct"]
    assert yolo_pos > ultra_pos


def test_ultra_safe_tightest_guards():
    """Ultra-safe has tightest stop loss."""
    ultra_sl = agent_trader.STRATEGIES["ultra_safe"]["stop_loss_pct"]
    yolo_sl = agent_trader.STRATEGIES["yolo"]["stop_loss_pct"]
    assert ultra_sl < yolo_sl

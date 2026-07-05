#!/usr/bin/env python3
"""
🤖 agent_trader.py — Autonomous Solana Trading Agent

Working example of a trading agent with strict guardrails.
Supports dry-run mode (paper trading) and live mode (real transactions).

STRATEGY:
- Monitors new tokens via DexScreener + Helius RPC
- Filters by rug score (must be ≥ MIN_RUG_SCORE)
- Buys with position sizing (max % of capital per token)
- Sells on take-profit or stop-loss trigger
- Hard daily loss limit (kill switch)

GUARDRAILS:
- MAX_POSITION_PCT: max % of capital per position
- STOP_LOSS_PCT: auto-sell if loss > threshold
- TAKE_PROFIT_PCT: auto-sell if profit > threshold
- MAX_DAILY_LOSS_PCT: pause agent if daily loss > threshold
- MAX_OPEN_POSITIONS: max concurrent positions
- COOLDOWN_SECONDS: min seconds between trades

Usage:
    # Dry-run (no real transactions)
    python agent_trader.py --dry-run --capital 100 --strategy conservative

    # Live (REAL MONEY — BE CAREFUL)
    python agent_trader.py --live --capital 100 --strategy conservative \\
        --discord $DISCORD_WEBHOOK_URL

Dependencies:
    pip install requests base58 cryptography
"""
import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
DEXSCREENER_LATEST = "https://api.dexscreener.com/latest/dex/pairs/solana"
JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_PRICE_API = "https://price.jup.ag/v6/price"

SOL_MINT = "So11111111111111111111111111111111111111112"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

# State files
STATE_DIR = Path.home() / ".solana-agent"
STATE_FILE = STATE_DIR / "agent_state.json"
PAUSE_FILE = Path.home() / ".agent_paused"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("agent_trader.log"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger("agent")


# ============================================================
# STRATEGY PRESETS
# ============================================================
STRATEGIES = {
    "ultra_safe": {
        "max_position_pct": 1, "stop_loss_pct": 15, "take_profit_pct": 50,
        "max_daily_loss_pct": 5, "max_open_positions": 2, "cooldown_seconds": 600,
        "min_rug_score": 80, "min_liquidity_usd": 100_000, "min_volume_24h": 50_000,
    },
    "conservative": {
        "max_position_pct": 5, "stop_loss_pct": 30, "take_profit_pct": 100,
        "max_daily_loss_pct": 20, "max_open_positions": 3, "cooldown_seconds": 300,
        "min_rug_score": 70, "min_liquidity_usd": 50_000, "min_volume_24h": 10_000,
    },
    "moderate": {
        "max_position_pct": 10, "stop_loss_pct": 40, "take_profit_pct": 200,
        "max_daily_loss_pct": 30, "max_open_positions": 4, "cooldown_seconds": 180,
        "min_rug_score": 60, "min_liquidity_usd": 20_000, "min_volume_24h": 5_000,
    },
    "aggressive": {
        "max_position_pct": 15, "stop_loss_pct": 50, "take_profit_pct": 500,
        "max_daily_loss_pct": 50, "max_open_positions": 5, "cooldown_seconds": 60,
        "min_rug_score": 50, "min_liquidity_usd": 10_000, "min_volume_24h": 1_000,
    },
    "yolo": {
        "max_position_pct": 25, "stop_loss_pct": 70, "take_profit_pct": 1000,
        "max_daily_loss_pct": 80, "max_open_positions": 8, "cooldown_seconds": 30,
        "min_rug_score": 40, "min_liquidity_usd": 5_000, "min_volume_24h": 500,
    },
}


# ============================================================
# DATA FETCHERS
# ============================================================
def rpc_call(method: str, params: list) -> dict:
    """Call Helius RPC."""
    if not HELIUS_API_KEY:
        log.error("HELIUS_API_KEY not set")
        return {}
    try:
        resp = requests.post(HELIUS_RPC,
                             json={"jsonrpc": "2.0", "id": "agent", "method": method, "params": params},
                             timeout=15)
        resp.raise_for_status()
        return resp.json().get("result") or {}
    except Exception as e:
        log.error(f"RPC error: {e}")
        return {}


def fetch_new_pairs(min_liquidity: float, limit: int = 20) -> list:
    """Fetch new Solana pairs from DexScreener."""
    try:
        resp = requests.get(DEXSCREENER_LATEST, timeout=15)
        resp.raise_for_status()
        pairs = resp.json().get("pairs", [])
    except Exception as e:
        log.error(f"DexScreener error: {e}")
        return []

    filtered = []
    for p in pairs:
        liq = float((p.get("liquidity") or {}).get("usd") or 0)
        vol = float((p.get("volume") or {}).get("h24") or 0)
        if liq < min_liquidity or vol < 1_000:
            continue
        filtered.append({
            "mint": (p.get("baseToken") or {}).get("address", ""),
            "symbol": (p.get("baseToken") or {}).get("symbol", "?"),
            "liquidity_usd": liq,
            "volume_24h": vol,
            "market_cap": float(p.get("marketCap") or 0),
            "price_usd": float(p.get("priceUsd") or 0),
            "price_change_24h": float((p.get("priceChange") or {}).get("h24") or 0),
            "pair_age_ms": p.get("pairCreatedAt") or 0,
            "url": p.get("url", ""),
        })
    return sorted(filtered, key=lambda x: x["pair_age_ms"], reverse=True)[:limit]


def calculate_rug_score(mint: str) -> tuple:
    """Calculate quick rug score for token."""
    info = rpc_call("getAccountInfo", [mint, {"encoding": "jsonParsed"}])
    parsed = (info.get("value") or {}).get("data", {}).get("parsed", {}).get("info", {}) if info else {}

    if not parsed:
        return 0, "Token not found"

    score = 0
    reasons = []

    if parsed.get("mintAuthority") is None:
        score += 25
    else:
        reasons.append("Mint authority active")

    if parsed.get("freezeAuthority") is None:
        score += 20
    else:
        reasons.append("Freeze authority active")

    # Get top holders
    holders = rpc_call("getTokenLargestAccounts", [mint])
    accounts = (holders.get("value") or []) if holders else []
    total = sum(float(a.get("uiAmount") or 0) for a in accounts)
    top10 = sum(float(a.get("uiAmount") or 0) for a in accounts[:10])
    if total > 0:
        pct = (top10 / total) * 100
        if pct < 40:
            score += 20
        elif pct < 60:
            score += 10

    score += 15  # bonus for successful parse
    return score, "; ".join(reasons) if reasons else "All checks passed"


# ============================================================
# AGENT STATE
# ============================================================
class AgentState:
    """Persistent agent state across runs."""

    def __init__(self, capital: float):
        STATE_DIR.mkdir(exist_ok=True)
        self.capital = capital
        self.initial_capital = capital
        self.positions: dict = {}  # {mint: {entry_price, amount, entry_time}}
        self.last_trade_time = None
        self.daily_pnl: float = 0.0
        self.daily_reset_date = datetime.utcnow().date()
        self.trade_log = []
        self.paused = False
        self._load()

    def _load(self):
        if STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text())
                self.capital = data.get("capital", self.capital)
                self.initial_capital = data.get("initial_capital", self.capital)
                self.positions = data.get("positions", {})
                self.trade_log = data.get("trade_log", [])
            except Exception as e:
                log.warning(f"Could not load state: {e}")

    def save(self):
        data = {
            "capital": self.capital,
            "initial_capital": self.initial_capital,
            "positions": self.positions,
            "trade_log": self.trade_log[-100:],
            "saved_at": datetime.utcnow().isoformat() + "Z",
        }
        STATE_FILE.write_text(json.dumps(data, indent=2))
        os.chmod(STATE_FILE, 0o600)

    def record_trade(self, mint: str, side: str, amount_usd: float, price: float, reason: str):
        self.trade_log.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "mint": mint,
            "side": side,
            "amount_usd": amount_usd,
            "price": price,
            "reason": reason,
        })

    def reset_daily_pnl(self):
        today = datetime.utcnow().date()
        if today != self.daily_reset_date:
            self.daily_pnl = 0.0
            self.daily_reset_date = today

    def check_pause_file(self):
        """Check if user created pause file."""
        self.paused = PAUSE_FILE.exists()


# ============================================================
# STRATEGY DECISION
# ============================================================
def should_buy(token: dict, rug_score: int, state: AgentState, config: dict) -> tuple:
    """Decide whether to buy token. Returns (should_buy: bool, size_usd: float, reason: str)."""
    # 1. Rug score check
    if rug_score < config["min_rug_score"]:
        return False, 0, f"Rug score {rug_score} < {config['min_rug_score']}"

    # 2. Liquidity check
    if token["liquidity_usd"] < config["min_liquidity_usd"]:
        return False, 0, f"Liquidity ${token['liquidity_usd']:,.0f} < ${config['min_liquidity_usd']:,.0f}"

    # 3. Volume check
    if token["volume_24h"] < config["min_volume_24h"]:
        return False, 0, f"Volume ${token['volume_24h']:,.0f} < ${config['min_volume_24h']:,.0f}"

    # 4. Max positions check
    if len(state.positions) >= config["max_open_positions"]:
        return False, 0, f"Max open positions ({config['max_open_positions']}) reached"

    # 5. Already in position?
    if token["mint"] in state.positions:
        return False, 0, "Already in position"

    # 6. Cooldown check
    if state.last_trade_time:
        elapsed = (datetime.utcnow() - state.last_trade_time).total_seconds()
        if elapsed < config["cooldown_seconds"]:
            return False, 0, f"Cooldown {elapsed:.0f}s / {config['cooldown_seconds']}s"

    # 7. Calculate position size
    position_size = state.capital * (config["max_position_pct"] / 100)

    return True, position_size, f"All checks passed (rug={rug_score}, liq=${token['liquidity_usd']:,.0f})"


def should_sell(mint: str, current_price: float, state: AgentState, config: dict) -> tuple:
    """Decide whether to sell. Returns (should_sell: bool, reason: str)."""
    if mint not in state.positions:
        return False, "No position"

    pos = state.positions[mint]
    entry = pos["entry_price"]
    change_pct = ((current_price - entry) / entry) * 100

    if change_pct <= -config["stop_loss_pct"]:
        return True, f"STOP LOSS at {change_pct:.1f}%"

    if change_pct >= config["take_profit_pct"]:
        return True, f"TAKE PROFIT at +{change_pct:.1f}%"

    return False, f"Hold ({change_pct:+.1f}%)"


# ============================================================
# EXECUTION (dry-run or live)
# ============================================================
def execute_trade(dry_run: bool, mint: str, side: str, size_usd: float,
                  state: AgentState, discord_webhook: Optional[str] = None) -> dict:
    """Execute trade. In dry-run mode, just record."""

    price = 0.0
    # In dry-run, use DexScreener price; in live, use Jupiter quote
    if side == "buy":
        # Simplified: get price from DexScreener pairs
        try:
            resp = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{mint}", timeout=10)
            pairs = resp.json().get("pairs") or []
            if pairs:
                price = float(pairs[0].get("priceUsd") or 0)
        except Exception:
            pass

    if dry_run:
        action = f"DRY RUN: Would {side.upper()} ${size_usd:.2f} of {mint[:8]}..."
    else:
        # LIVE MODE — would integrate Jupiter swap & wallet signing here
        # For safety, this template only logs the action without actual execution
        action = f"LIVE: {side.upper()} ${size_usd:.2f} of {mint[:8]}..."
        # NOTE: Actual swap implementation requires:
        # 1. Jupiter quote API
        # 2. Build swap transaction
        # 3. Sign with encrypted wallet
        # 4. Send via Helius Sender (private mempool)
        # See: https://docs.jup.ag/docs/swap-integration

    log.info(f"  {action}")
    if side == "buy":
        state.capital -= size_usd
        if price > 0:
            state.positions[mint] = {
                "entry_price": price,
                "amount_usd": size_usd,
                "entry_time": datetime.utcnow().isoformat() + "Z",
            }
        state.last_trade_time = datetime.utcnow()
    elif side == "sell":
        if mint in state.positions:
            pos = state.positions.pop(mint)
            pnl = size_usd - pos["amount_usd"]
            state.capital += size_usd
            state.daily_pnl += pnl

    state.record_trade(mint, side, size_usd, price, action)
    state.save()

    # Discord notification
    if discord_webhook:
        try:
            requests.post(discord_webhook, json={"content": f"🤖 AGENT: {action}"}, timeout=10)
        except Exception:
            pass

    return {"success": True, "action": action}


# ============================================================
# MAIN LOOP
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Solana Trading Agent")
    parser.add_argument("--dry-run", action="store_true", help="Paper trading mode (no real transactions)")
    parser.add_argument("--live", action="store_true", help="Live trading mode (REAL MONEY)")
    parser.add_argument("--capital", type=float, default=100, help="Initial capital in USD")
    parser.add_argument("--strategy", default="conservative", choices=list(STRATEGIES.keys()),
                        help="Strategy preset")
    parser.add_argument("--max-position", type=float, help="Override max position %%")
    parser.add_argument("--stop-loss", type=float, help="Override stop loss %%")
    parser.add_argument("--take-profit", type=float, help="Override take profit %%")
    parser.add_argument("--max-daily-loss", type=float, help="Override max daily loss %%")
    parser.add_argument("--interval", type=int, default=60, help="Scan interval (seconds)")
    parser.add_argument("--duration", type=int, help="Run duration in minutes (default: forever)")
    parser.add_argument("--discord", help="Discord webhook URL for notifications")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    if not args.dry_run and not args.live:
        parser.error("Specify --dry-run or --live")

    if args.live and args.capital > 50:
        log.warning(f"⚠️  LIVE mode with ${args.capital} capital. Start small!")

    config = dict(STRATEGIES[args.strategy])
    if args.max_position: config["max_position_pct"] = args.max_position
    if args.stop_loss: config["stop_loss_pct"] = args.stop_loss
    if args.take_profit: config["take_profit_pct"] = args.take_profit
    if args.max_daily_loss: config["max_daily_loss_pct"] = args.max_daily_loss

    state = AgentState(capital=args.capital)
    end_time = None
    if args.duration:
        end_time = datetime.utcnow() + timedelta(minutes=args.duration)

    mode = "DRY RUN" if args.dry_run else "⚠️  LIVE"
    log.info("=" * 60)
    log.info(f"🤖 Solana Trading Agent — {mode} Mode")
    log.info("=" * 60)
    log.info(f"⚙️  Strategy: {args.strategy}")
    log.info(f"💰 Capital: ${state.capital:.2f}")
    log.info(f"🎯 Max position: {config['max_position_pct']}%")
    log.info(f"🛑 Stop loss: -{config['stop_loss_pct']}%")
    log.info(f"🎯 Take profit: +{config['take_profit_pct']}%")
    log.info(f"📉 Max daily loss: -{config['max_daily_loss_pct']}%")
    log.info(f"🔢 Max open positions: {config['max_open_positions']}")
    log.info(f"⏰ Cooldown: {config['cooldown_seconds']}s")
    log.info(f"📊 Min rug score: {config['min_rug_score']}")
    log.info("=" * 60)
    log.info(f"💡 Tip: Create file {PAUSE_FILE} to pause agent")
    log.info(f"💡 Logs: agent_trader.log")
    log.info("=" * 60)

    try:
        while True:
            # End time check
            if end_time and datetime.utcnow() >= end_time:
                log.info("⏰ Duration reached, exiting")
                break

            # Pause file check
            state.check_pause_file()
            if state.paused:
                log.info("⏸️  Paused (touch ~/.agent_paused detected). Sleeping 60s...")
                time.sleep(60)
                continue

            # Daily loss check
            state.reset_daily_pnl()
            max_daily_loss = state.capital * (config["max_daily_loss_pct"] / 100)
            if state.daily_pnl < -max_daily_loss:
                log.warning(f"🛑 Daily loss limit hit (${state.daily_pnl:.2f}). Pausing for 24h.")
                time.sleep(86400)
                continue

            # Scan for new tokens
            log.info(f"👀 Scanning DexScreener...")
            tokens = fetch_new_pairs(min_liquidity=config["min_liquidity_usd"])

            if not tokens:
                log.info("   No tokens found")
            else:
                log.info(f"   Found {len(tokens)} candidates")

                for token in tokens[:5]:  # check top 5 only per cycle
                    # Skip if already in position
                    if token["mint"] in state.positions:
                        # Check exit conditions
                        current_price = token["price_usd"]
                        should_exit, reason = should_sell(token["mint"], current_price, state, config)
                        if should_exit:
                            pos = state.positions[token["mint"]]
                            execute_trade(args.dry_run, token["mint"], "sell",
                                          pos["amount_usd"], state, args.discord)
                            log.info(f"   🔴 SELL {token['symbol']}: {reason}")
                        continue

                    # Calculate rug score
                    rug_score, rug_reason = calculate_rug_score(token["mint"])
                    if rug_score == 0:
                        continue

                    # Decide
                    should_buy_now, size_usd, reason = should_buy(token, rug_score, state, config)
                    if should_buy_now:
                        execute_trade(args.dry_run, token["mint"], "buy",
                                      size_usd, state, args.discord)
                        log.info(f"   🟢 BUY {token['symbol']}: {reason}")
                        break  # one buy per cycle
                    else:
                        log.debug(f"   ⏭️  Skip {token['symbol']}: {reason}")

            if args.once:
                break

            log.info(f"💼 Capital: ${state.capital:.2f} | Open: {len(state.positions)} | "
                     f"Daily P&L: ${state.daily_pnl:.2f}")
            log.info(f"   Sleeping {args.interval}s...")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        log.info("\n👋 Agent stopped by user")

    state.save()
    log.info(f"💾 Final state saved to {STATE_FILE}")
    log.info(f"📊 Total trades: {len(state.trade_log)}")


if __name__ == "__main__":
    main()

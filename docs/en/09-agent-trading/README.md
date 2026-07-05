# 🤖 09. Trading with AI Agent — Setup, Install, & Execute

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/09-agent-trading/README.md)

> 🎯 **Goal:** Set up your own Solana trading agent — autonomous, safe, with strict guardrails.

---

## 📖 Table of Contents

- [What is Agent Trading?](#what-is-agent-trading)
- [Agent Architecture](#agent-architecture)
- [Choose Agent Platform](#choose-agent-platform)
- [Install & Setup](#install--setup)
- [Simple Agent Example](#simple-agent-example)
- [Strategy Library](#strategy-library)
- [Mandatory Guardrails](#mandatory-guardrails)
- [Trade Execution](#trade-execution)
- [Monitoring & Override](#monitoring--override)
- [Troubleshooting](#troubleshooting)

---

## What is Agent Trading?

**Agent trading** = AI/automated program that:
1. 👀 **Monitor** market in real-time (new tokens, price, holder activity)
2. 🧠 **Analyze** based on rules / LLM / signals
3. ✅ **Decide** buy/sell based on strategy
4. 🚀 **Execute** transactions via Jupiter/Raydium
5. 📊 **Report** results to Discord/Telegram

```
   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ MONITOR  │ →  │ ANALYZE  │ →  │ DECIDE   │ →  │ EXECUTE  │
   │          │    │          │    │          │    │          │
   │ • DexScr │    │ • rug    │    │ • rules  │    │ • Jupiter│
   │ • Helius │    │   score  │    │ • LLM    │    │ • wallet │
   │ • X/CTG  │    │ • social │    │ • size   │    │   sign   │
   └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

> ⚠️ **Agent ≠ autopilot greedy.** A good agent has **strict guardrails**: position limit, stop loss, kill switch, dry-run mode.

---

## Agent Architecture

### Layer 1: Data Sources (Input)
| Source | Used for | API |
|---|---|---|
| **Helius RPC** | On-chain data, holders, mint info | Helius |
| **DexScreener** | Volume, LP, market cap | Free |
| **Jupiter Price** | Real-time price | Free |
| **Birdeye** | Social metrics, trending | Optional |
| **X/Twitter API** | Sentiment, alpha calls | Optional |
| **Telegram channels** | Signal groups | Manual |

### Layer 2: Analysis (Brain)
| Method | Best for |
|---|---|
| **Rule-based** | Beginners, predictable, easy to debug |
| **LLM-based** (GPT, Claude) | Adaptive, narrative analysis |
| **ML model** | Advanced, needs dataset |
| **Hybrid** | Production-grade |

### Layer 3: Decision Engine
- Position sizing rules
- Risk management
- Portfolio constraints
- Kill switch

### Layer 4: Execution
- Jupiter Aggregator API (best price)
- Wallet signing (stored encrypted)
- Slippage protection

### Layer 5: Reporting
- Discord webhook
- Telegram bot
- Dashboard (Streamlit)

---

## Choose Agent Platform

### Option A: Self-Hosted Python (Recommended for Learning)

```bash
# Minimum stack
Python 3.11+
Helius RPC (free tier)
Jupiter API (free, no key)
Solana wallet (encrypted)
```

**Pros:** Full control, free, customizable, learning-friendly
**Cons:** Self-managed (uptime, security)

### Option B: Telegram Bot as Agent

Use Telegram bots like **Trojan**, **BonkBot**, **Maestro**:

| Bot | Setup | Features |
|---|---|---|
| **Trojan** | DM @Trojan_on_solana | Sniper, copy trade, limit, DCA |
| **BonkBot** | DM @bonkbot_solana | Sniper + anti-MEV |
| **Maestro** | DM @MaestroBot | Advanced, multi-wallet |

> ⚠️ **Telegram bot = delegate agent to third party.** Wallet stored on their server. Trust risk.

### Option C: Cloud-Based Agent Platform

| Platform | Type | Price |
|---|---|---|
| **GMGN.ai** | Sniper bot | Freemium |
| **Axiom.trade** | Smart money tracking | Subscription |
| **Bloom Trading** | AI auto-trade | Premium |

### Option D: LLM Agent (AI Reasoning)

Use LLM (Claude/GPT) as decision engine:

```python
# Pseudo-code
def decide_trade(token_data, market_context):
    prompt = f"""
    Token: {token_data['symbol']}
    Market cap: ${token_data['mc']}
    Rug score: {token_data['rug_score']}/100
    Narrative: {token_data['narrative']}

    Decide: BUY / SKIP
    Reasoning:
    """
    return llm.complete(prompt)
```

**Pros:** Can analyze narrative & sentiment that rule-based can't
**Cons:** Needs LLM API key, higher latency, hallucination risk

---

## Install & Setup

### 1. Prerequisites

```bash
# System
- Linux/MacOS (or WSL on Windows)
- Python 3.11+
- 2GB RAM minimum
- Stable internet

# Wallet
- Dedicated Solana trading wallet (NOT main wallet)
- Minimum 0.5 SOL for gas + trading
- Seed phrase stored offline
```

### 2. Clone Repo & Install

```bash
# Clone
git clone https://github.com/Celebez/solana-agent-memecoin.git
cd solana-agent-memecoin

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt

# Setup API keys (don't commit!)
export HELIUS_API_KEY="your-key-here"
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

### 3. Generate Trading Wallet

```bash
python scripts/wallet_setup.py
```

Output:
```
Passphrase (min 12 char): ********
Konfirmasi passphrase: ********
Label wallet: trading-agent
Simpan di [~/.solana-wallets/...]: [Enter]

✅ Wallet berhasil dibuat!
   📍 Address : 7xKXtg...XXXX
   💾 File    : ~/.solana-wallets/trading-agent-7xKXtg.json
```

> ⚠️ **SAVE passphrase in password manager.** Wallet file CANNOT be decrypted without passphrase.

### 4. Fund Wallet

```bash
# Send SOL to trading wallet address
# Minimum 0.5 SOL to start
# Recommended 1-2 SOL for several trades

# Check balance
python scripts/multi_wallet_balance.py <YOUR_ADDRESS>
```

### 5. Test Agent (Dry Run)

```bash
# DRY RUN mode — no real transactions
python scripts/agent_trader.py --dry-run --strategy conservative
```

Output:
```
🤖 Solana Trading Agent — Dry Run Mode

⚙️  Strategy: Conservative
💰 Wallet: 7xKXtg...XXXX
🎯 Max position: 5% capital
🛑 Stop loss: -30%
📊 Initialized

[10:23:45] 👀 Scanning DexScreener...
[10:23:46] 🆕 Found 3 new tokens
[10:23:47] 🔍 Token X: rug_score=85, mc=$50K
[10:23:48] ✅ DRY RUN: Would BUY $25 of Token X
[10:23:48]    Reasoning: High rug score, trending on CT
```

### 6. Live Mode (CAREFUL!)

```bash
# Backup: test with $10 first
python scripts/agent_trader.py --live --capital 10 --strategy conservative

# Monitor via Discord (recommended)
python scripts/agent_trader.py --live --capital 100 \
  --discord $DISCORD_WEBHOOK_URL \
  --strategy conservative
```

---

## Simple Agent Example

See [`scripts/agent_trader.py`](../../scripts/agent_trader.py) — working example with guardrails.

### Built-in Features:

```python
# 1. Pre-trade safety check
if rug_score < 60:
    return SKIP

# 2. Position sizing
position_size = capital * MAX_POSITION_PCT  # default 5%

# 3. Stop loss & take profit
if current_price < entry_price * (1 - STOP_LOSS):
    return SELL
if current_price > entry_price * (1 + TAKE_PROFIT):
    return SELL

# 4. Daily loss limit
if daily_pnl < -MAX_DAILY_LOSS:
    return PAUSE_AGENT
```

### Full CLI Usage:

```bash
python scripts/agent_trader.py \
  --live \
  --capital 100 \
  --strategy conservative \
  --max-position 5 \
  --stop-loss 30 \
  --take-profit 100 \
  --max-daily-loss 20 \
  --interval 60 \
  --discord $DISCORD_WEBHOOK_URL
```

### Strategy Presets:

| Strategy | Max Pos | Stop Loss | Take Profit | Daily Loss | Best for |
|---|---|---|---|---|---|
| `ultra-safe` | 1% | 15% | 50% | 5% | Learning, small capital |
| `conservative` | 5% | 30% | 100% | 20% | Daily, established token |
| `moderate` | 10% | 40% | 200% | 30% | Trending token |
| `aggressive` | 15% | 50% | 500% | 50% | Sniping (high risk) |
| `yolo` | 25% | 70% | 1000% | 80% | Almost guaranteed rug |

---

## Strategy Library

### Strategy 1: "Trending New Launch"

```python
def trending_new_launch(token):
    """Buy new token trending on CT & high holders growth."""
    if token.age_hours > 6: return SKIP
    if token.rug_score < 70: return SKIP
    if token.holders_growth_1h < 50: return SKIP
    if token.volume_24h < 10000: return SKIP
    return BUY(size=capital * 0.03)
```

### Strategy 2: "Whale Accumulation"

```python
def whale_accumulation(token):
    """Buy when top 10 holders increase (smart money entering)."""
    if token.rug_score < 80: return SKIP
    if token.top10_change_24h <= 0: return SKIP  # whales selling
    if token.mc > 1_000_000: return SKIP  # too late
    return BUY(size=capital * 0.05)
```

### Strategy 3: "Mean Reversion"

```python
def mean_reversion(token):
    """Buy when token trending dump after healthy pump."""
    if token.change_24h > -30: return SKIP  # not dumped enough
    if token.volume_spike_1h < 2: return SKIP
    if token.rug_score < 70: return SKIP
    return BUY(size=capital * 0.02)
```

### Custom Strategy

Edit `scripts/agent_trader.py` and add new function in `# === STRATEGIES ===` section. See docstring for signature.

---

## Mandatory Guardrails

> 🚨 **MANDATORY before running live.** Agent without guardrails = ticking time bomb.

### 🛑 1. Position Size Cap
```python
MAX_POSITION_PCT = 5  # max 5% capital per token
```

### 🛑 2. Stop Loss
```python
STOP_LOSS_PCT = 30  # cut loss at -30%
```

### 🎯 3. Take Profit
```python
TAKE_PROFIT_PCT = 100  # take profit at +100% (2x)
```

### 📉 4. Daily Loss Limit
```python
MAX_DAILY_LOSS_PCT = 20  # pause agent if loses >20% per day
```

### 🔢 5. Max Open Positions
```python
MAX_OPEN_POSITIONS = 3  # max 3 tokens simultaneously
```

### ⏰ 6. Cooldown Period
```python
COOLDOWN_BETWEEN_TRADES = 300  # 5 minutes minimum between trades
```

### 🔒 7. Token Whitelist/Blacklist
```python
BLOCKED_MINTS = [...]  # list of forbidden mints
ALLOWED_NARRATIVES = ["meme", "ai", "defi"]  # optional filter
```

### 🛑 8. Kill Switch (Manual)
```bash
# Stop agent with signal
Ctrl+C (SIGINT)

# Or kill from process
pkill -f agent_trader.py
```

### 📋 9. Audit Log
Every decision must be logged:
```
[2026-07-05 10:23:45] DECISION: BUY $5 of TOKEN_X
   Reason: rug_score=85, trending on CT
   Token: 7xKXtg...
   Price: $0.0000123
```

### 🧪 10. Dry Run First
```bash
# ALWAYS test in dry-run 24-48 hours before live
python agent_trader.py --dry-run --duration 24h
```

---

## Trade Execution

### Jupiter Swap API

Agent uses **Jupiter Aggregator** for execution (best price):

```python
# Pseudocode
quote = jupiter.get_quote(
    input_mint="SOL",
    output_mint=token_mint,
    amount=position_size_lamports,
    slippage_bps=300,  # 3% for meme coin
)

tx = jupiter.build_swap_transaction(quote, wallet.public_key)
signature = wallet.sign_and_send(tx)

# Confirm
result = solana.confirm_transaction(signature, timeout=60)
```

### Slippage Guide

| Situation | Slippage |
|---|---|
| Liquid (SOL, USDC, BONK) | 0.5–1% |
| Trending meme | 2–3% |
| Sniping new | 3–5% |
| Microcap | 5–10% (risky) |

> ⚠️ **Slippage too high = sandwich attack risk.**

### Private Mempool (Anti-MEV)

For large trades, use private routing:

```python
# Helius Sender (private mempool)
tx = jupiter.build_swap_with_sender(tx, sender_endpoint=helius_sender)

# Or use Jito bundle
tx = jito.build_bundle([tx])
```

---

## Monitoring & Override

### Real-time Monitoring

```bash
# Terminal 1: agent running
python scripts/agent_trader.py --live --discord $WEBHOOK

# Terminal 2: monitor balance
watch -n 30 "python scripts/multi_wallet_balance.py <WALLET>"

# Terminal 3: portfolio dashboard
streamlit run scripts/streamlit_dashboard.py
```

### Discord Notifications

Every trade sends to Discord:

```
🤖 AGENT TRADE
✅ BUY executed
Token: BONK
Amount: $5.00 (0.05 SOL)
Price: $0.0000123
TX: https://solscan.io/tx/5x...
Reason: rug_score=85, trending
```

### Manual Override

Sometimes agent makes mistakes. Override with:

```bash
# 1. Kill agent
pkill -f agent_trader.py

# 2. Manual sell via Jupiter UI
# https://jupiter.ag → connect wallet → sell

# 3. Investigate log
cat agent_trader.log | grep "DECISION"

# 4. Adjust strategy
nano scripts/agent_trader.py
```

### Pause Strategy Without Killing

Create file `~/.agent_paused`:
```bash
touch ~/.agent_paused
# Agent will pause next loop iteration

# Resume
rm ~/.agent_paused
```

---

## Troubleshooting

### ❌ "Insufficient balance"
- Send SOL to agent wallet
- Check balance: `python scripts/multi_wallet_balance.py <WALLET>`

### ❌ "Transaction failed"
- Slippage too low → raise to 3-5%
- Slow RPC → use Helius Sender
- Low priority fee → set priority fee

### ❌ "Rug score too low"
- Strategy too strict → adjust min_rug_score
- Volatile market → use conservative strategy

### ❌ "Agent not finding tokens"
- Check DexScreener API status
- Increase scan interval (don't go too fast = rate limit)

### ❌ "Discord webhook not working"
- Test webhook: `python scripts/discord_notifier.py "test"`
- Check URL is correct
- Check channel permission

---

## 📚 Further References

### Resources
- 📖 [Jupiter Aggregator Docs](https://docs.jup.ag)
- 📖 [Helius RPC Docs](https://docs.helius.dev)
- 📖 [Solana Cookbook](https://solanacookbook.com)
- 📖 [Anchor Framework](https://www.anchor-lang.com/)

### Repository Sections
- 📖 [08. Anti-Scam Tips](../08-tips/README.md) — trader wisdom
- 📖 [07. Tools](../07-tools/README.md) — bots & alerts
- 📖 [Scripts](../../scripts/README.md) — automation library

---

> ⚠️ **FINAL DISCLAIMER:** Agent trading is **NOT profit autopilot**. Most agents lose money due to poor strategy or no guardrails. Always: dry-run → backtest → small capital → iterate. **NOT financial advice.**

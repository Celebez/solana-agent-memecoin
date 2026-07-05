# 🤖 09. Trading dengan AI Agent — Setup, Install, & Eksekusi

> 🇮🇩 Bahasa Indonesia | 🇬🇧 [English](../en/09-agent-trading/README.md)

> 🎯 **Tujuan:** Setup agent trading Solana Anda sendiri — autonomous, aman, dengan guardrails ketat.

---

## 📖 Daftar Isi

- [Apa itu Agent Trading?](#apa-itu-agent-trading)
- [Arsitektur Agent](#arsitektur-agent)
- [Pilih Platform Agent](#pilih-platform-agent)
- [Install & Setup](#install--setup)
- [Contoh Agent Sederhana](#contoh-agent-sederhana)
- [Strategy Library](#strategy-library)
- [Guardrails Wajib](#guardrails-wajib)
- [Eksekusi Trade](#eksekusi-trade)
- [Monitoring & Override](#monitoring--override)
- [Troubleshooting](#troubleshooting)

---

## Apa itu Agent Trading?

**Agent trading** = program AI/automated yang:
1. 👀 **Monitor** market real-time (token baru, harga, holder activity)
2. 🧠 **Analisa** berdasarkan rules / LLM / signal
3. ✅ **Decide** beli/jual berdasarkan strategy
4. 🚀 **Eksekusi** transaksi via Jupiter/Raydium
5. 📊 **Report** hasil ke Discord/Telegram

```
   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ MONITOR  │ →  │ ANALYZE  │ →  │ DECIDE   │ →  │ EXECUTE  │
   │          │    │          │    │          │    │          │
   │ • DexScr │    │ • rug    │    │ • rules  │    │ • Jupiter│
   │ • Helius │    │   score  │    │ • LLM    │    │ • wallet │
   │ • X/CTG  │    │ • social │    │ • size   │    │   sign   │
   └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

> ⚠️ **Agent ≠ autopilot serakah.** Agent yang baik punya **guardrails ketat**: position limit, stop loss, kill switch, dry-run mode.

---

## Arsitektur Agent

### Layer 1: Data Sources (Input)
| Source | Untuk apa | API |
|---|---|---|
| **Helius RPC** | On-chain data, holder, mint info | Helius |
| **DexScreener** | Volume, LP, market cap | Free |
| **Jupiter Price** | Real-time price | Free |
| **Birdeye** | Social metrics, trending | Optional |
| **X/Twitter API** | Sentiment, alpha calls | Optional |
| **Telegram channels** | Signal groups | Manual |

### Layer 2: Analysis (Brain)
| Method | Cocok untuk |
|---|---|
| **Rule-based** | Pemula, predictable, mudah di-debug |
| **LLM-based** (GPT, Claude) | Adaptif, analisa narasi |
| **ML model** | Advanced, butuh dataset |
| **Hybrid** | Production-grade |

### Layer 3: Decision Engine
- Position sizing rules
- Risk management
- Portfolio constraints
- Kill switch

### Layer 4: Execution
- Jupiter Aggregator API (best price)
- Wallet signing (tersimpan encrypted)
- Slippage protection

### Layer 5: Reporting
- Discord webhook
- Telegram bot
- Dashboard (Streamlit)

---

## Pilih Platform Agent

### Opsi A: Self-Hosted Python (Recommended untuk Belajar)

```bash
# Stack minimum
Python 3.11+
Helius RPC (free tier)
Jupiter API (free, no key)
Wallet Solana (encrypted)
```

**Kelebihan:** Full control, free, customizable, learning-friendly
**Kekurangan:** Anda manage sendiri (uptime, security)

### Opsi B: Telegram Bot sebagai Agent

Gunakan bot Telegram seperti **Trojan**, **BonkBot**, **Maestro**:

| Bot | Setup | Fitur |
|---|---|---|
| **Trojan** | DM @Trojan_on_solana | Sniper, copy trade, limit, DCA |
| **BonkBot** | DM @bonkbot_solana | Sniper + anti-MEV |
| **Maestro** | DM @MaestroBot | Advanced, multi-wallet |

> ⚠️ **Bot Telegram = delegasikan agent ke third party.** Wallet disimpan di server mereka. Risiko trust.

### Opsi C: Cloud-Based Agent Platform

| Platform | Tipe | Harga |
|---|---|---|
| **GMGN.ai** | Sniper bot | Freemium |
| **Axiom.trade** | Smart money tracking | Subscription |
| **Bloom Trading** | AI auto-trade | Premium |

### Opsi D: LLM Agent (AI Reasoning)

Gunakan LLM (Claude/GPT) sebagai decision engine:

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

**Kelebihan:** Bisa analisa narasi & sentiment yang rule-based susah
**Kekurangan:** Butuh API key LLM, latency lebih tinggi, hallucination risk

---

## Install & Setup

### 1. Prasyarat

```bash
# System
- Linux/MacOS (atau WSL di Windows)
- Python 3.11+
- 2GB RAM minimum
- Koneksi internet stabil

# Wallet
- Wallet Solana khusus trading (BUKAN wallet utama)
- Minimal 0.5 SOL untuk gas + trading
- Seed phrase disimpan offline
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

# Setup API keys (jangan commit!)
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

> ⚠️ **SIMPAN passphrase di password manager.** File wallet TIDAK bisa di-decrypt tanpa passphrase.

### 4. Fund Wallet

```bash
# Kirim SOL ke address trading wallet
# Minimum 0.5 SOL untuk start
# Recommended 1-2 SOL untuk beberapa trade

# Cek saldo
python scripts/multi_wallet_balance.py <YOUR_ADDRESS>
```

### 5. Test Agent (Dry Run)

```bash
# DRY RUN mode — tanpa transaksi real
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

### 6. Live Mode (HATI-HATI!)

```bash
# Backup: test dengan $10 dulu
python scripts/agent_trader.py --live --capital 10 --strategy conservative

# Monitor via Discord (recommended)
python scripts/agent_trader.py --live --capital 100 \
  --discord $DISCORD_WEBHOOK_URL \
  --strategy conservative
```

---

## Contoh Agent Sederhana

Lihat [`scripts/agent_trader.py`](../../scripts/agent_trader.py) — working example dengan guardrails.

### Fitur Built-in:

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

### CLI Usage Lengkap:

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

| Strategy | Max Pos | Stop Loss | Take Profit | Daily Loss | Cocok untuk |
|---|---|---|---|---|---|
| `ultra-safe` | 1% | 15% | 50% | 5% | Belajar, modal kecil |
| `conservative` | 5% | 30% | 100% | 20% | Harian, established token |
| `moderate` | 10% | 40% | 200% | 30% | Trending token |
| `aggressive` | 15% | 50% | 500% | 50% | Sniping (high risk) |
| `yolo` | 25% | 70% | 1000% | 80% | Hampir pasti rug |

---

## Strategy Library

### Strategy 1: "Trending New Launch"

```python
def trending_new_launch(token):
    """Buy token baru yang trending di CT & high holders growth."""
    if token.age_hours > 6: return SKIP
    if token.rug_score < 70: return SKIP
    if token.holders_growth_1h < 50: return SKIP
    if token.volume_24h < 10000: return SKIP
    return BUY(size=capital * 0.03)
```

### Strategy 2: "Whale Accumulation"

```python
def whale_accumulation(token):
    """Buy saat top 10 holders bertambah (smart money masuk)."""
    if token.rug_score < 80: return SKIP
    if token.top10_change_24h <= 0: return SKIP  # whales selling
    if token.mc > 1_000_000: return SKIP  # too late
    return BUY(size=capital * 0.05)
```

### Strategy 3: "Mean Reversion"

```python
def mean_reversion(token):
    """Buy saat token trending dump setelah pump sehat."""
    if token.change_24h > -30: return SKIP  # not dumped enough
    if token.volume_spike_1h < 2: return SKIP
    if token.rug_score < 70: return SKIP
    return BUY(size=capital * 0.02)
```

### Custom Strategy

Edit `scripts/agent_trader.py` dan tambah function baru di section `# === STRATEGIES ===`. Lihat docstring untuk signature.

---

## Guardrails Wajib

> 🚨 **WAJIB ADA sebelum run live.** Agent tanpa guardrails = bom waktu.

### 🛑 1. Position Size Cap
```python
MAX_POSITION_PCT = 5  # max 5% modal per token
```

### 🛑 2. Stop Loss
```python
STOP_LOSS_PCT = 30  # cut loss di -30%
```

### 🎯 3. Take Profit
```python
TAKE_PROFIT_PCT = 100  # take profit di +100% (2x)
```

### 📉 4. Daily Loss Limit
```python
MAX_DAILY_LOSS_PCT = 20  # pause agent jika rugi >20% per hari
```

### 🔢 5. Max Open Positions
```python
MAX_OPEN_POSITIONS = 3  # max 3 token simultaneously
```

### ⏰ 6. Cooldown Period
```python
COOLDOWN_BETWEEN_TRADES = 300  # 5 menit minimum antar trade
```

### 🔒 7. Token Whitelist/Blacklist
```python
BLOCKED_MINTS = [...]  # list mint yang dilarang
ALLOWED_NARRATIVES = ["meme", "ai", "defi"]  # opsional filter
```

### 🛑 8. Kill Switch (Manual)
```bash
# Stop agent dengan signal
Ctrl+C (SIGINT)

# Atau kill dari process
pkill -f agent_trader.py
```

### 📋 9. Audit Log
Setiap keputusan harus di-log:
```
[2026-07-05 10:23:45] DECISION: BUY $5 of TOKEN_X
   Reason: rug_score=85, trending on CT
   Token: 7xKXtg...
   Price: $0.0000123
```

### 🧪 10. Dry Run First
```bash
# SELALU test di dry-run 24-48 jam sebelum live
python agent_trader.py --dry-run --duration 24h
```

---

## Eksekusi Trade

### Jupiter Swap API

Agent pakai **Jupiter Aggregator** untuk eksekusi (best price):

```python
# Pseudocode
quote = jupiter.get_quote(
    input_mint="SOL",
    output_mint=token_mint,
    amount=position_size_lamports,
    slippage_bps=300,  # 3% untuk meme coin
)

tx = jupiter.build_swap_transaction(quote, wallet.public_key)
signature = wallet.sign_and_send(tx)

# Confirm
result = solana.confirm_transaction(signature, timeout=60)
```

### Slippage Guide

| Situasi | Slippage |
|---|---|
| Liquid (SOL, USDC, BONK) | 0.5–1% |
| Trending meme | 2–3% |
| Sniping baru | 3–5% |
| Microcap | 5–10% (risky) |

> ⚠️ **Slippage terlalu tinggi = sandwich attack risk.**

### Private Mempool (Anti-MEV)

Untuk trade besar, pakai private routing:

```python
# Helius Sender (private mempool)
tx = jupiter.build_swap_with_sender(tx, sender_endpoint=helius_sender)

# Atau pakai Jito bundle
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

Setiap trade akan kirim ke Discord:

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

Kadang agent salah. Override dengan:

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

### Pause Strategy Tanpa Kill

Buat file `~/.agent_paused`:
```bash
touch ~/.agent_paused
# Agent akan pause next loop iteration

# Resume
rm ~/.agent_paused
```

---

## Troubleshooting

### ❌ "Insufficient balance"
- Kirim SOL ke wallet agent
- Cek balance: `python scripts/multi_wallet_balance.py <WALLET>`

### ❌ "Transaction failed"
- Slippage terlalu rendah → naikkan ke 3-5%
- RPC lambat → pakai Helius Sender
- Priority fee rendah → set priority fee

### ❌ "Rug score too low"
- Strategy terlalu strict → adjust min_rug_score
- Market volatile → gunakan conservative strategy

### ❌ "Agent not finding tokens"
- Cek DexScreener API status
- Increase scan interval (jangan terlalu cepat = rate limit)

### ❌ "Discord webhook not working"
- Test webhook: `python scripts/discord_notifier.py "test"`
- Cek URL benar
- Cek channel permission

---

## 📚 Referensi Lanjutan

### Resources
- 📖 [Jupiter Aggregator Docs](https://docs.jup.ag)
- 📖 [Helius RPC Docs](https://docs.helius.dev)
- 📖 [Solana Cookbook](https://solanacookbook.com)
- 📖 [Anchor Framework](https://www.anchor-lang.com/)

### Repository Sections
- 📖 [08. Tips Anti-Scam](../08-tips/README.md) — wisdom trader
- 📖 [07. Tools](../07-tools/README.md) — bot & alert
- 📖 [Scripts](../../scripts/README.md) — automation library

---

> ⚠️ **FINAL DISCLAIMER:** Agent trading **bukan autopilot profit**. Mayoritas agent lose money karena poor strategy atau no guardrails. Selalu: dry-run → backtest → small capital → iterate. **BUKAN saran finansial.**

# 🐸 04. Meme Coin — Anatomy, Risk & Opportunity

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/04-memecoin/README.md)

## Definition

**Meme coin** = crypto token with **minimal/zero intrinsic utility**, its value determined by:

- 🤝 Community strength
- 😂 Meme / internet culture
- 📈 Hype & momentum
- 🐋 Whales (large holders)
- 🎯 CEX listing timing (Binance, Coinbase, etc.)

## 🧬 Anatomy of a Solana Token

Every SPL (Solana Program Library) token has metadata:

```
Mint Address  : 7xKXtg... (unique token identity)
Decimals      : 6 / 9 / 18 (precision)
Supply        : 1,000,000,000 (1B)
Authorities   :
  - Mint Authority    : who can add supply
  - Freeze Authority  : who can freeze token holders
Metadata      : name, symbol, logo URI
```

> ⚠️ **Active Mint Authority = danger**. Can mint unlimited → supply rises → price drops.
> ⚠️ **Active Freeze Authority = danger**. Can freeze your wallet → can't sell.

## 📊 Meme Coin Lifecycle

```
       ┌──────────┐
       │  Launch  │   ← New token, supply in LP
       └─────┬────┘
             ▼
       ┌──────────┐
       │   Pump   │   ← Hype rises, FOMO enters
       └─────┬────┘
             ▼
       ┌──────────┐
       │  Peak    │   ← ATH, time to EXIT
       └─────┬────┘
             ▼
       ┌──────────┐
       │   Dump   │   ← Whales exit, retail loses
       └─────┬────┘
             ▼
       ┌──────────┐
       │Recovery  │   ← Stabilize at low, or rug = 0
       └──────────┘
```

**Your goal:** Buy at early Pump, sell before Peak.

## 🎭 Types of Meme Coins by Origin

### 1. 🐶 Established Meme Coin
Examples: BONK, WIF, POPCAT, MEW
- Already listed on major CEXs
- High liquidity, more stable
- Slower growth (~5–50x)

### 2. 🔥 Trending Token
Examples: tokens viral on Twitter/X
- Quickly 50–500x in hours
- High risk, needs precise timing
- Extreme volatility

### 3. 💩 Microcap
Examples: new tokens from pump.fun
- Market cap < $100K
- VERY high rug pull risk
- 1000x potential but 99% rug

## 🏛️ Launching Platforms

| Platform | Mechanism | Risk | Examples |
|---|---|---|---|
| **pump.fun** | Fair launch, bonding curve | Medium | DOGE20, MEW |
| **Raydium** | DEX, LP must be provided | Low-Medium | New tokens |
| **Orca** | DEX, focus on Solana DeFi | Low | New tokens |
| **Meteora** | Dynamic AMM | Medium | DLMM pairs |
| **Jupiter Studio** | Token launchpad | Medium | JUP token |

## 💡 Entry Strategies

### A. Sniping (First Seconds)
- Buy **< 30 seconds** after launch
- Needs **bot** (Trojan, BonkBot, Maestro)
- Very high risk (honeypot, dev dump)

### B. Early Trending (Minutes to Hours)
- Buy when starting to trend on Twitter/DexScreener
- Safer, still 10–100x possible
- Needs real-time monitoring

### C. Breakout Trading
- Wait for volume + community confirmation
- Entry on pullback/retest of support
- Better risk/reward, but smaller upside

## 📈 Exit Strategies

> 🎯 **Exit plan is more important than entry plan.**

### 1. 🎯 Profit Target
| Profit | Action |
|---|---|
| **+100% (2x)** | Take out initial capital |
| **+300% (4x)** | Take 50% profit |
| **+1000% (10x)** | Take 70–80% |
| **+10000% (100x)** | Remaining 1–5% as "moon bag" |

### 2. 🛑 Stop Loss
- **Hard stop** at -30% to -50% (depending on volatility)
- Use mental stop, **DO NOT** leave on exchange (instant rug pull)

### 3. ⏰ Time Stop
- After 1–2 weeks **no catalyst** → cut loss
- "Dead cat bounce" can happen but rare

## 📊 Important Metrics to Watch

| Metric | Source | Meaning |
|---|---|---|
| **Market Cap** | DexScreener | Total token valuation |
| **FDV** | DexScreener | Valuation if all tokens unlocked |
| **Liquidity** | DexScreener | How much SOL/USDC in LP |
| **Holders** | Solscan | Number of unique wallets |
| **Top 10 holders %** | Solscan | Concentration (danger if >50%) |
| **Volume 24h** | DexScreener | How active trading is |
| **Buy/Sell ratio** | Birdeye | Real-time sentiment |

## ⚠️ Definite Rug Pull Signs

```
🚩 1. Liquidity < $5,000
🚩 2. Top 10 holders > 60%
🚩 3. Mint authority still active
🚩 4. Freeze authority still active
🚩 5. Dev wallet > 20% supply
🚩 6. Volume drop > 90% in 1 hour
🚩 7. Social channels created < 1 week ago
🚩 8. Team anonymous + no audit
🚩 9. "Don't sell, we'll moon together" — but devs are selling
🚩 10. Token contract not verified
```

## 📚 Pre-Buy Checklist

```markdown
[ ] Mint authority: NONE
[ ] Freeze authority: NONE  
[ ] Top 10 holders < 50%
[ ] Liquidity > $50,000 and locked
[ ] Dev wallet < 10% supply
[ ] Organic volume (not wash trading)
[ ] Social proof (real Twitter followers, active Telegram)
[ ] Not in scam database (RugCheck, Chainabuse)
[ ] You can afford 100% loss
[ ] Clear exit plan
```

## 🔗 Next

- **[04. Meme Coin](../04-memecoin/README.md)** — what, why, how
- **[05. Token Safety Check](../05-token-check/README.md)** — check with Helius RPC + scripts
- **[06. Trading](../06-trading/README.md)** — Jupiter, Raydium, Pump.fun
- **[09. 🤖 Trading with AI Agent](../09-agent-trading/README.md)** — autonomous trading

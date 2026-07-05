# 💱 06. Trading — Buy/Sell on Jupiter, Raydium, Pump.fun

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/06-trading/README.md)

## 🏛️ Major DEXs on Solana

| DEX | Volume | Strengths | Weaknesses |
|---|---|---|---|
| **Jupiter** | Aggregator #1 | Best price routing | Executes via other DEXs |
| **Raydium** | High | Deep liquidity, AMM v4 | UI less intuitive |
| **Orca** | Medium | Concentrated liquidity | Limited pairs |
| **Meteora** | Medium | DLMM, advanced LP | Needs understanding |
| **Pump.fun** | Very high | Meme coin launchpad | High risk |

## 🌐 Jupiter (Aggregator)

**URL:** https://jupiter.ag

Why use Jupiter:
- ✅ **Best price** — auto-routes to DEX with best price
- ✅ **Limit orders** (free)
- ✅ **DCA** (Dollar-Cost Averaging)
- ✅ **Perpetuals** (leverage trading)

### How to Swap

1. Go to https://jupiter.ag
2. Connect wallet (Phantom/Solflare)
3. Select **From**: SOL/USDC
4. Select **To**: token you want to buy
5. Set **slippage** (default 0.5%, raise to 1–3% for meme coins)
6. Click **Swap** → confirm in wallet

### Slippage Guide

| Situation | Recommended Slippage |
|---|---|
| **Liquid token (SOL, USDC, BONK)** | 0.1–0.5% |
| **Trending token** | 1–2% |
| **Sniping new launch** | 3–5% (or more) |
| **Low liquidity** | 5–10% (but risky) |

> ⚠️ **Slippage too high = can be sandwich-attacked** (MEV bot front-runs you).

### MEV Protection (Anti-Bot)

```
❌ TXN visible in mempool → MEV bot knows you want to buy
   → bot front-runs, raises price
   → you get worst slippage
```

Solutions:
- Use **Jupiter RFQ mode** (private routing, no mempool leak)
- Use **Triton RPC** or **Helius Sender** (private mempool)
- For large transactions, split into multiple tx

## 🌊 Raydium

**URL:** https://raydium.io

### Swap
1. Go to https://raydium.io/swap
2. Connect wallet
3. Select token pair
4. Swap

### Add Liquidity (LP)
1. Go to https://raydium.io/liquidity-pools
2. Select pair (e.g. SOL/USDC)
3. Set price range (for CLMM)
4. Deposit tokens → get LP token
5. Stake LP token in farm for additional yield

> ⚠️ **Impermanent loss** is LP risk. Learn first before depositing large amounts.

## 🐸 Pump.fun

**URL:** https://pump.fun

Meme coin launching platform **fair launch** — everyone buys at the same price.

### How to Buy
1. Go to https://pump.fun
2. Search token (sort by trending/newest)
3. Make sure **graduation progress** → higher = closer to Raydium listing
4. Connect wallet → **Buy**
5. Sell via **Sell** button (anytime before/after graduation)

### Graduation
```
Token on pump.fun → market cap rises → graduates to Raydium
Usually when MC ~$69K → LP seeded to Raydium
```

### Pump.fun Risks
- 🚨 **Honeypot** — can buy, can't sell (rare on pump.fun but exists)
- 🚨 **Bundled buy** — one person/wallet has lots of control
- 🚨 **Dev dump after graduation**

## 🤖 Trading Bots

| Bot | Platform | Features | Cost |
|---|---|---|---|
| **Trojan** | Telegram | Sniper, copy trade, limit | 1% fee |
| **BonkBot** | Telegram | Sniper, MEV protection | 1% fee |
| **Maestro** | Telegram | Sniper, multi-wallet | 1% fee |
| **SolTradingBot** | Telegram | Advanced | Subscription |

### Trojan Setup (Example)
1. Open Telegram → search @Trojan_on_solana
2. **MUST** create new wallet for bot (Trojan generates encrypted wallet)
3. Send SOL to Trojan wallet
4. Set slippage → paste contract address → Buy

> ⚠️ **NEVER** use main wallet for bots. Create dedicated burner wallet.

## 📊 Limit Orders

**Jupiter Limit Order** = buy/sell at specific price, auto-executes.

Use case:
- Want to buy BONK at $0.000001, currently $0.0000015 → set limit buy, wait for drop
- Want take profit at 2x → set limit sell

Cost: **free** (no gas fee until executed)

URL: https://jupiter.ag/limit

## 💼 Position Sizing

> 🎯 **Most important formula:** Position size = (% capital) × (total capital)

| Risk Level | % Capital per Trade | Best for |
|---|---|---|
| 🟢 Conservative | 1–2% | Established token |
| 🟡 Moderate | 2–5% | Trending token |
| 🟠 Aggressive | 5–10% | Sniping / early |
| 🔴 YOLO | > 10% | Almost guaranteed rug |

**Example:**
- Capital: $1000
- Risk per trade (2%): **$20**
- Stop loss: -30%
- Max loss per trade: $20 → means entry no more than $66 per position

## 📋 Pre-Trade Checklist

```markdown
[ ] Token already checked (rug score ≥ 60)
[ ] Position size ≤ 5% capital
[ ] Stop loss level determined
[ ] Take profit level (multi-tier)
[ ] Slippage set reasonably (1–3% for meme)
[ ] Dedicated trading wallet (not main wallet)
[ ] Clear exit plan (time stop / target / SL)
[ ] Not under influence of FOMO / revenge trading
[ ] Stable internet connection
[ ] Well-rested (don't trade sleepy)
```

## ⚠️ Anti-Scam Trading

| Scam Tactic | How to Avoid |
|---|---|
| **Honeypot** | Test buy & sell small first before all-in |
| **Huge tax (10%+)** | Check DexScreener "Buy Tax" & "Sell Tax" |
| **Fake volume** | Volume > market cap = red flag |
| **Bundle buy** | Check holder distribution at initial listing |
| **Dev wallet dump** | Track dev wallet on Solscan |
| **Sandwich attack** | Use private mempool (Helius Sender) |

## 🔗 Next

- **[07. Tools](docs/en/07-tools/README.md)** — bots, alerts, portfolio tracker
- **[08. Tips](docs/en/08-tips/README.md)** — wisdom from experienced traders

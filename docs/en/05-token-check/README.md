# 🔍 05. Token Safety Check — Helius RPC & Tools

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/05-token-check/README.md)

> 🎯 **Trading Rule #1:** Never buy a token without checking first. 30 seconds of checking = potentially save from rug.

## 🛠️ Tools We Use

| Tool | Function | API Key | Reliability |
|---|---|---|---|
| **Helius RPC** | Check mint/freeze authority, supply, holders | Required | ⭐⭐⭐⭐⭐ |
| **DexScreener** | Check LP, volume, market cap | Free | ⭐⭐⭐⭐⭐ |
| **Solscan** | On-chain explorer | Free | ⭐⭐⭐⭐ |
| **Birdeye** | Complete analytics | Optional | ⭐⭐⭐ (often down) |
| **RugCheck.xyz** | Auto rug detection | Free | ⭐⭐⭐ (often down) |
| **Jupiter** | Real-time price check, swap route | Free | ⭐⭐⭐⭐⭐ |

> 💡 **Principle:** Helius RPC = **most reliable data source**. Birdeye/RugCheck often error — don't rely on them.

## 🔑 Setup Helius API Key (Free)

1. Go to https://dashboard.helius.dev
2. Sign up (email/Google/GitHub)
3. Free tier: **100,000 credits/day** (enough for hundreds of checks)
4. Create new API key
5. Save in environment variable:

```bash
# Temporary (current session)
export HELIUS_API_KEY="your-key-here"

# Permanent (Linux/Mac)
echo 'export HELIUS_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# Permanent (zsh)
echo 'export HELIUS_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 📡 Useful Helius Endpoints

| Endpoint | Function |
|---|---|
| `getAccountInfo` | Check mint/freeze authority (jsonParsed) |
| `getTokenSupply` | Check total token supply |
| `getTokenLargestAccounts` | Check holder distribution |
| `getTransaction` | Transaction details |
| `getSignaturesForAddress` | Wallet transaction history |
| `searchAssets` | Search token by name/symbol |
| `getAsset` | Complete token metadata |

## 🔍 What Must Be Checked (Required)

### 1. Mint Authority
```
✅ SAFE   : null  (supply cannot be increased)
🚨 DANGER : <pubkey>  (dev can mint unlimited → price drops)
```

### 2. Freeze Authority
```
✅ SAFE   : null  (token cannot be frozen)
🚨 DANGER : <pubkey>  (dev can freeze your wallet)
```

### 3. Total Supply & Decimals
```
Supply = 1,000,000,000 (1B)
Decimals = 6 → 1 token = 1,000,000 units
```

### 4. Top 10 Holders Concentration
```
✅ SAFE    : < 50%
⚠️ MEDIUM  : 50–70%
🚨 DANGER  : > 70%
```

### 5. Liquidity (DexScreener)
```
✅ SAFE    : > $50,000
⚠️ MEDIUM  : $10,000–$50,000
🚨 DANGER  : < $10,000 (vulnerable to rug)
```

### 6. LP Lock
```
✅ SAFE    : Locked for > 30 days
🚨 DANGER  : Not locked (dev can pull all)
```

## 🚀 Quick Check (30 Seconds)

Before buying a token, **MUST** run this:

```bash
# Setup once
export HELIUS_API_KEY="your-key"

# Check token
python scripts/check_token.py <MINT_ADDRESS>
```

Output example:
```
🔍 Checking token: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

✅ Mint Authority   : None (SAFE)
✅ Freeze Authority : None (SAFE)
✅ Total Supply     : 1,000,000,000
⚠️  Top 10 Holders  : 42.5% (MEDIUM)

📊 Verdict: MEDIUM RISK — DYOR further
```

## 📜 Composite Rug Score

Use **Composite Rug Score** (0–100, higher = safer):

| Factor | Weight | Safe | Dangerous |
|---|---|---|---|
| Mint Authority null | 25 | null (+25) | active (+0) |
| Freeze Authority null | 20 | null (+20) | active (+0) |
| Top 10 holders < 40% | 20 | <40% (+20) | >70% (+0) |
| Liquidity > $50K | 15 | >$50K (+15) | <$10K (+0) |
| LP Locked | 10 | Locked (+10) | Unlocked (+0) |
| Organic volume | 10 | >$10K (+10) | <$1K (+0) |

**Interpretation:**
- **80–100**: 🟢 Very safe (rare for meme coin)
- **60–79**: 🟢 Safe, DYOR
- **40–59**: 🟡 Medium risk
- **20–39**: 🟠 High risk
- **0–19**: 🔴 Don't buy (likely rug)

See full implementation: [`scripts/rug_score.py`](../../scripts/rug_score.py)

## 🐍 Python Script — `check_token.py`

Location: [`scripts/check_token.py`](../../scripts/check_token.py)

Features:
- ✅ Check mint/freeze authority via Helius
- ✅ Check total supply + decimals
- ✅ Check top 10 holders concentration
- ✅ Check LP & volume via DexScreener
- ✅ Composite rug score
- ✅ Color-coded output

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run
python scripts/check_token.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

## 🎯 Complete Workflow

```
   See trending token on Twitter / DexScreener
                  │
                  ▼
   Copy mint address
                  │
                  ▼
   Run: python scripts/check_token.py <MINT>
                  │
                  ▼
   ┌─────────── Score < 40 ─────────────┐
   │  DO NOT BUY. Find another token.   │
   └────────────────────────────────────┘
                  │
                  ▼
   ┌─────────── Score 40–79 ───────────┐
   │  DYOR further:                    │
   │  - Check real Twitter followers   │
   │  - Check Telegram activity        │
   │  - Check dev wallet history       │
   │  - Check buy/sell transactions    │
   └────────────────────────────────────┘
                  │
                  ▼
   ┌─────────── Score ≥ 80 ────────────┐
   │  ✅ BUY (but still use            │
   │  stop loss & position sizing!)    │
   └────────────────────────────────────┘
```

## ⚠️ Limitations

- ✅ Helius checks **on-chain data** (most accurate)
- ❌ Cannot detect **social engineering** (e.g. dev exit scam even with null authorities)
- ❌ Cannot predict **market crashes** or FUD

> Always combine with **fundamental analysis** (community, narrative, timing) and **technical analysis** (chart patterns, volume).

## 🔗 Next

- **[06. Trading](docs/en/06-trading/README.md)** — Jupiter, Raydium, Pump.fun
- **[07. Tools](docs/en/07-tools/README.md)** — bots, alerts, portfolio tracker

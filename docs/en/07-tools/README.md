# 🛠️ 07. Supporting Tools — Bots, Alerts, Portfolio Trackers

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/07-tools/README.md)

## 📊 Portfolio Trackers

| Tool | Platform | Features | Cost |
|---|---|---|---|
| **Solscan Portfolio** | Web | Track holdings, tx history | Free |
| **Birdeye Portfolio** | Web | P&L tracking, watchlist | Free |
| **Phantom Portfolio** | Browser | Real-time, in-wallet | Free |
| **Step Finance** | Web | Advanced analytics | Free |
| **Koinly** | Web | Tax reporting | Subscription |

### Setup Solscan Watchlist
1. Go to https://solscan.io
2. Connect wallet
3. "Portfolio" tab → see all holdings
4. "Watchlist" tab → add address to monitor

## 🔔 Alerts & Monitoring

| Service | Type | Cost |
|---|---|---|
| **DexScreener alerts** | Email/push | Free |
| **Birdeye alerts** | Telegram | Freemium |
| **Helius webhooks** | Custom | Free (with API key) |
| **Custom Discord bot** | Self-hosted | Free |

### Setup DexScreener Alert
1. Go to https://dexscreener.com/solana
2. Search your token pair
3. Click ⭐ → add to watchlist
4. Settings → enable notifications
5. Get notified when volume/MC changes significantly

### Custom Discord Alert (Helius Webhook)
See scripts: [`scripts/monitor_wallet.py`](../../../scripts/monitor_wallet.py) + [`scripts/discord_notifier.py`](../../../scripts/discord_notifier.py)

## 🤖 Popular Telegram Bots

| Bot | Strengths | Weaknesses |
|---|---|---|
| **Trojan** | Fast, sniper, copy trade | 1% fee |
| **BonkBot** | Built-in anti-MEV | Standard UI |
| **Maestro** | Multi-wallet, advanced | 1% fee |
| **Bloom** | AI auto-trading | Premium |

### Beginner Recommendation
✅ **Trojan** — friendly interface, lots of features
✅ **BonkBot** — best MEV protection

## 🧮 Tax & Reporting

> ⚠️ Crypto **is taxed** in many countries.

Tools:
- **Koinly** (https://koinly.io) — auto-import from wallet/exchange
- **CoinTracker** — alternative
- **TokenTax** — advanced

Features:
- Import CSV from Phantom/Binance
- Calculate realized gain/loss
- Generate tax report (PDF/CSV)

## 🛡️ Wallet Security Tools

| Tool | Function |
|---|---|
| **revoke.cash** | Revoke old token approvals |
| **Socket** | Bridge aggregator with security check |
| **Pocket Universe** | Browser extension — transaction preview |
| **Blowfish** | API to check transactions before signing |

### Setup Revoke.cash (Mandatory!)
1. Go to https://revoke.cash
2. Connect wallet
3. See all active approvals
4. **Revoke** unnecessary ones
5. Do this **weekly** or after many dApp interactions

### Setup Pocket Universe
1. Install extension https://www.pocketuniverse.com
2. For each transaction, Pocket Universe will **preview** what happens
3. **Cancel** if anything suspicious

## 📈 Charting & TA

| Platform | Strengths |
|---|---|
| **DexScreener** | Charts with on-chain data |
| **TradingView** | Advanced TA tools |
| **GMGN** | Smart money tracking |
| **DexCheck** | Advanced Solana charts |

### Setup TradingView Alert
1. Open chart in TradingView
2. Add indicator (RSI, MA, volume)
3. Click "Alert" (🔔)
4. Set condition (e.g. RSI > 70 → sell signal)
5. Notification via email/app

## 📱 Mobile Apps

| App | Platform | Function |
|---|---|---|
| **Phantom Mobile** | iOS/Android | Full wallet |
| **Solflare** | iOS/Android | Wallet + staking |
| **Step** | iOS/Android | Portfolio |
| **Birdeye** | iOS/Android | Charts & alerts |
| **Trojan** | Telegram | Trading bot |

## 🔍 Research Tools

| Tool | Function |
|---|---|
| **Twitter/X** | Following smart money, trending tokens |
| **Telegram groups** | Alpha calls, real-time chat |
| **GitHub** | Audit open-source smart contracts |
| **DeFiLlama** | TVL tracking |
| **Dune Analytics** | On-chain dashboards |

## 🧰 Recommended Bundles

### For Beginners (< $1000 capital)
```
✅ Phantom wallet (browser)
✅ Jupiter for swaps
✅ Solscan for monitoring
✅ DexScreener for screening
✅ Telegram: Trojan bot
✅ Browser: Pocket Universe
```

### For Active Traders
```
+ Helius RPC + custom scripts
+ Jupiter limit orders
+ Discord custom alert
+ Birdeye Pro
+ Multi-wallet setup (4 wallets)
```

### For Whales/Pro
```
+ Helius Sender (private mempool)
+ Multiple RPC endpoints (load balance)
+ Dedicated Telegram bot
+ Custom dashboard (Streamlit)
+ Koinly for taxes
```

## 📜 Custom Scripts

See folder [`scripts/`](../../../scripts/):

| Script | Function |
|---|---|
| `check_token.py` | Check token safety via Helius |
| `wallet_setup.py` | Generate encrypted wallet |
| `monitor_wallet.py` | Monitor transactions real-time |
| `lp_check.py` | Check new LPs on DexScreener |
| `rug_score.py` | Composite rug scoring |
| `discord_notifier.py` | Send alert to Discord |

## 🔗 Next

- **[08. Tips](../08-tips/README.md)** — wisdom & anti-scam
- **[Scripts](../../../scripts/README.md)** — ready-to-use automation

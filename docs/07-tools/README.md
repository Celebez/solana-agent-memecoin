# 🛠️ 07. Tools Pendukung — Bot, Alert, Portfolio Tracker

## 📊 Portfolio Tracker

| Tool | Platform | Fitur | Biaya |
|---|---|---|---|
| **Solscan Portfolio** | Web | Track holdings, tx history | Gratis |
| **Birdeye Portfolio** | Web | P&L tracking, watchlist | Gratis |
| **Phantom Portfolio** | Browser | Real-time, in-wallet | Gratis |
| **Step Finance** | Web | Advanced analytics | Gratis |
| **Koinly** | Web | Tax reporting | Subscription |

### Setup Solscan Watchlist
1. Buka https://solscan.io
2. Connect wallet
3. Tab "Portfolio" → lihat semua holdings
4. Tab "Watchlist" → tambah address yang mau dimonitor

## 🔔 Alert & Monitoring

| Service | Tipe | Harga |
|---|---|---|
| **DexScreener alerts** | Email/push | Gratis |
| **Birdeye alerts** | Telegram | Freemium |
| **Helius webhooks** | Custom | Gratis (dengan API key) |
| **Custom Discord bot** | Self-hosted | Free |

### Setup DexScreener Alert
1. Buka https://dexscreener.com/solana
2. Cari pair token Anda
3. Klik ⭐ → add to watchlist
4. Settings → enable notifications
5. Notif masuk saat volume/MC berubah signifikan

### Custom Discord Alert (Helius Webhook)
Lihat script: [`scripts/monitor_wallet.py`](../scripts/monitor_wallet.py) + [`scripts/discord_notifier.py`](../scripts/discord_notifier.py)

## 🤖 Bot Telegram Populer

| Bot | Kelebihan | Kekurangan |
|---|---|---|
| **Trojan** | Cepat, sniper, copy trade | 1% fee |
| **BonkBot** | Anti-MEV built-in | UI standar |
| **Maestro** | Multi-wallet, advanced | 1% fee |
| **Bloom** | Trading otomatis AI | Premium |

### Rekomendasi Pemula
✅ **Trojan** — interface ramah, banyak fitur
✅ **BonkBot** — MEV protection terbaik

## 🧮 Tax & Reporting

> ⚠️ Crypto **kena pajak** di banyak negara (termasuk Indonesia untuk aset kripto terdaftar di Bappebti).

Tools:
- **Koinly** (https://koinly.io) — auto-import dari wallet/exchange
- **CoinTracker** — alternatif
- **TokenTax** — advanced

Fitur:
- Import CSV dari Phantom/Binance
- Hitung realized gain/loss
- Generate tax report (PDF/CSV)

## 🛡️ Wallet Security Tools

| Tool | Fungsi |
|---|---|
| **revoke.cash** | Cabut token approval lama |
| **Socket** | Bridge aggregator dengan security check |
| **Pocket Universe** | Browser extension — preview transaksi |
| **Blowfish** | API untuk cek transaksi sebelum sign |

### Setup Revoke.cash (Wajib!)
1. Buka https://revoke.cash
2. Connect wallet
3. Lihat semua approval aktif
4. **Revoke** yang tidak perlu
5. Lakukan **mingguan** atau setelah banyak interaksi dApp

### Setup Pocket Universe
1. Install extension https://www.pocketuniverse.com
2. Setiap transaksi, Pocket Universe akan **preview** apa yang terjadi
3. **Cancel** kalau ada hal mencurigakan

## 📈 Charting & TA

| Platform | Kelebihan |
|---|---|
| **DexScreener** | Chart dengan on-chain data |
| **TradingView** | Advanced TA tools |
| **GMGN** | Smart money tracking |
| **DexCheck** | Advanced chart Solana |

### Setup TradingView Alert
1. Buka chart di TradingView
2. Add indicator (RSI, MA, volume)
3. Klik "Alert" (🔔)
4. Set kondisi (mis. RSI > 70 → sell signal)
5. Notifikasi via email/app

## 📱 Mobile Apps

| App | Platform | Fungsi |
|---|---|---|
| **Phantom Mobile** | iOS/Android | Full wallet |
| **Solflare** | iOS/Android | Wallet + staking |
| **Step** | iOS/Android | Portfolio |
| **Birdeye** | iOS/Android | Charts & alerts |
| **Trojan** | Telegram | Trading bot |

## 🔍 Research Tools

| Tool | Fungsi |
|---|---|
| **Twitter/X** | Following smart money, trending tokens |
| **Telegram groups** | Alpha calls, real-time chat |
| **GitHub** | Audit open-source smart contract |
| **DeFiLlama** | TVL tracking |
| **Dune Analytics** | On-chain dashboards |

## 🧰 Bundel Rekomendasi

### Untuk Pemula (< $1000 modal)
```
✅ Phantom wallet (browser)
✅ Jupiter untuk swap
✅ Solscan untuk monitoring
✅ DexScreener untuk screening
✅ Telegram: Trojan bot
✅ Browser: Pocket Universe
```

### Untuk Trader Aktif
```
+ Helius RPC + custom scripts
+ Limit order Jupiter
+ Discord custom alert
+ Birdeye Pro
+ Multi-wallet setup (4 wallets)
```

### Untuk Whale/Pro
```
+ Helius Sender (private mempool)
+ Multiple RPC endpoints (load balance)
+ Dedicated Telegram bot
+ Custom dashboard (Streamlit)
+ Koinly untuk tax
```

## 📜 Script Kustom

Lihat folder [`scripts/`](../scripts/):

| Script | Fungsi |
|---|---|
| `check_token.py` | Cek safety token via Helius |
| `wallet_setup.py` | Generate wallet ter-enkripsi |
| `monitor_wallet.py` | Monitor transaksi real-time |
| `lp_check.py` | Cek LP baru di DexScreener |
| `rug_score.py` | Composite rug scoring |
| `discord_notifier.py` | Kirim alert ke Discord |

## 🔗 Lanjut

- **[08. Tips](docs/08-tips/README.md)** — wisdom & anti-scam
- **[Scripts](../scripts/README.md)** — automasi siap pakai

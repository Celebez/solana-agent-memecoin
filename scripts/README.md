# 🐍 Scripts Otomatis — Katalog Lengkap

Kumpulan **17 script Python siap pakai** untuk workflow Solana & meme coin trading — dari screening token sampai tax reporting.

## 📋 Daftar Lengkap

| # | Script | Fungsi | API Key | Kategori |
|---|---|---|---|---|
| 1 | `check_token.py` | Cek safety token via Helius RPC | Helius | 🛡️ Security |
| 2 | `rug_score.py` | Composite rug scoring (0-100) | Helius | 🛡️ Security |
| 3 | `revoke_approvals.py` | Cek & revoke token approval | Helius | 🛡️ Security |
| 4 | `wallet_setup.py` | Generate & encrypt wallet baru | - | 👛 Wallet |
| 5 | `monitor_wallet.py` | Monitor transaksi wallet + alert | Helius | 👁️ Monitoring |
| 6 | `multi_wallet_balance.py` | Cek SOL balance banyak wallet sekaligus | Helius | 👁️ Monitoring |
| 7 | `portfolio_tracker.py` | Multi-wallet portfolio + USD value | Helius | 💼 Portfolio |
| 8 | `watchlist_manager.py` | CRUD watchlist token ke JSON | - | ⭐ Watchlist |
| 9 | `price_alert.py` | Alert saat harga reach target | - | 🔔 Alerts |
| 10 | `whale_tracker.py` | Monitor transaksi top holders | Helius | 🐋 Tracking |
| 11 | `lp_check.py` | Cek LP baru di DexScreener | - | 🔍 Discovery |
| 12 | `swap_helper.py` | Jupiter quote + route detail | - | 💱 Trading |
| 13 | `airdrop_checker.py` | Cek eligibility airdrop protocol | Helius | 🪂 Airdrop |
| 14 | `pnl_calculator.py` | Hitung realized & unrealized P&L | - | 📊 Reporting |
| 15 | `export_tax_report.py` | Export ke Koinly/generic CSV | - | 📤 Tax |
| 16 | `discord_notifier.py` | Kirim alert ke Discord webhook | - | 📢 Notification |
| 17 | `telegram_notifier.py` | Kirim alert ke Telegram bot | - | 📢 Notification |
| 18 | `bot_runner.py` | Scheduler untuk multi-bot | - | ⏰ Automation |
| 19 | `streamlit_dashboard.py` | Web dashboard interaktif | Helius | 📊 Dashboard |

## 📦 Install

```bash
# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# API keys (opsional, hanya untuk script yang butuh)
export HELIUS_API_KEY="your-key-here"        # https://dashboard.helius.dev (free)
export DISCORD_WEBHOOK_URL="https://..."     # Discord channel webhook
export TELEGRAM_BOT_TOKEN="123456:ABC..."    # @BotFather
export TELEGRAM_CHAT_ID="123456789"          # Your chat ID
```

## 🚀 Quick Start

### 🛡️ Security & Safety
```bash
# Cek token sebelum buy
python check_token.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

# Composite rug score
python rug_score.py <MINT>

# Cek approval aktif di wallet
python revoke_approvals.py <YOUR_WALLET>
```

### 👛 Wallet Management
```bash
# Generate wallet baru ter-enkripsi
python wallet_setup.py

# Monitor transaksi wallet
python monitor_wallet.py <ADDRESS> --discord <webhook>

# Cek balance banyak wallet
python multi_wallet_balance.py <ADDR1> <ADDR2> <ADDR3> --label "Main,Cold,Trading"
```

### 💼 Portfolio & Tracking
```bash
# Track multi-wallet portfolio
python portfolio_tracker.py <ADDR1> <ADDR2> --save portfolio.json

# Manage watchlist
python watchlist_manager.py add <MINT> --label "BONK" --note "Watch breakout"
python watchlist_manager.py list
python watchlist_manager.py update <MINT> --above 0.00003
```

### 🔔 Alerts
```bash
# Price alert
python price_alert.py --mint <MINT> --above 0.001 --below 0.0005 --discord <webhook>

# Whale tracker (multi-config)
python price_alert.py --config alerts.json

# Whale tracker
python whale_tracker.py <MINT> --top 10 --interval 60 --discord <webhook>
```

### 💱 Trading & Discovery
```bash
# Jupiter swap quote
python swap_helper.py So11111111111111111111111111111111111111112 EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 1000000000

# LP baru di DexScreener
python lp_check.py --min-liquidity 10000 --max-age-hours 6
```

### 🪂 Airdrops
```bash
# Cek eligibility
python airdrop_checker.py <YOUR_WALLET> --protocols jupiter,tensor,drift
```

### 📊 Reporting & Tax
```bash
# Hitung P&L dari CSV trades
python pnl_calculator.py trades.csv

# Export ke Koinly
python export_tax_report.py --input trades.csv --format koinly --output 2026.csv
```

### ⏰ Automation
```bash
# Run multiple bots with scheduler
python bot_runner.py --config bot_config.json

# Streamlit dashboard
streamlit run streamlit_dashboard.py
# → buka http://localhost:8501
```

## 🗂️ Use Case Workflows

### 🔍 Workflow 1: Screening Token Baru
```bash
# 1. Lihat LP baru
python lp_check.py --min-liquidity 5000 --max-age-hours 12

# 2. Untuk setiap token menarik, cek safety
python check_token.py <MINT>

# 3. Kalau skor bagus, tambah ke watchlist
python watchlist_manager.py add <MINT> --label "X" --note "Trending on CT"

# 4. Set alert
python price_alert.py --mint <MINT> --above 0.001 --discord <webhook>
```

### 💼 Workflow 2: Daily Portfolio Review
```bash
# 1. Cek total portfolio
python portfolio_tracker.py <MAIN> <TRADING> <COLD> --label "Main,Trading,Cold"

# 2. Monitor whale dump risk
python whale_tracker.py <TOP_HOLDING_MINT> --top 20

# 3. Hitung P&L bulan ini
python pnl_calculator.py trades_july.csv

# 4. Export untuk tax
python export_tax_report.py --input trades_july.csv --format koinly --output koinly_july.csv
```

### 🚨 Workflow 3: 24/7 Monitoring
```bash
# Buat bot_config.json:
cat > bot_config.json <<EOF
{
  "bots": [
    {"name": "whale", "script": "whale_tracker.py", "args": ["<MINT>", "--top", "10", "--interval", "60"], "interval": null},
    {"name": "price", "script": "price_alert.py", "args": ["--mint", "<MINT>", "--above", "0.001"], "interval": null},
    {"name": "approval-check", "script": "revoke_approvals.py", "args": ["<WALLET>"], "interval": 3600}
  ]
}
EOF

# Run semua
python bot_runner.py --config bot_config.json
```

## ⚠️ Keamanan

- ✅ **JANGAN** commit file wallet `*.json` ke git (sudah di .gitignore)
- ✅ **JANGAN** share passphrase ke siapapun
- ✅ File wallet ter-enkripsi dengan AES-256-GCM
- ✅ Test wallet dengan nominal kecil dulu
- ⚠️ Streamlit dashboard = **JANGAN di-expose publik tanpa auth**

## 🧪 Testing

```bash
cd scripts
PYTHONPATH=. pytest tests/ -v
```

Lihat [`tests/`](tests/) untuk unit tests.

## 📚 Dokumentasi Detail

Lihat folder [`docs/en/07-tools/`](../docs/en/07-tools/README.md) atau [`docs/id/07-tools/`](../docs/id/07-tools/README.md) untuk penjelasan lengkap setiap tools dan workflow.

---

⚠️ **DISCLAIMER:** Semua script untuk edukasi & otomasi. **Tidak ada jaminan profit.** Selalu DYOR.

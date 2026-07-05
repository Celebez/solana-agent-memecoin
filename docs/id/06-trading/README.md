# 💱 06. Trading — Beli/Jual di Jupiter, Raydium, Pump.fun

## 🏛️ DEX Utama di Solana

| DEX | Volume | Kelebihan | Kekurangan |
|---|---|---|---|
| **Jupiter** | Aggregator #1 | Best price routing | Eksekusi via DEX lain |
| **Raydium** | Tinggi | Likuiditas dalam, AMM v4 | UI kurang intuitif |
| **Orca** | Sedang | Concentrated liquidity | Pair terbatas |
| **Meteora** | Sedang | DLMM, advanced LP | Butuh pemahaman |
| **Pump.fun** | Sangat tinggi | Launchpad meme coin | Risiko tinggi |

## 🌐 Jupiter (Aggregator)

**URL:** https://jupiter.ag

Kenapa pakai Jupiter:
- ✅ **Best price** — auto-route ke DEX dengan harga terbaik
- ✅ **Limit order** (gratis)
- ✅ **DCA** (Dollar-Cost Averaging)
- ✅ **Perpetuals** (leverage trading)

### Cara Swap

1. Buka https://jupiter.ag
2. Connect wallet (Phantom/Solflare)
3. Pilih **From**: SOL/USDC
4. Pilih **To**: token yang ingin dibeli
5. Set **slippage** (default 0.5%, naikkan ke 1–3% untuk meme coin)
6. Klik **Swap** → konfirmasi di wallet

### Slippage Guide

| Situasi | Recommended Slippage |
|---|---|
| **Token likuid (SOL, USDC, BONK)** | 0.1–0.5% |
| **Token trending** | 1–2% |
| **Sniping baru launch** | 3–5% (atau lebih) |
| **Low liquidity** | 5–10% (tapi riskan) |

> ⚠️ **Slippage terlalu tinggi = bisa di-sandwich attack** (MEV bot front-run Anda).

### MEV Protection (Anti-Bot)

```
❌ TXN terlihat di mempool → MEV bot tahu Anda mau beli
   → bot front-run, naikkan harga
   → Anda dapat slippage terburuk
```

Solusi:
- Pakai **Jupiter RFQ mode** (private routing, tidak bocor ke mempool)
- Pakai **Triton RPC** atau **Helius Sender** (private mempool)
- Untuk transaksi besar, pecah jadi beberapa tx

## 🌊 Raydium

**URL:** https://raydium.io

### Swap
1. Buka https://raydium.io/swap
2. Connect wallet
3. Pilih token pair
4. Swap

### Add Liquidity (LP)
1. Buka https://raydium.io/liquidity-pools
2. Pilih pair (mis. SOL/USDC)
3. Set range harga (untuk CLMM)
4. Deposit token → dapat LP token
5. Stake LP token di farm untuk yield tambahan

> ⚠️ **Impermanent loss** adalah risiko LP. Pelajari dulu sebelum deposit besar.

## 🐸 Pump.fun

**URL:** https://pump.fun

Platform launching meme coin **fair launch** — semua orang beli di harga yang sama.

### Cara Beli
1. Buka https://pump.fun
2. Cari token (sort by trending/newest)
3. Pastikan **graduation progress** → semakin tinggi semakin dekat listing Raydium
4. Connect wallet → **Buy**
5. Jual via **Sell** button (kapan saja sebelum/sesudah graduation)

### Graduation
```
Token di pump.fun → market cap naik → graduasi ke Raydium
Biasanya saat MC ~$69K → LP di-seed ke Raydium
```

### Resiko Pump.fun
- 🚨 **Honeypot** — bisa beli, tidak bisa jual (jarang di pump.fun, tapi ada)
- 🚨 **Bundled buy** — 1 orang/wallet banyak kontrol
- 🚨 **Dev dump setelah graduation**

## 🤖 Trading Bot

| Bot | Platform | Fitur | Biaya |
|---|---|---|---|
| **Trojan** | Telegram | Sniper, copy trade, limit | 1% fee |
| **BonkBot** | Telegram | Sniper, MEV protection | 1% fee |
| **Maestro** | Telegram | Sniper, multi-wallet | 1% fee |
| **SolTradingBot** | Telegram | Advanced | Subscription |

### Setup Trojan (Contoh)
1. Buka Telegram → cari @Trojan_on_solana
2. **WAJIB** buat wallet baru khusus bot (Trojan generates encrypted wallet)
3. Kirim SOL ke wallet Trojan
4. Set slippage → paste contract address → Buy

> ⚠️ **TIDAK PERNAH** pakai wallet utama untuk bot. Buat wallet burner khusus.

## 📊 Limit Orders

**Jupiter Limit Order** = beli/jual di harga tertentu, otomatis eksekusi.

Use case:
- Mau beli BONK di $0.000001, sekarang $0.0000015 → set limit buy, tunggu turun
- Mau take profit di 2x → set limit sell

Biaya: **gratis** (tidak ada gas fee sampai tereksekusi)

URL: https://jupiter.ag/limit

## 💼 Position Sizing

> 🎯 **Rumus paling penting:** Position size = (% modal) × (total modal)

| Risk Level | % Modal per Trade | Cocok untuk |
|---|---|---|
| 🟢 Konservatif | 1–2% | Established token |
| 🟡 Moderat | 2–5% | Trending token |
| 🟠 Agresif | 5–10% | Sniping / early |
| 🔴 YOLO | > 10% | Hampir pasti rug |

**Contoh:**
- Modal: $1000
- Risk per trade (2%): **$20**
- Stop loss: -30%
- Max loss per trade: $20 → artinya entry tidak lebih dari $66 per position

## 📋 Pre-Trade Checklist

```markdown
[ ] Token sudah dicek (rug score ≥ 60)
[ ] Position size ≤ 5% modal
[ ] Stop loss level ditentukan
[ ] Take profit level (multi-tier)
[ ] Slippage diset合理 (1–3% untuk meme)
[ ] Wallet khusus trading (bukan main wallet)
[ ] Exit plan jelas (time stop / target / SL)
[ ] Tidak dalam pengaruh FOMO / revenge trading
[ ] Koneksi internet stabil
[ ] Sudah istirahat cukup (jangan trade ngantuk)
```

## ⚠️ Anti-Scam Trading

| Taktik Scam | Cara Hindari |
|---|---|
| **Honeypot** | Test buy & sell kecil dulu sebelum all-in |
| **Huge tax** (10%+)** | Cek di DexScreener "Buy Tax" & "Sell Tax" |
| **Fake volume** | Volume > market cap = red flag |
| **Bundle buy** | Cek distribusi holder di awal listing |
| **Dev wallet dump** | Track dev wallet di Solscan |
| **Sandwich attack** | Pakai private mempool (Helius Sender) |

## 🔗 Lanjut

- **[07. Tools](../07-tools/README.md)** — bot, alert, portfolio tracker
- **[08. Tips](../08-tips/README.md)** — wisdom dari trader berpengalaman

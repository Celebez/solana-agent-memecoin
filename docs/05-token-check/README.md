# 🔍 05. Token Safety Check — Helius RPC & Tools

> 🎯 **Aturan #1 Trading:** Jangan buy token tanpa cek dulu. 30 detik cek = hemat potencialmente rug.

## 🛠️ Tools yang Kita Gunakan

| Tool | Fungsi | API Key | Reliability |
|---|---|---|---|
| **Helius RPC** | Cek mint/freeze authority, supply, holders | Wajib | ⭐⭐⭐⭐⭐ |
| **DexScreener** | Cek LP, volume, market cap | Gratis | ⭐⭐⭐⭐⭐ |
| **Solscan** | Explorer on-chain | Gratis | ⭐⭐⭐⭐ |
| **Birdeye** | Analytics lengkap | Optional | ⭐⭐⭐ (sering down) |
| **RugCheck.xyz** | Auto rug detection | Gratis | ⭐⭐⭐ (sering down) |
| **Jupiter** | Cek harga real-time, swap route | Gratis | ⭐⭐⭐⭐⭐ |

> 💡 **Prinsip:** Helius RPC = **sumber data paling reliable**. Birdeye/RugCheck sering error — jangan diandalkan.

## 🔑 Setup Helius API Key (Gratis)

1. Buka https://dashboard.helius.dev
2. Sign up (email/Google/GitHub)
3. Free tier: **100,000 credits/hari** (cukup untuk ratusan cek)
4. Buat API key baru
5. Simpan di environment variable:

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

## 📡 Endpoint Helius yang Berguna

| Endpoint | Fungsi |
|---|---|
| `getAccountInfo` | Cek mint/freeze authority (jsonParsed) |
| `getTokenSupply` | Cek total supply token |
| `getTokenLargestAccounts` | Cek distribusi holder |
| `getTransaction` | Detail transaksi |
| `getSignaturesForAddress` | History transaksi wallet |
| `searchAssets` | Cari token by name/symbol |
| `getAsset` | Metadata lengkap token |

## 🔍 Yang Harus Dicek (Wajib)

### 1. Mint Authority
```
✅ AMAN  : null  (supply tidak bisa ditambah)
🚨 BAHAYA: <pubkey>  (dev bisa mint unlimited → harga turun)
```

### 2. Freeze Authority
```
✅ AMAN  : null  (token tidak bisa di-freeze)
🚨 BAHAYA: <pubkey>  (dev bisa freeze wallet Anda)
```

### 3. Total Supply & Decimals
```
Supply = 1,000,000,000 (1B)
Decimals = 6 → 1 token = 1,000,000 unit
```

### 4. Top 10 Holders Concentration
```
✅ AMAN  : < 50%
⚠️ RISIKO: 50–70%
🚨 BAHAYA: > 70%
```

### 5. Liquidity (DexScreener)
```
✅ AMAN  : > $50,000
⚠️ RISIKO: $10,000–$50,000
🚨 BAHAYA: < $10,000 (rentan rug)
```

### 6. LP Lock
```
✅ AMAN  : Locked untuk > 30 hari
🚨 BAHAYA: Tidak di-lock (dev bisa tarik semua)
```

## 🚀 Quick Check (30 Detik)

Sebelum buy token, **WAJIB** jalankan ini:

```bash
# Setup sekali
export HELIUS_API_KEY="your-key"

# Cek token
python scripts/check_token.py <MINT_ADDRESS>
```

Output contoh:
```
🔍 Checking token: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

✅ Mint Authority   : None (AMAN)
✅ Freeze Authority : None (AMAN)
✅ Total Supply     : 1,000,000,000
⚠️  Top 10 Holders  : 42.5% (SEDANG)

📊 Verdict: RISIKO SEDANG — DYOR lebih lanjut
```

## 📜 Composite Rug Score

Gunakan **Composite Rug Score** (0–100, makin tinggi makin aman):

| Faktor | Bobot | Aman | Bahaya |
|---|---|---|---|
| Mint Authority null | 25 | null (+25) | aktif (+0) |
| Freeze Authority null | 20 | null (+20) | aktif (+0) |
| Top 10 holders < 40% | 20 | <40% (+20) | >70% (+0) |
| Liquidity > $50K | 15 | >$50K (+15) | <$10K (+0) |
| LP Locked | 10 | Locked (+10) | Unlocked (+0) |
| Volume organik | 10 | >$10K (+10) | <$1K (+0) |

**Interpretasi:**
- **80–100**: 🟢 Sangat aman (rare untuk meme coin)
- **60–79**: 🟢 Aman, DYOR
- **40–59**: 🟡 Risiko sedang
- **20–39**: 🟠 Risiko tinggi
- **0–19**: 🔴 Jangan beli (kemungkinan rug)

Lihat implementasi lengkap: [`scripts/rug_score.py`](../scripts/rug_score.py)

## 🐍 Script Python — `check_token.py`

Lokasi: [`scripts/check_token.py`](../scripts/check_token.py)

Fitur:
- ✅ Cek mint/freeze authority via Helius
- ✅ Cek total supply + decimals
- ✅ Cek top 10 holders concentration
- ✅ Cek LP & volume via DexScreener
- ✅ Composite rug score
- ✅ Output warna-warni (color-coded)

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run
python scripts/check_token.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

## 🎯 Workflow Lengkap

```
   Lihat token trending di Twitter / DexScreener
                  │
                  ▼
   Copy mint address
                  │
                  ▼
   Jalankan: python scripts/check_token.py <MINT>
                  │
                  ▼
   ┌─────────── Skor < 40 ────────────┐
   │  JANGAN BUY. Cari token lain.    │
   └──────────────────────────────────┘
                  │
                  ▼
   ┌─────────── Skor 40–79 ──────────┐
   │  DYOR lebih lanjut:             │
   │  - Cek Twitter followers real   │
   │  - Cek Telegram activity        │
   │  - Cek dev wallet history       │
   │  - Cek transaksi buy/sell       │
   └──────────────────────────────────┘
                  │
                  ▼
   ┌─────────── Skor ≥ 80 ───────────┐
   │  ✅ BUY (tapi tetap pakai       │
   │  stop loss & position sizing!)  │
   └──────────────────────────────────┘
```

## ⚠️ Limitasi

- ✅ Helius cek **data on-chain** (paling akurat)
- ❌ Tidak bisa deteksi **social engineering** (mis. dev exit scam padahal authorities null)
- ❌ Tidak bisa prediksi **market crash** atau FUD

> Selalu kombinasikan dengan **analisis fundamental** (komunitas, narasi, timing) dan **analisis teknikal** (chart pattern, volume).

## 🔗 Lanjut

- **[06. Trading](docs/06-trading/README.md)** — Jupiter, Raydium, Pump.fun
- **[07. Tools](docs/07-tools/README.md)** — bot, alert, portfolio tracker

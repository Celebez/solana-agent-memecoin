# 🐸 04. Memecoin — Anatomi, Risiko & Peluang

## Definisi

**Memecoin** = token kripto dengan **utility intrinsik minimal/nol**, valuasinya ditentukan oleh:

- 🤝 Kekuatan komunitas
- 😂 Meme / internet culture
- 📈 Hype & momentum
- 🐋 Whales (holder besar)
- 🎯 Timing listing di CEX (Binance, Coinbase, dll.)

## 🧬 Anatomi Token Solana

Setiap token SPL (Solana Program Library) punya metadata:

```
Mint Address  : 7xKXtg... (identitas unik token)
Decimals      : 6 / 9 / 18 (presisi)
Supply        : 1,000,000,000 (1B)
Authorities   :
  - Mint Authority    : siapa yang boleh tambah supply
  - Freeze Authority  : siapa yang boleh freeze token holder
Metadata      : nama, simbol, logo URI
```

> ⚠️ **Mint Authority aktif = bahaya**. Bisa di-mint unlimited → suplai naik → harga turun.
> ⚠️ **Freeze Authority aktif = bahaya**. Bisa freeze wallet Anda → tidak bisa jual.

## 📊 Lifecycle Memecoin

```
       ┌──────────┐
       │  Launch  │   ← Token baru, supply di LP
       └─────┬────┘
             ▼
       ┌──────────┐
       │   Pump   │   ← Hype naik, FOMO masuk
       └─────┬────┘
             ▼
       ┌──────────┐
       │  Peak    │   ← ATH, waktu EXIT
       └─────┬────┘
             ▼
       ┌──────────┐
       │   Dump   │   ← Whale keluar, retail rugi
       └─────┬────┘
             ▼
       ┌──────────┐
       │Recovery  │   ← Stabil di low, atau rug = 0
       └──────────┘
```

**Tujuan Anda:** Beli di Pump awal, jual sebelum Peak.

## 🎭 Jenis Meme Coin Berdasarkan Origin

### 1. 🐶 Established Memecoin
Contoh: BONK, WIF, POPCAT, MEW
- Sudah listing di CEX besar
- Likuiditas tinggi, lebih stabil
- Pertumbuhan lebih lambat (~5–50x)

### 2. 🔥 Trending Token
Contoh: token yang viral di Twitter/X
- Naik cepat 50–500x dalam jam
- Risiko tinggi, butuh timing presisi
- Volatilitas ekstrem

### 3. 💩 Microcap
Contoh: token baru dari pump.fun
- Market cap < $100K
- Risiko rug pull SANGAT tinggi
- Potensi 1000x tapi 99% rug

## 🏛️ Platform Launching

| Platform | Mekanisme | Risiko | Contoh |
|---|---|---|---|
| **pump.fun** | Fair launch, bonding curve | Sedang | DOGE20, MEW |
| **Raydium** | DEX, LP harus disediakan | Rendah-Sedang | Token baru |
| **Orca** | DEX, fokus di Solana DeFi | Rendah | Token baru |
| **Meteora** | Dynamic AMM | Sedang | DLMM pairs |
| **Jupiter Studio** | Token launchpad | Sedang | JUP token |

## 💡 Strategi Entry

### A. Sniping (Detik Pertama)
- Beli **< 30 detik** setelah launch
- Butuh **bot** (Trojan, BonkBot, Maestro)
- Risiko sangat tinggi (honeypot, dev dump)

### B. Early Trending (Menit ke Jam)
- Beli saat mulai trending di Twitter/DexScreener
- Lebih aman, masih bisa 10–100x
- Butuh monitoring real-time

### C. Breakout Trading
- Tunggu konfirmasi volume + community
- Entry saat pullback/retest support
- Risk/reward lebih baik, tapi upside lebih kecil

## 📈 Strategi Exit

> 🎯 **Exit plan lebih penting dari entry plan.**

### 1. 🎯 Profit Target
| Profit | Action |
|---|---|
| **+100% (2x)** | Take out modal awal |
| **+300% (4x)** | Take 50% profit |
| **+1000% (10x)** | Take 70–80% |
| **+10000% (100x)** | Sisa 1–5% "moon bag" |

### 2. 🛑 Stop Loss
- **Hard stop** di -30% sampai -50% (tergantung volatilitas)
- Pakai mental stop, **JANGAN** titip di exchange (rug pull instant)

### 3. ⏰ Time Stop
- Setelah 1–2 minggu **tidak ada catalyst** → cut loss
- "Dead cat bounce" bisa terjadi tapi jarang

## 📊 Metrik Penting untuk Watch

| Metrik | Sumber | Apa artinya |
|---|---|---|
| **Market Cap** | DexScreener | Valuasi total token |
| **FDV** | DexScreener | Valuasi kalau semua token dilepas |
| **Liquidity** | DexScreener | Berapa SOL/USDC di LP |
| **Holders** | Solscan | Jumlah unique wallet |
| **Top 10 holders %** | Solscan | Konsentrasi (bahaya jika >50%) |
| **Volume 24h** | DexScreener | Seberapa aktif trading |
| **Buy/Sell ratio** | Birdeye | Sentimen real-time |

## ⚠️ Tanda Pasti Rug Pull

```
🚩 1. Liquidity < $5,000
🚩 2. Top 10 holders > 60%
🚩 3. Mint authority masih aktif
🚩 4. Freeze authority masih aktif
🚩 5. Dev wallet > 20% supply
🚩 6. Volume drop > 90% dalam 1 jam
🚩 7. Social channels dibuat < 1 minggu lalu
🚩 8. Team anonymous + no audit
🚩 9. "Don't sell, we'll moon together" — padahal devs sedang jual
🚩 10. Token contract tidak verified
```

## 📚 Checklist Sebelum Buy

```markdown
[ ] Mint authority: NONE
[ ] Freeze authority: NONE  
[ ] Top 10 holders < 50%
[ ] Liquidity > $50,000 dan locked
[ ] Dev wallet < 10% supply
[ ] Volume organik (bukan wash trading)
[ ] Social proof (Twitter followers real, Telegram aktif)
[ ] Tidak ada di scam database (RugCheck, Chainabuse)
[ ] Anda bisa afford 100% loss
[ ] Exit plan jelas
```

## 🔗 Lanjut

- **[05. Token Safety Check](../05-token-check/README.md)** — cek dengan Helius RPC + script
- **[06. Trading](../06-trading/README.md)** — Jupiter, Raydium, Pump.fun

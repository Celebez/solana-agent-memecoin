# 👛 02. Wallet Solana — Jenis & Cara Pilih

## Apa itu Wallet?

**Wallet** adalah aplikasi yang menyimpan **private key** Anda. Private key = akses penuh ke dana di address tertentu. **Siapa yang punya private key, dia yang punya uangnya.**

```
Wallet ≠ menyimpan koin
Wallet = menyimpan KUNCI ke koin Anda di blockchain
```

## Jenis Wallet Solana

### 1. 🥇 Hot Wallet (Online)

| Wallet | Platform | Harga | Cocok untuk |
|---|---|---|---|
| **Phantom** | Browser, iOS, Android | Gratis | Pemula — paling populer |
| **Solflare** | Browser, Mobile | Gratis | Advanced, staking |
| **Backpack** | Browser, Mobile | Gratis | Multi-chain (SOL + ETH) |
| **Trust Wallet** | Mobile | Gratis | Multi-chain |
| **Exodus** | Desktop, Mobile | Gratis | UI cantik, beginner-friendly |

### 2. 🥈 Hardware Wallet (Cold Storage — PALING AMAN)

| Wallet | Harga | Level Keamanan |
|---|---|---|
| **Ledger Nano S Plus** | ~$79 | ⭐⭐⭐⭐⭐ |
| **Ledger Nano X** | ~$149 | ⭐⭐⭐⭐⭐ + Bluetooth |
| **Trezor Model T** | ~$219 | ⭐⭐⭐⭐⭐ |

### 3. 🥉 CLI Wallet (Untuk Developer)

```bash
# Solana CLI resmi
solana-keygen new --outfile ~/my-wallet.json
solana config set --keypair ~/my-wallet.json
solana balance
```

## 📊 Perbandingan Lengkap

| Aspek | Hot Wallet | Hardware Wallet | CLI |
|---|---|---|---|
| Keamanan | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Kemudahan | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Biaya | Gratis | $79–$219 | Gratis |
| Akses cepat | ✅ | ⚠️ Perlu device | ⚠️ Perlu terminal |
| Untuk trading aktif | ✅ | ❌ Terlalu lambat | ⚠️ |
| Untuk simpanan | ❌ | ✅ | ⚠️ |

## 🏆 Rekomendasi Setup Hybrid (Paling Aman untuk Trader)

```
┌────────────────────────────────────────────────┐
│  💰 Trading Wallet (Phantom) — SOL kecil       │
│  • Isi max $100–$500                           │
│  • Untuk interaksi频繁: swap, claim airdrop    │
│  • Hot wallet, tapi saldo terbatas             │
└────────────────────────────────────────────────┘
                    ↕ transfer saat perlu
┌────────────────────────────────────────────────┐
│  🏦 Cold Storage (Ledger) — SOL utama         │
│  • 80–95% dana                                 │
│  • Offline, tidak pernah connect ke dApp       │
│  • Seed phrase disimpan di lokasi fisik aman   │
└────────────────────────────────────────────────┘
```

> 💡 **Prinsip:** Hot wallet itu "dompet saku" — secukupnya. Cold storage itu "brankas" — uang utama.

## 🔧 Setup Phantom Wallet (Step-by-Step)

### Install
1. Buka https://phantom.app
2. Pilih browser (Chrome/Brave/Firefox) atau mobile
3. Klik "Download"
4. Install extension

### Buat Wallet Baru
1. Klik **"Create New Wallet"**
2. Set password (minimal 8 karakter)
3. **PENTING:** Phantom akan tampilkan **12 kata seed phrase**
   - ⚠️ Tulis di kertas (jangan screenshot!)
   - ⚠️ Simpan di 2+ lokasi aman
   - ⚠️ JANGAN bagikan ke SIAPAPUN
4. Konfirmasi urutan kata

### Verifikasi
1. Buka https://solscan.io
2. Copy address Anda
3. Paste di Phantom (klik nama wallet di atas)
4. Pastikan address cocok

### Fund Wallet
1. Beli SOL di exchange (Binance, Indodax, dll.)
2. Withdraw ke address Phantom Anda
3. Tunggu 1–3 menit konfirmasi
4. Saldo muncul di Phantom

## 🆚 Ledger Setup (Ringkas)

1. Beli **Ledger** di situs resmi (HATI-HATI fake!)
2. Install **Ledger Live** di desktop
3. Init device → set PIN → **catat 24 kata recovery**
4. Install **Solana app** di Ledger
5. Buka Phantom → Settings → "Connect Hardware Wallet" → Ledger
6. Address Anda: Phantom `XXXX...XXX` (tetap, sama seperti native)

## ❌ Kesalahan Umum Pemula

- ❌ Simpan seed di Notes HP / screenshot
- ❌ Pakai wallet yang sama untuk "coba-coba" airdrop scam
- ❌ Connect wallet ke situs tidak dikenal
- ❌ Simpan semua dana di hot wallet
- ❌ Lupa test wallet recovery dengan nominal kecil dulu

## 🔗 Lanjut

- **[03. Keamanan](../03-security/README.md)** — best practice wajib
- **[04. Memecoin](../04-memecoin/README.md)** — anatomi & peluang

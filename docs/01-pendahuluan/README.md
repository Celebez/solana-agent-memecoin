# 📖 01. Pendahuluan — Apa itu Solana & Meme Coin?

## 🟣 Apa itu Solana?

**Solana** adalah blockchain Layer-1 berkinerja tinggi yang launched pada 2020 oleh Anatoly Yakovenko. Dikenal sebagai "Ethereum killer" karena:

| Fitur | Ethereum | Solana |
|---|---|---|
| Throughput | ~15 TPS | ~65.000 TPS |
| Biaya transaksi | $1–$50 | $0.0001–$0.01 |
| Block time | ~12 detik | ~400 ms |
| Bahasa smart contract | Solidity | Rust / Anchor |

> 💡 **TPS = Transactions Per Second.** Solana secara teori bisa 65.000, Ethereum cuma 15. Itulah kenapa Solana jadi rumah favorit meme coin.

## 🌐 Arsitektur Singkat

```
┌─────────────────────────────────────────┐
│  Wallet (Phantom, Solflare, Backpack)   │
│         ↓ signed transaction            │
│  RPC Node (Helius, QuickNode, Triton)   │
│         ↓                               │
│  Validator Network (PoS + PoH)          │
│         ↓                               │
│  Programs (Jupiter, Raydium, Pump.fun)  │
│         ↓                               │
│  State update → confirmed ~400 ms       │
└─────────────────────────────────────────┘
```

- **Wallet** = aplikasi yang pegang private key kamu (bukan uangnya)
- **RPC Node** = "pintu" ke blockchain, baca/tulis data
- **Validator** = komputer yang jalankan konsensus
- **Programs** = smart contract (DEX, lending, dll)

## 🐸 Apa itu Meme Coin?

**Meme coin** = cryptocurrency yang lahir dari internet culture/lelucon, **tidak punya utility intrinsik**. Valuasinya murni dari:

- 🎭 **Hype & komunitas**
- 🐸 **Karakter/lelucon** (Dogecoin → Shiba → Bonk → Pepe)
- 📈 **Spekulasi & timing**
- 👥 **Holder count & social sentiment**

### Contoh Meme Coin Populer

| Token | Lahir | Tema | ATH Market Cap |
|---|---|---|---|
| DOGE | 2013 | Doge meme | ~$95B |
| SHIB | 2020 | "Dogecoin killer" | ~$40B |
| BONK | 2022 | First SOL dog | ~$3B |
| WIF | 2023 | Dog with hat | ~$4B |
| PEPE | 2023 | Pepe the Frog | ~$1.8B |
| PUMP | 2024 | Pump.fun meta | ~$1B |

## 🎯 Kenapa Orang Trading Meme Coin?

1. **100x–1000x potential** — bisa naik drastis dalam hitungan jam
2. **Low barrier** — modal kecil ($10–$50) sudah bisa mulai
3. **Komunitas solid** — Discord/Twitter ramai, ada "alpha group"
4. **Sensasi adrenalin** — jujur aja, seru 😄

## ⚠️ Kenapa 90% Rugi?

Tapi realitanya:
- 🚨 **Rug pull** — dev tarik likuiditas, token → 0
- 🎭 **Honeypot** — bisa beli, tidak bisa jual
- 📉 **Dump setelah pump** — insider exit, retail tertinggal
- 💸 **Impermanent loss** di LP
- 🧠 **FOMO & revenge trading**

> 🎯 **Target repo ini:** supaya Anda ada di **10% sisanya** yang menang.

## 📊 Mental Model: Meme Coin Lifecycle

```
   Fase 1          Fase 2          Fase 3         Fase 4
   Launch          Hype            Peak           Dump
     │               │               │              │
   ●───────●─────────●─────●─────────●─────●────────●────
   $0.0001         $0.001         $0.01         $0.0001
   
   🟢 Entry         🟡 Hold         🔴 Exit        ⚫ Rug
   terbaik         berisiko        WAKTUNYA       biasanya
```

**Kunci:** Masuk di Fase 1–2, keluar di Fase 3.

## 📚 Topik Lanjutan

Lanjut ke:
- **[02. Wallet Solana](docs/02-wallet/README.md)** — jenis wallet & cara pilih
- **[03. Keamanan](docs/03-keamanan/README.md)** — best practice wajib

---

**Disclaimer:** Bukan saran finansial. Risiko ditanggung masing-masing.

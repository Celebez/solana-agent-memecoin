# 📖 01. Introduction — What is Solana & Meme Coin?

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../id/01-introduction/README.md)

## 🟣 What is Solana?

**Solana** is a high-performance Layer-1 blockchain launched in 2020 by Anatoly Yakovenko. Known as the "Ethereum killer" because:

| Feature | Ethereum | Solana |
|---|---|---|
| Throughput | ~15 TPS | ~65,000 TPS |
| Transaction fees | $1–$50 | $0.0001–$0.01 |
| Block time | ~12 seconds | ~400 ms |
| Smart contract language | Solidity | Rust / Anchor |

> 💡 **TPS = Transactions Per Second.** Solana can theoretically do 65,000, Ethereum only 15. That's why Solana is the meme coin capital.

## 🌐 Architecture Overview

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

- **Wallet** = app that holds your private key (not the coins)
- **RPC Node** = gateway to blockchain, read/write data
- **Validator** = computer running consensus
- **Programs** = smart contracts (DEX, lending, etc.)

## 🐸 What is a Meme Coin?

**Meme coin** = cryptocurrency born from internet culture/jokes, **with no intrinsic utility**. Its value comes purely from:

- 🎭 **Hype & community**
- 🐸 **Memes / characters** (Dogecoin → Shiba → Bonk → Pepe)
- 📈 **Speculation & timing**
- 👥 **Holder count & social sentiment**

### Popular Meme Coin Examples

| Token | Born | Theme | ATH Market Cap |
|---|---|---|---|
| DOGE | 2013 | Doge meme | ~$95B |
| SHIB | 2020 | "Dogecoin killer" | ~$40B |
| BONK | 2022 | First SOL dog | ~$3B |
| WIF | 2023 | Dog with hat | ~$4B |
| PEPE | 2023 | Pepe the Frog | ~$1.8B |
| PUMP | 2024 | Pump.fun meta | ~$1B |

## 🎯 Why People Trade Meme Coins?

1. **100x–1000x potential** — can spike drastically in hours
2. **Low barrier** — small capital ($10–$50) is enough to start
3. **Solid community** — Discord/Twitter active, "alpha groups"
4. **Adrenaline rush** — honestly, it's fun 😄

## ⚠️ Why 90% Lose Money?

But reality:
- 🚨 **Rug pull** — devs drain liquidity, token → 0
- 🎭 **Honeypot** — can buy, can't sell
- 📉 **Dump after pump** — insiders exit, retail left behind
- 💸 **Impermanent loss** in LP
- 🧠 **FOMO & revenge trading**

> 🎯 **Goal of this repo:** make sure you're in the **remaining 10%** that wins.

## 📊 Mental Model: Meme Coin Lifecycle

```
   Phase 1          Phase 2          Phase 3         Phase 4
   Launch          Hype             Peak            Dump
     │               │               │              │
   ●───────●─────────●─────●─────────●─────●────────●────
   $0.0001         $0.001         $0.01         $0.0001
   
   🟢 Entry         🟡 Hold         🔴 Exit         ⚫ Rug
   best time        risky            TIME            usually
```

**Key:** Enter Phase 1–2, exit at Phase 3.

## 📚 Next Topics

Continue to:
- **[02. Solana Wallet](docs/en/02-wallet/README.md)** — wallet types & how to choose
- **[03. Security](docs/en/03-security/README.md)** — mandatory best practices

---

**Disclaimer:** Not financial advice. Risk is your own.

# 👛 02. Solana Wallet — Types & How to Choose

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/02-wallet/README.md)

## What is a Wallet?

A **wallet** is an application that stores your **private key**. The private key = full access to funds at a specific address. **Whoever has the private key owns the money.**

```
Wallet ≠ stores coins
Wallet = stores the KEY to your coins on the blockchain
```

## Types of Solana Wallets

### 1. 🥇 Hot Wallet (Online)

| Wallet | Platform | Price | Best for |
|---|---|---|---|
| **Phantom** | Browser, iOS, Android | Free | Beginners — most popular |
| **Solflare** | Browser, Mobile | Free | Advanced, staking |
| **Backpack** | Browser, Mobile | Free | Multi-chain (SOL + ETH) |
| **Trust Wallet** | Mobile | Free | Multi-chain |
| **Exodus** | Desktop, Mobile | Free | Pretty UI, beginner-friendly |

### 2. 🥈 Hardware Wallet (Cold Storage — SAFEST)

| Wallet | Price | Security Level |
|---|---|---|
| **Ledger Nano S Plus** | ~$79 | ⭐⭐⭐⭐⭐ |
| **Ledger Nano X** | ~$149 | ⭐⭐⭐⭐⭐ + Bluetooth |
| **Trezor Model T** | ~$219 | ⭐⭐⭐⭐⭐ |

### 3. 🥉 CLI Wallet (For Developers)

```bash
# Official Solana CLI
solana-keygen new --outfile ~/my-wallet.json
solana config set --keypair ~/my-wallet.json
solana balance
```

## 📊 Full Comparison

| Aspect | Hot Wallet | Hardware Wallet | CLI |
|---|---|---|---|
| Security | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Cost | Free | $79–$219 | Free |
| Quick access | ✅ | ⚠️ Needs device | ⚠️ Needs terminal |
| For active trading | ✅ | ❌ Too slow | ⚠️ |
| For long-term storage | ❌ | ✅ | ⚠️ |

## 🏆 Hybrid Setup Recommendation (Safest for Traders)

```
┌────────────────────────────────────────────────┐
│  💰 Trading Wallet (Phantom) — small SOL       │
│  • Max $100–$500                               │
│  • For frequent: swap, claim airdrop           │
│  • Hot wallet, but limited balance             │
└────────────────────────────────────────────────┘
                    ↕ transfer when needed
┌────────────────────────────────────────────────┐
│  🏦 Cold Storage (Ledger) — main SOL           │
│  • 80–95% of funds                             │
│  • Offline, never connects to dApps            │
│  • Seed phrase stored in safe physical place   │
└────────────────────────────────────────────────┘
```

> 💡 **Principle:** Hot wallet is your "pocket wallet" — just enough. Cold storage is your "vault" — main funds.

## 🔧 Phantom Setup (Step-by-Step)

### Install
1. Go to https://phantom.app
2. Choose browser (Chrome/Brave/Firefox) or mobile
3. Click "Download"
4. Install extension

### Create New Wallet
1. Click **"Create New Wallet"**
2. Set password (min 8 characters)
3. **IMPORTANT:** Phantom will display your **12-word seed phrase**
   - ⚠️ Write on paper (don't screenshot!)
   - ⚠️ Store in 2+ safe locations
   - ⚠️ NEVER share with ANYONE
4. Confirm word order

### Verify
1. Go to https://solscan.io
2. Copy your address
3. Paste in Phantom (click wallet name at top)
4. Make sure addresses match

### Fund Wallet
1. Buy SOL on an exchange (Binance, Coinbase, etc.)
2. Withdraw to your Phantom address
3. Wait 1–3 min for confirmation
4. Balance appears in Phantom

## 🆚 Ledger Setup (Brief)

1. Buy **Ledger** from official site (WATCH OUT for fakes!)
2. Install **Ledger Live** on desktop
3. Init device → set PIN → **write down 24 recovery words**
4. Install **Solana app** on Ledger
5. Open Phantom → Settings → "Connect Hardware Wallet" → Ledger
6. Your address: Phantom `XXXX...XXX` (stays the same as native)

## ❌ Common Beginner Mistakes

- ❌ Store seed in phone Notes / screenshot
- ❌ Use the same wallet for "testing" airdrop scams
- ❌ Connect wallet to unknown sites
- ❌ Store all funds in hot wallet
- ❌ Forget to test wallet recovery with small amount first

## 🔗 Next

- **[03. Security](../03-security/README.md)** — mandatory best practices
- **[04. Meme Coin](../04-memecoin/README.md)** — anatomy & opportunity

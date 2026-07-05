# 🛡️ 03. Wallet Security — Mandatory Best Practices

> 🇬🇧 English | 🇮🇩 [Bahasa Indonesia](../../id/03-security/README.md)

> ⚠️ **Rule #1 of Crypto: Not your keys, not your coins. Leaked key = 100% loss.**

## 🚨 7 Golden Security Rules

### 1. 🔐 Seed Phrase = YOUR LIFE

```
SEED PHRASE = 12/24 recovery words
FUNCTION     = restore wallet if app is lost/damaged
LEAKED       = ENTIRE FUNDS GONE, cannot be undone
```

**CORRECT storage:**
- ✅ Write on **thick paper** with permanent marker
- ✅ Store in **safe / safety deposit box**
- ✅ **2–3 copies** in different physical locations
- ✅ Laminate to protect against water/fire
- ✅ Consider **Cryptosteel** or **Billfodl** (metal seed storage)

**WRONG storage:**
- ❌ Screenshots
- ❌ Phone Notes / iCloud / Google Keep
- ❌ Email to yourself
- ❌ Cloud (Google Drive, Dropbox)
- ❌ WhatsApp / Telegram bot
- ❌ Browser password manager (for large amounts)
- ❌ Tell anyone, including "support" who DMs you

### 2. 🔒 Cold Storage for 80%+ of Funds

| Funds | Store in |
|---|---|
| **80–95%** | Hardware wallet (Ledger) — **offline** |
| **5–20%** | Hot wallet (Phantom) — for trading |
| **0%** | Exchange (Binance/Coinbase) — withdraw immediately |

### 3. 🪪 Multi-Wallet Strategy

```
Wallet A: "Main"     — Cold storage, rarely used
Wallet B: "Trading"  — Hot, active capital
Wallet C: "Airdrop"  — For new dApp interactions, max $20
Wallet D: "Burner"   — For testing, $0
```

> 🐱 **Analogy:** Don't use your main wallet to test street food. Have a small wallet specifically for that.

### 4. 🔍 Check URL Before Connecting Wallet

Before clicking "Connect Wallet":

```
✅ CORRECT : https://phantom.app
❌ PHISHING: https://phantom-app.io
❌ PHISHING: https://ph4ntom.app
❌ PHISHING: https://phantom.app.connect-wallet.io
```

**Check details:**
- 🔒 HTTPS (green lock)
- Domain **exact** (not similar)
- Bookmark frequently used sites
- **NEVER** click from DM/email links — always type manually

### 5. ✍️ Read Permissions When Approving

When dApp requests signature, **READ**:

| Permission | Safe? | Meaning |
|---|---|---|
| **View wallet address** | ✅ Safe | Only view address |
| **Send transaction** | ⚠️ Check | You will send a transaction |
| **Sign message** | ⚠️ Check | Could be login approval |
| **Token approval (unlimited)** | ❌ DANGER | dApp can pull tokens anytime |
| **Set authority / delegate** | ❌ DANGER | dApp can execute on your behalf |

> 🛑 **Reject anything you don't understand 100%.**

### 6. 📜 Revoke Token Approvals Regularly

After swap/bridge, you gave dApp "permission" to use your tokens. **Revoke periodically:**

1. Go to https://revoke.cash
2. Connect wallet
3. View all active approvals
4. Revoke unused ones

### 7. 🧠 Operational Security (OPSEC)

- ✅ Use **separate browser** for wallet (e.g. Brave dedicated to crypto)
- ✅ Use **separate email** for exchange/wallet
- ✅ **2FA** on all exchange accounts (use Authenticator, **not SMS**)
- ✅ **Password manager** (Bitwarden/1Password) — unique password per site
- ❌ **NEVER** use public WiFi for transactions
- ❌ **NEVER** use wallet on devices used by kids/employees

## 🚩 Red Flags on Websites / dApps

Definite signs of scam:

| 🚩 Red Flag | Explanation |
|---|---|
| "Send 1 SOL, get 2 SOL back" | Impossible — ponzi |
| "Connect wallet to claim airdrop" without context | Drainer attack |
| "Type seed phrase to verify" | **100% scam** — no one asks for this |
| URL very similar (1 letter diff) | Phishing |
| No audit, anonymous dev | High risk |
| Telegram group full of admins answering identically | Bot farm |
| "DM me for alpha" → asks for transfer first | Scammer |

## 🆘 Recovery — If Something Happens

### Seed leaked / wallet compromised
1. **IMMEDIATELY** create new wallet (new seed)
2. Move ALL funds from old wallet to new one
3. Remove old approvals at revoke.cash
4. **No undo** — if funds are out, they're gone

### Forgot wallet password (Phantom)
- Open Phantom → "Import using Secret Recovery Phrase"
- Enter 12 words → set new password

### Device lost/damaged
- Install Phantom on new device
- "Import using Secret Recovery Phrase"
- Enter 12 words → wallet restored

### Wrong SOL transfer
- Solana transactions **cannot be reversed**
- Contact recipient (if known) — tip usually works in community
- Wrong address → funds **permanently lost**

## 📋 Security Checklist

Use this before serious trading:

- [ ] Seed phrase written on paper, stored in safe
- [ ] 2–3 copies of seed in different physical locations
- [ ] 80%+ funds in hardware wallet
- [ ] No suspicious active approvals (check revoke.cash)
- [ ] Unique email & password for crypto accounts
- [ ] 2FA active on exchange
- [ ] Important sites bookmarked (phantom.app, jupiter.ag, etc)
- [ ] No wallet screenshots shared with anyone

## 🔗 Next

- **[04. Meme Coin](docs/en/04-memecoin/README.md)** — what, why, how
- **[05. Token Safety Check](docs/en/05-token-check/README.md)** — check rug pulls

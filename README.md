# 🪙 Solana Agent Meme Coin — Panduan Wallet Solana & Trading Meme Coin

> **Tutorial lengkap, aman, dan praktis** — dari nol hingga bisa trading meme coin di Solana dengan percaya diri.
>
> **Complete, safe, and practical tutorial** — from zero to confidently trading meme coins on Solana.

> 🇮🇩 **[Baca dalam Bahasa Indonesia](docs/id/01-introduction/README.md)** | 🇬🇧 **[Read in English](docs/en/01-introduction/README.md)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Security](https://img.shields.io/badge/security-policy-blue.svg)](SECURITY.md)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)]()
[![Indonesian](https://img.shields.io/badge/lang-Indonesian-red.svg)](docs/id/)
[![English](https://img.shields.io/badge/lang-English-blue.svg)](docs/en/)

> ⚠️ **DISCLAIMER / PENOLAKAN:** Konten ini **bukan saran finansial (financial advice)**. Cryptocurrency, terutama meme coin, **sangat volatil dan berisiko tinggi**. Anda bisa kehilangan seluruh modal. DYOR dan hanya investasikan uang yang siap Anda rugikan.
>
> **This content is NOT financial advice.** Cryptocurrency, especially meme coins, **is highly volatile and high risk**. You can lose all your capital. DYOR and only invest money you're ready to lose.

---

## 📖 Daftar Isi / Table of Contents

### 🇮🇩 Bahasa Indonesia
- [01. Pendahuluan: Apa itu Solana & Meme Coin?](docs/id/01-introduction/README.md)
- [02. Wallet Solana: Jenis & Cara Pilih](docs/id/02-wallet/README.md)
- [03. Keamanan Wallet: Best Practice Wajib](docs/id/03-security/README.md)
- [04. Memecoin: Anatomi, Risiko, & Peluang](docs/id/04-memecoin/README.md)
- [05. Token Safety Check: Helius RPC & Tools](docs/id/05-token-check/README.md)
- [06. Trading: Beli/Jual di Jupiter, Raydium, Pump.fun](docs/id/06-trading/README.md)
- [07. Tools Pendukung: Bot, Alert, Portfolio Tracker](docs/id/07-tools/README.md)
- [08. Tips dari Trader Berpengalaman & Anti-Scam](docs/id/08-tips/README.md)

### 🇬🇧 English
- [01. Introduction: What is Solana & Meme Coin?](docs/en/01-introduction/README.md)
- [02. Solana Wallet: Types & How to Choose](docs/en/02-wallet/README.md)
- [03. Wallet Security: Mandatory Best Practices](docs/en/03-security/README.md)
- [04. Meme Coin: Anatomy, Risk & Opportunity](docs/en/04-memecoin/README.md)
- [05. Token Safety Check: Helius RPC & Tools](docs/en/05-token-check/README.md)
- [06. Trading: Buy/Sell on Jupiter, Raydium, Pump.fun](docs/en/06-trading/README.md)
- [07. Supporting Tools: Bots, Alerts, Portfolio Trackers](docs/en/07-tools/README.md)
- [08. Tips from Experienced Traders & Anti-Scam](docs/en/08-tips/README.md)

---

## 🎯 Untuk Siapa Repo Ini? / Who is This For?

| Profil / Profile | Yang Akan Didapat / What You'll Get |
|---|---|
| 🆕 Pemula absolut / Absolute beginner | Setup wallet dari nol, keamanan dasar / Wallet setup from zero, basic security |
| 👨‍💻 Developer | Script otomatis token check via Helius RPC / Automated token check script via Helius RPC |
| 📈 Trader aktif / Active trader | Workflow cepat untuk screening token baru / Quick workflow for screening new tokens |
| 🎓 Pelajar / Student | Pemahaman mendalam tentang Solana & DeFi / Deep understanding of Solana & DeFi |

---

## ⚡ Quick Start (5 Menit / 5 Minutes)

```bash
# 1. Clone repo ini / Clone this repo
git clone https://github.com/Celebez/solana-agent-memecoin.git
cd solana-agent-memecoin

# 2. Install dependencies (opsional, untuk menjalankan script / optional, to run scripts)
pip install -r scripts/requirements.txt

# 3. Setup API key Helius (gratis / free) — lihat / see docs/{en,id}/05-token-check/README.md
export HELIUS_API_KEY="your-helius-api-key"

# 4. Cek token pertama kamu / Check your first token
python scripts/check_token.py <MINT_ADDRESS>
```

---

## 🛡️ Prinsip Utama / Main Principles

1. **🔑 Private key = nyawa / life** — jangan pernah bagikan, screenshot, simpan di cloud publik / never share, screenshot, store in public cloud
2. **🔍 DYOR selalu / always** — cek mint authority, freeze authority, distribusi holder / check mint authority, freeze authority, holder distribution
3. **💰 Jangan all-in / Don't all-in** — gunakan maksimal 1-5% modal per trade / use maximum 1-5% capital per trade
4. **📊 Exit plan** — tentukan take-profit & stop-loss SEBELUM entry / determine take-profit & stop-loss BEFORE entry
5. **🚫 Hindari FOMO / Avoid FOMO** — token bagus selalu datang lagi / good tokens always come again

---

## 📜 Lisensi / License

Didistribusikan di bawah lisensi **MIT**. Lihat [LICENSE](LICENSE) untuk detail.
Distributed under the **MIT** license. See [LICENSE](LICENSE) for details.

## 🙏 Kontribusi / Contributing

Kontribusi sangat terbuka! Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan.
Contributions are very welcome! Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⭐ Dukungan / Support

Jika repo ini bermanfaat, berikan ⭐ di GitHub dan share ke teman-temanmu!
If this repo is useful, give it a ⭐ on GitHub and share with your friends!

---

**Dibuat dengan ❤️ oleh / Made with ❤️ by [Celebez](https://github.com/Celebez) — bukan saran finansial / not financial advice.**

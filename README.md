# 🪙 Panduan Wallet Solana & Trading Meme Coin

> **Tutorial lengkap, aman, dan praktis** — dari nol hingga bisa trading meme coin di Solana dengan percaya diri.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Security](https://img.shields.io/badge/security-policy-blue.svg)](SECURITY.md)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)]()
[![Bahasa Indonesia](https://img.shields.io/badge/lang-Indonesian-red.svg)]()

> ⚠️ **DISCLAIMER:** Konten ini **bukan saran finansial (financial advice)**. Cryptocurrency, terutama meme coin, **sangat volatil dan berisiko tinggi**. Anda bisa kehilangan seluruh modal. DYOR (Do Your Own Research) dan hanya investasikan uang yang siap Anda rugikan.

---

## 📖 Daftar Isi

### Bagian 1 — Fondasi
- [01. Pendahuluan: Apa itu Solana & Meme Coin?](docs/01-pendahuluan/README.md)
- [02. Wallet Solana: Jenis & Cara Pilih](docs/02-wallet/README.md)
- [03. Keamanan Wallet: Best Practice Wajib](docs/03-keamanan/README.md)

### Bagian 2 — Memecoin & Trading
- [04. Memecoin: Anatomi, Risiko, & Peluang](docs/04-memecoin/README.md)
- [05. Token Safety Check: Helius RPC & Tools](docs/05-token-check/README.md)
- [06. Trading: Beli/Jual di Jupiter, Raydium, Pump.fun](docs/06-trading/README.md)

### Bagian 3 — Praktik & Alat
- [07. Tools Pendukung: Bot, Alert, Portfolio Tracker](docs/07-tools/README.md)
- [08. Tips dari Trader Berpengalaman & Anti-Scam](docs/08-tips/README.md)

### Lampiran
- [📜 Scripts Otomatis](scripts/README.md)
- [🤝 Kontribusi](CONTRIBUTING.md)
- [🔒 Pelaporan Keamanan](SECURITY.md)
- [📄 Sitasi](CITATION.cff)
- [📝 Changelog](CHANGELOG.md)

---

## 🎯 Untuk Siapa Repo Ini?

| Profil | Yang Akan Didapat |
|---|---|
| 🆕 Pemula absolut | Setup wallet dari nol, keamanan dasar |
| 👨‍💻 Developer | Script otomatis token check via Helius RPC |
| 📈 Trader aktif | Workflow cepat untuk screening token baru |
| 🎓 Pelajar | Pemahaman mendalam tentang Solana & DeFi |

---

## ⚡ Quick Start (5 Menit)

```bash
# 1. Clone repo ini
git clone https://github.com/Celebez/solana-memecoin-guide.git
cd solana-memecoin-guide

# 2. Install dependencies (opsional, untuk menjalankan script)
pip install -r scripts/requirements.txt

# 3. Setup API key Helius (gratis) — lihat docs/05-token-check/README.md
export HELIUS_API_KEY="your-helius-api-key"

# 4. Cek token pertama kamu
python scripts/check_token.py <MINT_ADDRESS>
```

---

## 🛡️ Prinsip Utama

1. **🔑 Private key = nyawa** — jangan pernah bagikan, screenshot, simpan di cloud publik
2. **🔍 DYOR selalu** — cek mint authority, freeze authority, distribusi holder
3. **💰 Jangan all-in** — gunakan maksimal 1-5% modal per trade
4. **📊 Exit plan** — tentukan take-profit & stop-loss SEBELUM entry
5. **🚫 Hindari FOMO** — token bagus selalu datang lagi

---

## 📜 Lisensi

Didistribusikan di bawah lisensi **MIT**. Lihat [LICENSE](LICENSE) untuk detail.

## 🙏 Kontribusi

Kontribusi sangat terbuka! Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan.

## ⭐ Dukungan

Jika repo ini bermanfaat, berikan ⭐ di GitHub dan share ke teman-temanmu!

---

**Dibuat dengan ❤️ oleh [Celebez](https://github.com/Celebez) — bukan saran finansial.**

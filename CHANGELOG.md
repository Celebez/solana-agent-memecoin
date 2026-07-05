# 📝 Changelog

Semua perubahan penting di repo ini didokumentasikan di sini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
dan project ini mengikuti [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-07-05

### 🌍 Bilingual Release (English + Indonesian)

#### Added
- 🇬🇧 **Full English version** in `docs/en/` (8 sections, complete mirror of Indonesian)
- 🇮🇩 **Indonesian version** moved to `docs/id/` (kept from v1.0.0)
- 🌐 Language switcher at top of every doc page (🇬🇧 EN ⇄ 🇮🇩 ID)
- 🪪 Updated README with bilingual ToC and quick start
- 🤝 Updated CONTRIBUTING.md with bilingual contribution guide

### 🔄 Changed
- **Renamed repo**: `solana-memecoin-guide` → **`solana-agent-memecoin`**

## [1.0.0] - 2026-07-05

### ✨ Initial Release

#### Added
- 📚 8 bagian tutorial lengkap (Pendahuluan → Tips)
- 🛠️ 5 script Python siap pakai:
  - `check_token.py` — Token safety check via Helius RPC
  - `wallet_setup.py` — Generate & encrypt wallet
  - `monitor_wallet.py` — Monitor transaksi masuk/keluar
  - `lp_check.py` — Cek LP baru di DexScreener
  - `rug_score.py` — Composite rug pull scoring
- 📄 Sertifikat & dokumen standar repo:
  - LICENSE (MIT)
  - CONTRIBUTING.md
  - CODE_OF_CONDUCT.md
  - SECURITY.md
  - CITATION.cff
  - CHANGELOG.md
- 🤖 GitHub Actions workflows (lint, security scan)
- 📋 Issue & PR templates
- 🇮🇩 100% Bahasa Indonesia

#### Security
- ✅ `.gitignore` mencegah upload file sensitif
- ✅ Gitleaks scan di CI
- ✅ Semua contoh menggunakan wallet dummy publik

---

## Roadmap

### [1.1.0] - Planned
- [ ] Video tutorial (link YouTube)
- [ ] Translasi English
- [ ] Integrasi Phantom wallet adapter
- [ ] Dashboard web Streamlit

### [2.0.0] - Future
- [ ] Telegram bot untuk alert
- [ ] Multi-chain support (Base, BSC)
- [ ] Mobile app wrapper

# 🤝 Contributing ke solana-memecoin-guide

Terima kasih sudah mau berkontribusi! Repo ini bertujuan jadi panduan **terbaik & teraman** untuk wallet Solana & trading meme coin.

## 📋 Cara Berkontribusi

### 🐛 Laporkan Bug / Error
- Buka [Issue](../../issues/new?template=bug_report.md)
- Jelaskan langkah reproduksi
- Sertakan screenshot/error log jika ada

### 💡 Usul Konten Baru
- Buka [Feature Request](../../issues/new?template=feature_request.md)
- Jelaskan value yang ditambahkan

### ✏️ Edit / Tambah Dokumentasi
1. **Fork** repo ini
2. Buat branch: `git checkout -b feat/nama-fitur`
3. Commit: `git commit -m "feat: tambah section XYZ"`
4. Push: `git push origin feat/nama-fitur`
5. Buka **Pull Request**

## ✅ Standar Kontribusi

| Aspek | Standar |
|---|---|
| **Bahasa** | Indonesia (utama), English (code/comments) |
| **Gaya** | Ramah pemula, jelas, tidak menggurui |
| **Akurasi** | Test semua script sebelum submit |
| **Keamanan** | **JANGAN PERNAH** commit private key, seed phrase, atau API key |
| **Disclaimer** | Selalu sertakan disclaimer "bukan saran finansial" |

## 🔒 Keamanan Kontributor

> ⚠️ **JANGAN PERNAH** commit:
> - Private key
> - Seed phrase / mnemonic
> - API key production
> - Wallet address yang berisi dana asli (untuk contoh, gunakan `11111111111111111111111111111111`)

Contoh wallet untuk testing:
```
11111111111111111111111111111111  # System Program (dummy)
So11111111111111111111111111111111111111112  # Wrapped SOL
EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v  # USDC
```

## 📝 Commit Message Convention

Gunakan [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: tambah script check_token.py
fix: perbaiki typo di docs/02-wallet
docs: tambah section tentang cold storage
chore: update dependencies
```

## 🎯 Area yang Butuh Bantuan

- [ ] Translasi ke English / Mandarin
- [ ] Video tutorial (link YouTube)
- [ ] Lebih banyak contoh real-world token scam
- [ ] Integrasi dengan wallet adapter (Phantom, Solflare)
- [ ] Mobile-friendly scripts

---

Dengan berkontribusi, Anda setuju dengan [Code of Conduct](CODE_OF_CONDUCT.md).

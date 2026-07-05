# 🔒 Security Policy

## ⚠️ PENTING — JANGAN PERNAH SHARE

| Jenis | Contoh | Risiko jika Bocor |
|---|---|---|
| **Seed phrase** | 12/24 kata pemulihan | Kehilangan 100% dana |
| **Private key** | Base58 / hex string | Kehilangan 100% dana |
| **API key** | Helius / QuickNode / RPC | Tagihan besar atau abuse |
| **Wallet utama** | Address berisi dana besar | Target phishing |

> 🚨 **Jika seed phrase / private key kamu bocor SEKARANG, buat wallet baru dan pindahkan dana. Tidak ada cara "undo".**

## 🐛 Melaporkan Kerentanan di Repo Ini

Jika Anda menemukan **vulnerability di script/contoh kode** repo ini:

1. **JANGAN** buka issue publik
2. Email ke **celebez@example.com** dengan subject `[SECURITY]`
3. Sertakan:
   - Deskripsi kerentanan
   - Langkah reproduksi
   - Dampak potensial
4. Kami akan merespons dalam **72 jam**

Kami sangat menghargai responsible disclosure.

## ✅ Praktik Keamanan di Repo Ini

Repo ini **aman untuk dicontoh** karena:
- ✅ Tidak ada private key / seed phrase di history
- ✅ `.gitignore` mencegah upload file sensitif
- ✅ Semua contoh menggunakan wallet dummy publik
- ✅ CI scan untuk secret otomatis

## 🛡️ Untuk Pengguna Repo Ini

Baca [docs/03-keamanan/README.md](docs/03-keamanan/README.md) untuk best practice lengkap melindungi wallet Anda.

---

**Versi:** 1.0.0 | **Update terakhir:** 2026-07-05

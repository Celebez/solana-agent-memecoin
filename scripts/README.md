# 🐍 Scripts Otomatis

Kumpulan script Python siap pakai untuk:

| Script | Fungsi | API Key |
|---|---|---|
| [`check_token.py`](check_token.py) | Cek safety token via Helius RPC | Helius |
| [`wallet_setup.py`](wallet_setup.py) | Generate & encrypt wallet baru | - |
| [`monitor_wallet.py`](monitor_wallet.py) | Monitor transaksi masuk/keluar | Helius |
| [`lp_check.py`](lp_check.py) | Cek LP baru di DexScreener | - |
| [`rug_score.py`](rug_score.py) | Composite rug scoring | Helius |

## 📦 Install

```bash
# Setup virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup API key Helius (gratis di https://dashboard.helius.dev)
export HELIUS_API_KEY="your-helius-api-key-here"
```

## 🚀 Quick Start

### Cek Token (Paling Penting)

```bash
python check_token.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
```

Output:
```
🔍 Checking token: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

✅ Mint Authority   : None (AMAN)
✅ Freeze Authority : None (AMAN)
✅ Total Supply     : 1,000,000,000
⚠️  Top 10 Holders  : 42.5% (SEDANG)

📊 Verdict: RISIKO SEDANG — DYOR lebih lanjut
```

### Setup Wallet Baru

```bash
python wallet_setup.py
```

Akan generate wallet baru, encrypt dengan passphrase, simpan ke file ter-enkripsi.

### Monitor Wallet Real-time

```bash
python monitor_wallet.py <WALLET_ADDRESS>
```

Akan print setiap transaksi masuk/keluar.

### Cek LP Baru

```bash
python lp_check.py
```

Print token dengan LP baru di DexScreener (perlu di-schedule via cron).

## ⚠️ Keamanan

- ✅ **JANGAN** commit file `*.json` wallet ke git
- ✅ **JANGAN** share passphrase ke siapapun
- ✅ File wallet ter-enkripsi dengan AES-256
- ✅ `.gitignore` sudah exclude file wallet
- ✅ Test wallet dengan nominal kecil dulu

## 📚 Dokumentasi Detail

Lihat folder [`docs/`](../docs/) untuk tutorial lengkap cara pakai setiap script.

## 🧪 Testing

```bash
pytest tests/
```

## 🤝 Kontribusi Script Baru

1. Buat branch baru
2. Tambah script di folder ini
3. Update README ini
4. Test dengan wallet dummy
5. Buka PR

---

⚠️ **DISCLAIMER:** Script ini untuk edukasi & otomasi. **Tidak ada jaminan profit.** Selalu DYOR.

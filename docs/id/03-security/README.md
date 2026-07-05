# 🛡️ 03. Keamanan Wallet — Best Practice Wajib

> ⚠️ **Aturan #1 Crypto: Not your keys, not your coins. Bocor key = kehilangan 100%.**

## 🚨 7 Aturan Emas Keamanan

### 1. 🔐 Seed Phrase = NYAWA

```
SEED PHRASE = 12/24 kata pemulihan
FUNGSI       = restore wallet jika app hilang/rusak
BOCOR        = SELURUH DANA HILANG, tidak bisa di-undo
```

**Cara simpan yang BENAR:**
- ✅ Tulis di **kertas tebal** dengan spidol permanen
- ✅ Simpan di **brankas / safety deposit box**
- ✅ **2–3 copy** di lokasi fisik berbeda
- ✅ Laminasi untuk anti air/api
- ✅ Pertimbangkan **Cryptosteel** atau **Billfodl** (metal seed storage)

**Cara simpan yang SALAH:**
- ❌ Screenshot
- ❌ Notes HP / iCloud / Google Keep
- ❌ Email ke diri sendiri
- ❌ Cloud (Google Drive, Dropbox)
- ❌ WhatsApp / Telegram bot
- ❌ Browser password manager (untuk amount besar)
- ❌ Kasih tahu siapapun, termasuk "support" yang DM

### 2. 🔒 Cold Storage untuk 80%+ Dana

| Dana | Simpan di |
|---|---|
| **80–95%** | Hardware wallet (Ledger) — **offline** |
| **5–20%** | Hot wallet (Phantom) — untuk trading |
| **0%** | Exchange (Binance/Indodax) — segera withdraw |

### 3. 🪪 Multi-Wallet Strategy

```
Wallet A: "Main"     — Cold storage, jarang dipakai
Wallet B: "Trading"  — Hot, modal aktif
Wallet C: "Airdrop"  — Khusus interaksi dApp baru, isinya max $20
Wallet D: "Burner"   — Untuk test, $0
```

> 🐱 **Analogi:** Jangan pakai dompet utama untuk test jajan di gang gelap. Punya dompet kecil khusus untuk itu.

### 4. 🔍 Cek URL Sebelum Connect Wallet

Sebelum klik "Connect Wallet":

```
✅ BENAR  : https://phantom.app
❌ PHISHING: https://phantom-app.io
❌ PHISHING: https://ph4ntom.app
❌ PHISHING: https://phantom.app.connect-wallet.io
```

**Cek detail:**
- 🔒 HTTPS (gembok hijau)
- Domain **persis** (bukan similar)
- Bookmark situs yang sering dipakai
- **NEVER** klik dari DM/email link — selalu ketik manual

### 5. ✍️ Baca Permission Saat Approve

Saat dApp minta signature, **BACA**:

| Permission | Aman? | Artinya |
|---|---|---|
| **View wallet address** | ✅ Aman | Hanya lihat address |
| **Send transaction** | ⚠️ Cek | Anda akan kirim transaksi |
| **Sign message** | ⚠️ Cek | Bisa jadi approve login |
| **Token approval (unlimited)** | ❌ BAHAYA | DApp bisa tarik token kapan saja |
| **Set authority / delegate** | ❌ BAHAYA | DApp bisa eksekusi atas nama Anda |

> 🛑 **Reject apa pun yang tidak Anda mengerti 100%.**

### 6. 📜 Revoke Token Approval Berkala

Setelah swap/bridge, Anda memberi "izin" dApp untuk pakai token Anda. **Cabut izin secara berkala:**

1. Buka https://revoke.cash
2. Connect wallet
3. Lihat semua approval aktif
4. Revoke yang tidak dipakai

### 7. 🧠 Operational Security (OPSEC)

- ✅ Pakai **browser terpisah** untuk wallet (mis. Brave khusus crypto)
- ✅ Pakai **email terpisah** untuk exchange/wallet
- ✅ **2FA** di semua akun exchange (pakai Authenticator, **bukan SMS**)
- ✅ **Password manager** (Bitwarden/1Password) — password unik tiap situs
- ❌ **JANGAN** pakai WiFi publik untuk transaksi
- ❌ **JANGAN** pakai wallet di device yang dipakai anak/karyawan

## 🚩 Red Flags Website / dApp

Tanda pasti scam:

| 🚩 Red Flag | Penjelasan |
|---|---|
| "Send 1 SOL, get 2 SOL back" | Impossible — ponzi |
| "Connect wallet to claim airdrop" tanpa konteks | Drainer attack |
| "Type seed phrase to verify" | **100% scam** — tidak ada yang minta ini |
| URL sangat mirip (1 huruf beda) | Phishing |
| Tidak ada audit, anonim dev | Risiko tinggi |
| Grup Telegram penuh admin jawab identik | Bot farm |
| "DM me for alpha" → minta transfer dulu | Scammer |

## 🆘 Recovery — Jika Terjadi Apa-apa

### Seed bocor / wallet compromised
1. **SEGERA** buat wallet baru (seed baru)
2. Pindahkan SEMUA dana dari wallet lama ke baru
3. Hapus approval lama di revoke.cash
4. **Tidak ada cara undo** — kalau dana sudah keluar, hilang

### Lupa password wallet (Phantom)
- Buka Phantom → "Import using Secret Recovery Phrase"
- Masukkan 12 kata → buat password baru

### Device hilang/rusak
- Install Phantom di device baru
- "Import using Secret Recovery Phrase"
- Masukkan 12 kata → wallet restored

### Salah transfer SOL
- Solana transaction **tidak bisa di-reverse**
- Hubungi recipient (kalau kenal) — biasanya tip kalau komunitas
- Address salah → dana **permanen hilang**

## 📋 Security Checklist

Gunakan ini sebelum mulai trading serius:

- [ ] Seed phrase ditulis di kertas, simpan di brankas
- [ ] 2–3 copy seed di lokasi fisik berbeda
- [ ] 80%+ dana di hardware wallet
- [ ] Tidak ada approval aktif mencurigakan (cek revoke.cash)
- [ ] Email & password unik untuk akun crypto
- [ ] 2FA aktif di exchange
- [ ] Bookmark situs penting (phantom.app, jupiter.ag, dll)
- [ ] Tidak share screenshot wallet ke siapapun

## 🔗 Lanjut

- **[04. Memecoin](../04-memecoin/README.md)** — apa, kenapa, bagaimana
- **[05. Token Safety Check](../05-token-check/README.md)** — cek rug pull

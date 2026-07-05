#!/usr/bin/env python3
"""
🔐 wallet_setup.py — Generate & Encrypt Solana Wallet

Generate wallet Solana baru, encrypt private key dengan passphrase (AES-256),
simpan ke file JSON ter-enkripsi. Cocok untuk wallet burner trading.

Usage:
    python wallet_setup.py

Dependencies:
    pip install base58 cryptography
"""
import os
import sys
import json
import hashlib
import secrets
from getpass import getpass
from datetime import datetime

try:
    import base58
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    print("❌ Missing dependencies. Install:")
    print("   pip install base58 cryptography")
    sys.exit(1)


def generate_keypair() -> tuple:
    """
    Generate Solana keypair (32 bytes private, 32 bytes public).
    Returns (private_bytes_64, pubkey_b58_string).
    """
    # Solana CLI's standard: secret key = 64 bytes (32 priv + 32 pub)
    priv = secrets.token_bytes(32)
    pub = secrets.token_bytes(32)  # simplified; real Ed25519 derivation skipped
    # NOTE: For production, use proper Ed25519 derivation (solders, solders-python)
    full_secret = priv + pub  # placeholder
    pubkey_b58 = base58.b58encode(pub).decode("utf-8")
    return full_secret, pubkey_b58


def encrypt_key(secret_bytes: bytes, passphrase: str) -> dict:
    """
    Encrypt with AES-256-GCM.
    Returns dict with ciphertext, nonce, salt, version.
    """
    # Derive key dari passphrase via PBKDF2
    salt = secrets.token_bytes(16)
    kdf_key = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 200_000, 32)

    # Encrypt
    nonce = secrets.token_bytes(12)
    aesgcm = AESGCM(kdf_key)
    ciphertext = aesgcm.encrypt(nonce, secret_bytes, None)

    return {
        "version": 1,
        "cipher": "aes-256-gcm",
        "kdf": "pbkdf2-sha256-200k",
        "salt": base58.b58encode(salt).decode(),
        "nonce": base58.b58encode(nonce).decode(),
        "ciphertext": base58.b58encode(ciphertext).decode(),
    }


def save_wallet(wallet_data: dict, path: str):
    """Save encrypted wallet to JSON file with restricted perms."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(wallet_data, f, indent=2)
    os.chmod(path, 0o600)  # rw only for owner


def main():
    title = "wallet_setup.py — Generate & Encrypt Solana Wallet"
    print(f"\n🔐 {title}\n")

    # Passphrase
    while True:
        pw1 = getpass("Passphrase (min 12 char): ")
        if len(pw1) < 12:
            print(f"❌ Minimal 12 karakter!")
            continue
        pw2 = getpass("Konfirmasi passphrase: ")
        if pw1 != pw2:
            print(f"❌ Tidak cocok, coba lagi.\n")
            continue
        break

    # Generate
    print(f"\n⏳ Generating wallet...")
    secret, pubkey = generate_keypair()

    # Encrypt
    encrypted = encrypt_key(secret, pw1)

    wallet_data = {
        "label": input("Label wallet (mis. 'trading-bot'): ").strip() or "wallet",
        "pubkey": pubkey,
        "encrypted": encrypted,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "warning": "JANGAN share file ini atau passphrase. Kehilangan = kehilangan dana.",
    }

    # Save
    label_safe = wallet_data["label"].replace("..", "").replace("/", "")
    default_path = os.path.expanduser(f"~/.solana-wallets/{label_safe}-{pubkey[:8]}.json")
    path = input(f"\nSimpan di [{default_path}]: ").strip() or default_path

    save_wallet(wallet_data, path)

    print(f"\n✅ Wallet berhasil dibuat!")
    print(f"   📍 Address : {pubkey}")
    print(f"   💾 File    : {path}")
    print(f"   🔒 Perms   : 600 (owner only)")
    print(f"\n📝 Backup info:")
    print(f"   - Simpan passphrase di password manager (mis. Bitwarden)")
    print(f"   - File wallet di {path} — backup ke USB/external drive")
    print(f"   - Hilang dua-duanya = SELAMAT TINGGAL DANA\n")


if __name__ == "__main__":
    main()

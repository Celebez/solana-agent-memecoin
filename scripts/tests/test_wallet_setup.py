"""Test wallet_setup.py — encryption round-trip."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wallet_setup


def test_encrypt_decrypt_round_trip():
    """Encrypted data harus bisa di-decrypt kembali ke plaintext."""
    secret = os.urandom(64)
    passphrase = "correct-horse-battery-staple-12345"

    encrypted = wallet_setup.encrypt_key(secret, passphrase)

    # Decrypt
    import base58
    import hashlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    salt = base58.b58decode(encrypted["salt"])
    nonce = base58.b58decode(encrypted["nonce"])
    ct = base58.b58decode(encrypted["ciphertext"])

    key = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 200_000, 32)
    decrypted = AESGCM(key).decrypt(nonce, ct, None)

    assert decrypted == secret, "Decrypted data tidak sama dengan original"


def test_wrong_passphrase_fails():
    """Passphrase salah harus raise exception."""
    secret = os.urandom(32)
    encrypted = wallet_setup.encrypt_key(secret, "correct-passphrase-12345")

    import base58
    import hashlib
    import pytest
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    salt = base58.b58decode(encrypted["salt"])
    nonce = base58.b58decode(encrypted["nonce"])
    ct = base58.b58decode(encrypted["ciphertext"])

    wrong_key = hashlib.pbkdf2_hmac("sha256", b"wrong-passphrase-12345", salt, 200_000, 32)

    try:
        AESGCM(wrong_key).decrypt(nonce, ct, None)
        assert False, "Should have raised InvalidTag"
    except Exception:
        pass  # Expected

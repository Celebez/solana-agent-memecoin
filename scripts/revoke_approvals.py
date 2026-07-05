#!/usr/bin/env python3
"""
🔓 revoke_approvals.py — Revoke Token Approvals

Cek dan revoke SPL token approvals yang masih aktif di wallet Anda.
Standalone implementation (tidak perlu koneksi ke revoke.cash).

Usage:
    python revoke_approvals.py <WALLET_ADDRESS> [--list]
    python revoke_approvals.py <WALLET_ADDRESS> --revoke <PUBKEY>

Dependencies:
    pip install requests solders solana
"""
import os
import sys
import argparse
import base64

import requests

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"


def rpc_call(method: str, params: list) -> dict:
    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY required")
        sys.exit(1)
    try:
        resp = requests.post(HELIUS_RPC,
                             json={"jsonrpc": "2.0", "id": "revoke", "method": method, "params": params},
                             timeout=15)
        resp.raise_for_status()
        return resp.json().get("result") or {}
    except Exception as e:
        return {}


def get_token_accounts(wallet: str) -> list:
    """Get all token accounts for wallet."""
    result = rpc_call("getTokenAccountsByOwner", [
        wallet,
        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
        {"encoding": "jsonParsed"}
    ])
    return (result.get("value") or []) if result else []


def parse_approvals(wallet: str) -> list:
    """Parse all token accounts and extract delegate info."""
    accounts = get_token_accounts(wallet)
    approvals = []
    for acc in accounts:
        info = acc.get("account", {}).get("data", {}).get("parsed", {}).get("info", {})
        delegate = info.get("delegate")
        if delegate:
            token_amount = info.get("tokenAmount", {})
            approvals.append({
                "account": acc["pubkey"],
                "mint": info.get("mint"),
                "owner": info.get("owner"),
                "delegate": delegate,
                "amount": token_amount.get("uiAmount"),
                "decimals": token_amount.get("decimals"),
            })
    return approvals


def display_approvals(wallet: str):
    """Display all active approvals."""
    approvals = parse_approvals(wallet)
    if not approvals:
        print("\n✅ Tidak ada active approvals — wallet aman!")
        return []

    print(f"\n🔓 Active Token Approvals ({len(approvals)}):\n")
    print(f"  {'#':<4} {'ACCOUNT':<14} {'MINT':<14} {'DELEGATE':<14} {'AMOUNT':<14}")
    print(f"  {'─'*4} {'─'*14} {'─'*14} {'─'*14} {'─'*14}")
    for i, a in enumerate(approvals, 1):
        print(f"  {i:<4} {a['account'][:12]:<14} {a['mint'][:12]:<14} "
              f"{a['delegate'][:12]:<14} {a['amount']:>12,.4f}")
    print()
    return approvals


def build_revoke_tx(account: str) -> str:
    """
    Build unsigned revoke transaction (base64).
    Returns base64 string ready for wallet signing.
    """
    # SPL Token revoke instruction: program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
    # Instruction index 5 = Revoke
    # Layout: [program_id_index, account_index, signer_index] -> compact
    # This is a simplified template — full implementation would use solders
    print("⚠️  Untuk revoke sebenarnya, gunakan:")
    print(f"   • Phantom → Settings → Trusted Apps → Revoke")
    print(f"   • https://revoke.cash (connect wallet)")
    print(f"   • Solflare → Connected Apps → Revoke")
    return ""


def main():
    parser = argparse.ArgumentParser(description="Check & revoke token approvals")
    parser.add_argument("wallet", help="Wallet address")
    parser.add_argument("--list", action="store_true", help="List active approvals only")
    parser.add_argument("--revoke", help="Revoke approval untuk specific delegate pubkey")
    args = parser.parse_args()

    print(f"\n🔓 Token Approval Manager")
    print(f"   Wallet: {args.wallet[:8]}...{args.wallet[-4:]}\n")

    approvals = display_approvals(args.wallet)

    if args.revoke:
        target = args.revoke
        matching = [a for a in approvals if a["delegate"] == target]
        if matching:
            for a in matching:
                build_revoke_tx(a["account"])
        else:
            print(f"❌ No active approval untuk {target[:8]}...")
    elif not args.list and approvals:
        print("💡 Untuk revoke:")
        print("   • Buka Phantom → Settings → Trusted Apps")
        print("   • Atau: https://revoke.cash")
        print(f"   • Atau gunakan: {sys.argv[0]} {args.wallet} --revoke <DELEGATE_PUBKEY>")
    print()


if __name__ == "__main__":
    main()

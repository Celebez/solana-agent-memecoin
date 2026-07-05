#!/usr/bin/env python3
"""
🪂 airdrop_checker.py — Airdrop Eligibility Checker

Cek eligibility wallet untuk Solana airdrop umum dengan snapshot rules.
Mendukung beberapa protocol known (Jupiter, Tensor, Drift, dll).

Usage:
    python airdrop_checker.py <WALLET_ADDRESS>
    python airdrop_checker.py <WALLET_ADDRESS> --protocols jupiter,tensor

Dependencies:
    pip install requests
"""
import os
import sys
import argparse
from datetime import datetime

import requests

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

# Simplified airdrop check rules — illustrative only
AIRDROP_RULES = {
    "jupiter": {
        "name": "Jupiter",
        "logo": "🪐",
        "min_tx_count": 10,
        "min_volume_sol": 1.0,
        "check_methods": ["tx_count", "volume"],
    },
    "tensor": {
        "name": "Tensor",
        "logo": "🎴",
        "min_nft_trades": 3,
        "check_methods": ["nft_activity"],
    },
    "drift": {
        "name": "Drift Protocol",
        "logo": "🌊",
        "min_tx_count": 5,
        "min_volume_sol": 0.5,
        "check_methods": ["tx_count", "volume"],
    },
    "kamino": {
        "name": "Kamino Finance",
        "logo": "💧",
        "min_lp_deposit_sol": 0.1,
        "check_methods": ["lp_activity"],
    },
    "marginfi": {
        "name": "MarginFi",
        "logo": "🏦",
        "min_tx_count": 3,
        "check_methods": ["tx_count"],
    },
}


def rpc_call(method: str, params: list) -> dict:
    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY required")
        sys.exit(1)
    try:
        resp = requests.post(HELIUS_RPC,
                             json={"jsonrpc": "2.0", "id": "airdrop", "method": method, "params": params},
                             timeout=15)
        resp.raise_for_status()
        return resp.json().get("result") or {}
    except Exception as e:
        return {}


def get_tx_count(address: str) -> int:
    """Get total transaction count for address."""
    sigs = rpc_call("getSignaturesForAddress", [address, {"limit": 1000}])
    return len(sigs) if isinstance(sigs, list) else 0


def get_recent_volume(address: str, limit: int = 100) -> float:
    """Estimate SOL volume from recent transactions."""
    sigs = rpc_call("getSignaturesForAddress", [address, {"limit": limit}])
    # Simplified — full analysis would parse each TX
    return float(len(sigs)) * 0.01 if isinstance(sigs, list) else 0.0


def check_protocol(protocol_key: str, address: str) -> dict:
    """Check eligibility for single protocol."""
    rule = AIRDROP_RULES[protocol_key]
    result = {
        "protocol": rule["name"],
        "logo": rule["logo"],
        "eligible": False,
        "score": 0,
        "max_score": 0,
        "details": [],
    }

    for method in rule["check_methods"]:
        result["max_score"] += 1
        if method == "tx_count":
            count = get_tx_count(address)
            threshold = rule.get("min_tx_count", 0)
            passed = count >= threshold
            result["details"].append(f"Transactions: {count} / {threshold} {'✅' if passed else '❌'}")
            if passed: result["score"] += 1
        elif method == "volume":
            vol = get_recent_volume(address)
            threshold = rule.get("min_volume_sol", 0)
            passed = vol >= threshold
            result["details"].append(f"Volume: ~{vol:.2f} SOL / {threshold} SOL {'✅' if passed else '❌'}")
            if passed: result["score"] += 1
        elif method == "nft_activity":
            # Simplified check
            result["details"].append("NFT activity: ⚠️ Manual check required")
            result["score"] += 0.5
        elif method == "lp_activity":
            result["details"].append("LP activity: ⚠️ Manual check required")
            result["score"] += 0.5

    result["eligible"] = result["score"] >= result["max_score"] * 0.5
    return result


def main():
    parser = argparse.ArgumentParser(description="Airdrop eligibility checker")
    parser.add_argument("address", help="Wallet address")
    parser.add_argument("--protocols", help="Comma-separated protocol keys (default: all)")
    args = parser.parse_args()

    protocols = args.protocols.split(",") if args.protocols else list(AIRDROP_RULES.keys())

    print(f"\n🪂 Airdrop Eligibility Check")
    print(f"   Wallet: {args.address[:8]}...{args.address[-4:]}")
    print(f"   Protocols: {len(protocols)}\n")

    results = []
    for proto in protocols:
        proto = proto.strip().lower()
        if proto not in AIRDROP_RULES:
            print(f"⚠️ Unknown protocol: {proto}")
            continue
        r = check_protocol(proto, args.address)
        results.append(r)

    print("═══════════════════════════════════════════════════════")
    for r in results:
        status = "🟢 ELIGIBLE" if r["eligible"] else "🟡 NOT YET"
        print(f"\n{r['logo']} {r['protocol']}: {status}")
        print(f"   Score: {r['score']:.1f} / {r['max_score']}")
        for d in r["details"]:
            print(f"   • {d}")

    print("\n═══════════════════════════════════════════════════════")
    print("\n⚠️  DISCLAIMER:")
    print("   • These checks are simplified heuristics, not official criteria")
    print("   • Past airdrops don't guarantee future ones")
    print("   • Always verify from official protocol announcements")
    print(f"   • Snapshot: {datetime.utcnow().isoformat()}Z\n")


if __name__ == "__main__":
    main()

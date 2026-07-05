#!/usr/bin/env python3
"""
💱 swap_helper.py — Jupiter Quote & Swap Helper

Get swap quote dari Jupiter Aggregator API (free, no key).
Menampilkan expected output, price impact, dan route detail.

Usage:
    python swap_helper.py <INPUT_MINT> <OUTPUT_MINT> <AMOUNT> [--slippage 0.5]

Example:
    python swap_helper.py So11111111111111111111111111111111111111112 EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 1000000000
    # Swap 1 SOL → USDC

Dependencies:
    pip install requests
"""
import os
import sys
import json
import argparse
import requests

JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_TOKENS_API = "https://token.jup.ag/strict"

# Token list cache
_token_cache = None


def get_token_list() -> dict:
    """Fetch Jupiter strict token list (cached)."""
    global _token_cache
    if _token_cache is None:
        try:
            resp = requests.get(JUPITER_TOKENS_API, timeout=15)
            resp.raise_for_status()
            _token_cache = {t["address"]: t for t in resp.json()}
        except Exception as e:
            print(f"⚠️ Token list fetch failed: {e}")
            _token_cache = {}
    return _token_cache


def token_label(mint: str) -> str:
    """Get human label for mint (symbol if known)."""
    tokens = get_token_list()
    t = tokens.get(mint)
    if t:
        return f"{t.get('symbol', '?')} ({t.get('name', '?')})"
    return f"{mint[:6]}...{mint[-4:]}"


def get_quote(input_mint: str, output_mint: str, amount: int,
              slippage_bps: int = 50) -> dict:
    """
    Get swap quote dari Jupiter.

    Args:
        input_mint: Input token mint
        output_mint: Output token mint
        amount: Amount in smallest unit (lamports for SOL)
        slippage_bps: Slippage in basis points (50 = 0.5%)

    Returns:
        Quote dict or {} on error
    """
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": slippage_bps,
    }
    try:
        resp = requests.get(JUPITER_QUOTE_API, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            err = e.response.json().get("error", "Unknown")
            print(f"❌ Quote error: {err}")
        else:
            print(f"❌ HTTP error: {e}")
        return {}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}


def format_quote(quote: dict, input_mint: str, output_mint: str) -> str:
    """Format quote untuk display."""
    if not quote:
        return "❌ No quote available"

    in_amount = int(quote.get("inAmount", 0))
    out_amount = int(quote.get("outAmount", 0))
    price_impact = float(quote.get("priceImpactPct", 0))
    route_plan = quote.get("routePlan", [])

    # Get decimals
    in_tokens = get_token_list()
    in_meta = in_tokens.get(input_mint, {})
    out_meta = in_tokens.get(output_mint, {})
    in_dec = in_meta.get("decimals", 9)
    out_dec = out_meta.get("decimals", 6)

    in_human = in_amount / (10 ** in_dec)
    out_human = out_amount / (10 ** out_dec)
    rate = out_human / in_human if in_human > 0 else 0

    lines = [
        "═══════════════════════════════════════════",
        f"  INPUT  : {in_human:,.6f} {token_label(input_mint)}",
        f"  OUTPUT : {out_human:,.6f} {token_label(output_mint)}",
        f"  RATE   : 1 {in_meta.get('symbol', 'IN')} = {rate:,.6f} {out_meta.get('symbol', 'OUT')}",
        f"  PRICE IMPACT: {price_impact:.4f}%",
        "═══════════════════════════════════════════",
    ]

    if route_plan:
        lines.append(f"  ROUTE  ({len(route_plan)} hop):")
        for hop in route_plan:
            swap = hop.get("swapInfo", {})
            lines.append(f"    → {swap.get('label', '?')} ({swap.get('inputMint', '?')[:6]}... → {swap.get('outputMint', '?')[:6]}...)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Jupiter swap quote helper")
    parser.add_argument("input_mint", help="Input token mint address")
    parser.add_argument("output_mint", help="Output token mint address")
    parser.add_argument("amount", type=int, help="Amount in smallest unit (lamports for SOL)")
    parser.add_argument("--slippage", type=float, default=0.5,
                        help="Slippage tolerance (percent, default 0.5)")
    args = parser.parse_args()

    print(f"\n💱 Jupiter Quote\n")
    slippage_bps = int(args.slippage * 100)
    quote = get_quote(args.input_mint, args.output_mint, args.amount, slippage_bps)
    print(format_quote(quote, args.input_mint, args.output_mint))

    if quote:
        print(f"\n🔗 To execute: use Jupiter UI https://jupiter.ag or jupiter-sdk")
        print(f"📋 Quote data (for SDK):")
        # Print compact for copy-paste
        compact = {k: quote[k] for k in ["inputMint", "outputMint", "inAmount", "outAmount", "otherAmountThreshold"] if k in quote}
        print(f"   {json.dumps(compact, indent=2)}")
    print()


if __name__ == "__main__":
    main()

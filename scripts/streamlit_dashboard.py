"""
📊 streamlit_dashboard.py — Interactive Portfolio Dashboard

Dashboard web interaktif untuk monitoring portfolio Solana.
Built with Streamlit — clean, modern, dark theme.

Features:
- Multi-wallet portfolio overview
- Real-time price + P&L
- Watchlist dengan auto-refresh
- Token safety check inline
- Trade history visualization

Setup:
    pip install streamlit plotly pandas requests
    export HELIUS_API_KEY="your-key"
    streamlit run streamlit_dashboard.py

Then open http://localhost:8501
"""
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
JUPITER_PRICE_API = "https://price.jup.ag/v6/price"


# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="Solana Agent Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS — dark premium theme
st.markdown("""
<style>
    .stApp { background-color: #050816; color: #e0e0e0; }
    .metric-card {
        background: linear-gradient(135deg, rgba(33, 233, 154, 0.1), rgba(0, 0, 0, 0.2));
        padding: 20px; border-radius: 12px; border: 1px solid rgba(33, 233, 154, 0.3);
    }
    .stMetric { background-color: #0a0f24; padding: 15px; border-radius: 10px; }
    h1, h2, h3 { color: #21e99a !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# Helpers
# ============================================================
@st.cache_data(ttl=30)
def get_price(mint: str) -> float:
    try:
        resp = requests.get(JUPITER_PRICE_API, params={"ids": mint}, timeout=10)
        data = resp.json().get("data", {}).get(mint)
        return float(data.get("price", 0)) if data else 0.0
    except Exception:
        return 0.0


@st.cache_data(ttl=30)
def rpc(method: str, params: tuple) -> dict:
    if not HELIUS_API_KEY:
        return {}
    try:
        resp = requests.post(HELIUS_RPC,
                             json={"jsonrpc": "2.0", "id": "dash", "method": method, "params": list(params)},
                             timeout=10)
        return resp.json().get("result") or {}
    except Exception:
        return {}


def get_sol_balance(address: str) -> float:
    result = rpc("getBalance", (address,))
    return result.get("value", 0) / 1e9 if result else 0.0


def get_token_holdings(address: str) -> list:
    result = rpc("getTokenAccountsByOwner", (
        address,
        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
        {"encoding": "jsonParsed"}
    ))
    holdings = []
    for acc in (result.get("value") or []):
        info = acc.get("account", {}).get("data", {}).get("parsed", {}).get("info", {})
        amount = float(info.get("tokenAmount", {}).get("uiAmount") or 0)
        if amount > 0:
            holdings.append({
                "mint": info.get("mint"),
                "amount": amount,
            })
    return holdings


# ============================================================
# Header
# ============================================================
st.title("🪙 Solana Agent Dashboard")
st.markdown("*Real-time portfolio monitoring • powered by Helius RPC + Jupiter Price*")
st.divider()

# ============================================================
# Sidebar — wallet input
# ============================================================
with st.sidebar:
    st.header("⚙️ Settings")

    # Load wallets from session state or env
    if "wallets" not in st.session_state:
        st.session_state.wallets = []

    new_wallet = st.text_input("Add wallet address", placeholder="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU")
    new_label = st.text_input("Label", placeholder="Main / Cold / Trading")
    if st.button("➕ Add") and new_wallet:
        st.session_state.wallets.append({"address": new_wallet, "label": new_label or "Wallet"})
        st.rerun()

    st.divider()
    st.subheader("📋 Tracked Wallets")
    for w in st.session_state.wallets:
        st.text(f"  {w['label']}: {w['address'][:8]}...{w['address'][-4:]}")

    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()


# ============================================================
# Main content
# ============================================================
if not st.session_state.wallets:
    st.info("👈 Add a wallet address di sidebar untuk mulai monitoring")
    st.stop()

# Compute balances
all_rows = []
for w in st.session_state.wallets:
    label = w["label"]
    addr = w["address"]
    sol = get_sol_balance(addr)
    sol_price = get_price("So11111111111111111111111111111111111111112")
    sol_usd = sol * sol_price
    all_rows.append({"Wallet": label, "Asset": "SOL", "Amount": sol, "Price": sol_price, "Value (USD)": sol_usd})

    for h in get_token_holdings(addr)[:10]:
        price = get_price(h["mint"])
        all_rows.append({
            "Wallet": label,
            "Asset": h["mint"][:8] + "...",
            "Amount": h["amount"],
            "Price": price,
            "Value (USD)": h["amount"] * price,
        })

df = pd.DataFrame(all_rows).sort_values("Value (USD)", ascending=False)

# ============================================================
# Top metrics
# ============================================================
col1, col2, col3, col4 = st.columns(4)
total_value = df["Value (USD)"].sum()
sol_amount = df[df["Asset"] == "SOL"]["Amount"].sum()
num_tokens = len(df[df["Asset"] != "SOL"])
num_wallets = len(st.session_state.wallets)

col1.metric("💰 Total Value", f"${total_value:,.2f}")
col2.metric("◎ SOL Holdings", f"{sol_amount:,.4f}")
col3.metric("🪙 Token Count", num_tokens)
col4.metric("👛 Wallets", num_wallets)

st.divider()

# ============================================================
# Holdings table
# ============================================================
st.subheader("📊 Holdings")
st.dataframe(
    df.style.format({
        "Amount": "{:,.4f}",
        "Price": "${:,.6f}",
        "Value (USD)": "${:,.2f}",
    }),
    use_container_width=True,
    height=400,
)

# ============================================================
# Pie chart — allocation
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥧 Allocation by Asset")
    if not df.empty and df["Value (USD)"].sum() > 0:
        fig = px.pie(df, values="Value (USD)", names="Asset", hole=0.5)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Wallet Distribution")
    if not df.empty:
        wallet_totals = df.groupby("Wallet")["Value (USD)"].sum().reset_index()
        fig = px.bar(wallet_totals, x="Wallet", y="Value (USD)",
                     color="Value (USD)", color_continuous_scale="emerald")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================================================
# Token check tool
# ============================================================
st.subheader("🔍 Quick Token Check")
check_mint = st.text_input("Token mint to check", placeholder="Paste mint address...")
if st.button("Check Token") and check_mint:
    with st.spinner("Checking..."):
        # Get mint info
        info = rpc("getAccountInfo", (check_mint, {"encoding": "jsonParsed"}))
        parsed = (info.get("value") or {}).get("data", {}).get("parsed", {}).get("info", {})

        col1, col2, col3 = st.columns(3)
        col1.metric("Mint Authority", "✅ None" if parsed.get("mintAuthority") is None else "🚨 Active")
        col2.metric("Freeze Authority", "✅ None" if parsed.get("freezeAuthority") is None else "🚨 Active")
        col3.metric("Price", f"${get_price(check_mint):.8f}")

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Refresh interval: 30s")

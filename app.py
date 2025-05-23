import streamlit as st
import time
from chat_history import save_chat_history, load_chat_history
from vector_store import create_vector_store, load_vector_store
from llm_service import create_qa_chain
from crypto_api import (
    get_price_from_exchange,
    get_market_data,
    get_latest_news,
    get_symbol_from_name
)
from langchain_core.documents import Document
from difflib import get_close_matches

def extract_crypto_symbol(query: str):
    top_50_cryptocurrencies = {
        "BTC": "Bitcoin",
        "ETH": "Ethereum",
        "USDT": "Tether",
        "BNB": "BNB",
        "SOL": "Solana",
        "XRP": "XRP",
        "USDC": "USD Coin",
        "DOGE": "Dogecoin",
        "TON": "Toncoin",
        "ADA": "Cardano",
        "AVAX": "Avalanche",
        "SHIB": "Shiba Inu",
        "WTRX": "Wrapped TRON",
        "DOT": "Polkadot",
        "WBTC": "Wrapped Bitcoin",
        "LINK": "Chainlink",
        "MATIC": "Polygon",
        "TRX": "TRON",
        "ICP": "Internet Computer",
        "NEAR": "NEAR Protocol",
        "BCH": "Bitcoin Cash",
        "LTC": "Litecoin",
        "UNI": "Uniswap",
        "LEO": "UNUS SED LEO",
        "DAI": "Dai",
        "APT": "Aptos",
        "STETH": "Lido Staked Ether",
        "ETC": "Ethereum Classic",
        "IMX": "Immutable",
        "MNT": "Mantle",
        "OKB": "OKB",
        "FDUSD": "First Digital USD",
        "CRO": "Cronos",
        "ARB": "Arbitrum",
        "RNDR": "Render",
        "HBAR": "Hedera",
        "TAO": "Bittensor",
        "FIL": "Filecoin",
        "VET": "VeChain",
        "INJ": "Injective",
        "ATOM": "Cosmos",
        "STX": "Stacks",
        "TIA": "Celestia",
        "OP": "Optimism",
        "PEPE": "Pepe",
        "KAS": "Kaspa",
        "LDO": "Lido DAO",
        "GRT": "The Graph",
        "USDP": "Pax Dollar",
        "RUNE": "THORChain"
    }

    query = query.lower()
    for name in top_50_cryptocurrencies:
        if name in query:
            return top_50_cryptocurrencies[name]

    matches = get_close_matches(query, top_50_cryptocurrencies.keys(), n=1, cutoff=0.6)
    if matches:
        return top_50_cryptocurrencies[matches[0]]

    return None

# Set up Streamlit page
st.set_page_config(
    page_title="Crypto Assistant",
    layout="wide"
)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()


if "vectorstore" not in st.session_state:
    try:
        st.session_state.vectorstore = load_vector_store()
    except FileNotFoundError:
        dummy_doc = Document(page_content="This is a dummy document to initialize the vector store.")
        st.session_state.vectorstore = create_vector_store([dummy_doc])

# Create QA chain if not created
if "qa_chain" not in st.session_state or st.session_state.qa_chain is None:
    st.session_state.qa_chain = create_qa_chain(st.session_state.vectorstore)

# Title and intro
st.title("🪙 AI Crypto Assistant")
st.markdown("Ask questions about top 50 cryptocurrencies. The assistant pulls live data from exchanges, news, and market cap services.")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask something like: 'What's the market cap of Solana?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Fetching data..."):
            try:
                user_query = prompt.lower()
                symbol = extract_crypto_symbol(user_query)

                if not symbol:
                    raise ValueError("Error, no information about this token")

                # Pull data
                price_info = get_price_from_exchange(symbol)
                market_data = get_market_data(symbol)
                news = get_latest_news(symbol)

                # Create context for the LLM
                context = f"""
                Symbol: {symbol}
                \nPrice Info:\n{price_info}
                \nMarket Data:\n{market_data}
                \nLatest News:\n{news}
                """

                # Get answer from LLM
                response = st.session_state.qa_chain({"context": context, "query": prompt})
                answer = response.get("result") if isinstance(response, dict) else response

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Save chat history
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                save_chat_history(prompt, answer, timestamp)
                st.session_state.chat_history = load_chat_history()
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar for chat history
with st.sidebar:
    st.header("🕘 Chat History")
    if st.button("📂 View History"):
        st.session_state.show_history = True

if st.session_state.get("show_history", False):
    st.header("📜 Chat History")
    if st.session_state.chat_history.empty:
        st.info("No chat history available.")
    else:
        st.dataframe(st.session_state.chat_history, use_container_width=True, hide_index=True)
        csv = st.session_state.chat_history.to_csv(index=False)
        st.download_button("Download Chat History", csv, "chat_history.csv", "text/csv", key='download-csv')

    if st.button("❌ Hide History"):
        st.session_state.show_history = False
        st.rerun()

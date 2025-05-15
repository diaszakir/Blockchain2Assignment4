# AI Crypto Assistant with Off-Chain Data Integration

## 📘 Overview

This project is an AI-powered assistant designed to answer user queries about the cryptocurrency market. It integrates live data from various off-chain sources, including crypto news services, exchanges, and market data providers, to provide real-time information on the top 50 cryptocurrencies by market capitalization.

## 🎯 Features

* **Live News Retrieval**: Fetches the latest news articles related to specific cryptocurrencies.
* **Real-Time Price Data**: Retrieves current price information from major crypto exchanges.
* **Market Data Insights**: Provides market capitalization and ranking details from platforms like CoinGecko or CoinMarketCap.
* **AI-Powered Responses**: Utilizes a GPT-based model to generate comprehensive answers based on aggregated data.

## 🛠️ Technologies Used

* **Programming Language**: Python
* **Web Framework**: Streamlit
* **AI Model**: GPT-based model (e.g., via Ollama)
* **Data Sources**:

  * News API: CryptoPanic, Cointelegraph, or similar
  * Exchange API: Binance, Coinbase, Kraken
  * Market Data API: CoinGecko, CoinMarketCap
* **Vector Store**: ChromaDB
* **Libraries**: LangChain, Requests, etc.

## 📂 Project Structure

```
├── app.py               # Main Streamlit application
├── main.py              # Entry point for backend processing
├── crypto_api.py        # Handles API interactions with exchanges and market data providers
├── chat_history.py      # Manages user query history
├── llm_service.py       # Interfaces with the GPT-based model
├── ollama_llm.py        # Specific implementation for Ollama LLM
├── vector_store.py      # Manages vector storage using ChromaDB
├── requirements.txt     # Python dependencies
└── .gitignore           # Specifies files to ignore in version control
```

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* API keys for:

  * Crypto news service (e.g., CryptoPanic)
  * Crypto exchange (e.g., Binance)
  * Market data provider (e.g., CoinGecko)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/diaszakir/Blockchain2Assignment4.git
   cd Blockchain2Assignment4
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   Create a `.env` file in the root directory and add your API keys:

   ```env
   CRYPTO_NEWS_API_KEY=your_news_api_key
   EXCHANGE_API_KEY=your_exchange_api_key
   MARKET_DATA_API_KEY=your_market_data_api_key
   ```

4. **Run the Application**:

   ```bash
   streamlit run app.py
   ```

## 💡 Usage

Once the application is running, you can interact with the AI assistant through the Streamlit interface. Enter queries such as:

* "What's the latest news about Ethereum?"
* "What is the current price and market cap of Solana?"

The assistant will fetch and aggregate data from the specified sources and provide a comprehensive response.

## 📸 Demo




## 📚 References

1. [RAG with ChromaDB and Ollama - Guide for Beginners](https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guidefor-beginners-30857499d0a0)
2. [Streamlit File Uploader Documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader)
3. [LangChain Document Transformers](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/)
4. [LangChain Tools Documentation](https://python.langchain.com/docs/concepts/tools/)



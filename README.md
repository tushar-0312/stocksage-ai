# StockSage AI

An intelligent stock market AI chatbot powered by LangGraph agents with real-time financial data, web search, and document-based knowledge retrieval.

## Features

- 🤖 **AI-Powered Trading Assistant** - Context-aware responses using DeepSeek LLM via Groq
- 📊 **Real-Time Financial Data** - Live stock data via Polygon API
- 🔍 **Web Search** - Up-to-date market news via Tavily
- 📚 **Document RAG** - Upload PDFs/DOCX to create custom knowledge base
- 💬 **Interactive UI** - Streamlit chat interface

## Quick Start

### 1. Setup Environment

```bash
# Create conda environment
conda create -p env python=3.10 -y
conda activate ./env

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
# Edit .env with your keys
```

### 3. Run the Application

**Start Backend:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Start UI (in another terminal):**
```bash
streamlit run streamlit_ui.py
```

### 4. Usage

1. Upload stock market documents via the sidebar
2. Ask questions about stocks, trading strategies, or market analysis
3. The AI agent will use appropriate tools (RAG, web search, financial data) to answer

## Project Structure

```
stocksage-ai/
├── agent/           # LangGraph agent workflow
├── config/          # YAML configuration
├── core/            # Core utilities (config, models, logging, exceptions)
├── data/samples/    # Sample documents
├── ingestion/       # Document ingestion pipeline
├── models/          # Pydantic schemas
├── tools/           # Agent tools (RAG, Polygon, Tavily)
├── main.py          # FastAPI backend
└── streamlit_ui.py  # Streamlit frontend
```

## Required API Keys

| Service | Purpose | Get Key |
|---------|---------|---------|
| Google | Embeddings | [AI Studio](https://aistudio.google.com/) |
| Groq | LLM (DeepSeek) | [Console](https://console.groq.com/) |
| Pinecone | Vector DB | [Pinecone](https://www.pinecone.io/) |
| Polygon | Stock Data | [Polygon](https://polygon.io/) |
| Tavily | Web Search | [Tavily](https://tavily.com/) |

## License

MIT License

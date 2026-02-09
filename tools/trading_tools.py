import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from core import load_config, ModelLoader
from models.schemas import RagToolInput

load_dotenv()

# Initialize shared resources
config = load_config()
model_loader = ModelLoader()
api_wrapper = PolygonAPIWrapper()


@tool(args_schema=RagToolInput)
def retriever_tool(question: str) -> str:
    """
    Search the stock market knowledge base for relevant information.
    Use this tool when the user asks about concepts, strategies, or information
    that might be covered in uploaded documents about stock trading and investing.
    """
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    
    vector_store = PineconeVectorStore(
        index=pc.Index(config["vector_db"]["index_name"]),
        embedding=model_loader.load_embeddings()
    )
    
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": config["retriever"]["top_k"],
            "score_threshold": config["retriever"]["score_threshold"]
        },
    )
    
    results = retriever.invoke(question)
    
    if not results:
        return "No relevant information found in the knowledge base."
    
    return "\n\n".join([doc.page_content for doc in results])


# Tavily web search tool
tavily_tool = TavilySearchResults(
    max_results=config["tools"]["tavily"]["max_results"],
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    name="web_search",
    description="Search the web for current stock market news, prices, and real-time information. Use this for up-to-date market data and news."
)


# Polygon financials tool
financials_tool = PolygonFinancials(
    api_wrapper=api_wrapper,
    description="Get financial data and fundamentals for publicly traded companies. Use this for earnings, revenue, balance sheets, and other financial metrics."
)


# Export all tools
all_tools = [retriever_tool, financials_tool, tavily_tool]

from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from agent import TradingAgent
from ingestion import DataIngestion
from models import QuestionRequest

app = FastAPI(
    title="StockSage AI",
    description="Intelligent stock market AI chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload", summary="Upload documents to knowledge base")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload PDF or DOCX files to create the stock market knowledge base."""
    try:
        ingestion = DataIngestion()
        ingestion.run_pipeline(files)
        return {"message": "Files successfully processed and stored."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/query", summary="Query the trading assistant")
async def query_chatbot(request: QuestionRequest):
    """Send a question to the StockSage AI trading assistant."""
    try:
        agent = TradingAgent()
        agent.build()
        graph = agent.get_graph()
        
        messages = {"messages": [request.question]}
        result = graph.invoke(messages)
        
        # Extract the final response
        if isinstance(result, dict) and "messages" in result:
            final_output = result["messages"][-1].content
        else:
            final_output = str(result)
        
        return {"answer": final_output}
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/health", summary="Health check")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "StockSage AI"}

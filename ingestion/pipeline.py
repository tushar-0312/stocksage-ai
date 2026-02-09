import os
import sys
import tempfile
from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec, Pinecone

from core import load_config, ModelLoader, StockSageException, logger


class DataIngestion:
    """Handle document loading, processing, and storage in Pinecone."""
    
    def __init__(self):
        try:
            logger.info("Initializing DataIngestion pipeline...")
            load_dotenv()
            self._validate_env()
            self.config = load_config()
            self.model_loader = ModelLoader()
        except Exception as e:
            raise StockSageException(e, sys)
    
    def _validate_env(self):
        """Validate required environment variables."""
        required_vars = ["GOOGLE_API_KEY", "PINECONE_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
    
    def load_documents(self, uploaded_files) -> List[Document]:
        """Load documents from uploaded files."""
        try:
            documents = []
            
            for uploaded_file in uploaded_files:
                file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
                suffix = file_ext if file_ext in [".pdf", ".docx"] else ".tmp"
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.file.read())
                    temp_path = temp_file.name
                
                if file_ext == ".pdf":
                    loader = PyPDFLoader(temp_path)
                    documents.extend(loader.load())
                elif file_ext == ".docx":
                    loader = Docx2txtLoader(temp_path)
                    documents.extend(loader.load())
                else:
                    logger.warning(f"Unsupported file type: {uploaded_file.filename}")
                
                # Cleanup temp file
                os.unlink(temp_path)
            
            logger.info(f"Loaded {len(documents)} documents")
            return documents
            
        except Exception as e:
            raise StockSageException(e, sys)
    
    def store_in_vector_db(self, documents: List[Document]):
        """Chunk and store documents in Pinecone."""
        try:
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(documents)
            logger.info(f"Split into {len(chunks)} chunks")
            
            # Initialize Pinecone
            pc = Pinecone(api_key=self.pinecone_api_key)
            index_name = self.config["vector_db"]["index_name"]
            
            # Create index if it doesn't exist
            existing_indexes = [idx.name for idx in pc.list_indexes()]
            if index_name not in existing_indexes:
                logger.info(f"Creating Pinecone index: {index_name}")
                pc.create_index(
                    name=index_name,
                    dimension=768,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
            
            # Store documents
            index = pc.Index(index_name)
            vector_store = PineconeVectorStore(
                index=index,
                embedding=self.model_loader.load_embeddings()
            )
            
            uuids = [str(uuid4()) for _ in range(len(chunks))]
            vector_store.add_documents(documents=chunks, ids=uuids)
            
            logger.info(f"Stored {len(chunks)} chunks in Pinecone")
            
        except Exception as e:
            raise StockSageException(e, sys)
    
    def run_pipeline(self, uploaded_files):
        """Run the complete ingestion pipeline."""
        try:
            documents = self.load_documents(uploaded_files)
            
            if not documents:
                logger.warning("No valid documents found")
                return
            
            self.store_in_vector_db(documents)
            logger.info("Ingestion pipeline completed successfully")
            
        except Exception as e:
            raise StockSageException(e, sys)

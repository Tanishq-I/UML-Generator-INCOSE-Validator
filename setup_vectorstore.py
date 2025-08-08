import os
import json
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

def setup_incose_vectorstore():
    """Create and persist the INCOSE vectorstore"""
    
    print("🚀 Setting up INCOSE vector database...")
    
    # Check if chunked data exists
    if not os.path.exists("chunked_incose.json"):
        print("❌ chunked_incose.json not found. Please ensure the file is in the UML directory.")
        return False
    
    try:
        # Load the chunked text
        print("📖 Loading chunked INCOSE data...")
        with open("chunked_incose.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        print(f"✅ Loaded {len(chunks)} chunks")
        
        # Convert chunks to LangChain Document objects
        docs = [Document(page_content=chunk) for chunk in chunks]
        
        # Set PyTorch to avoid meta tensor issues
        torch.set_default_dtype(torch.float32)
        
        # Initialize HuggingFace Embeddings model with device mapping fix
        print("🤖 Initializing embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={
                'device': 'cpu',
                'torch_dtype': torch.float32
            },
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Create and persist Chroma vector DB
        persist_dir = "chroma_db_incose"
        print(f"💾 Creating vector database at {persist_dir}...")
        
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        
        # Save to disk
        vectorstore.persist()
        
        print(f"✅ INCOSE vector database created successfully at: {persist_dir}")
        print(f"📊 Database contains {len(chunks)} document chunks")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create vectorstore: {e}")
        return False

if __name__ == "__main__":
    setup_incose_vectorstore()

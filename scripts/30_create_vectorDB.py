
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS


db_path = ".."+os.sep +"data"+os.sep +"vector_databases"
# Ensure the vector database directory exists
os.makedirs(db_path, exist_ok=True)

# Initialize the embedding model once
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

# Function to process a single PDF file
def createvector_from_file(doc_path, file_name):
    try:
        # Load PDF
        file_name = os.path.splitext(file_name)[0]
        file_path = os.path.join(doc_path, file_name)
        loader = PyPDFLoader(file_path=file_path+".pdf")	
        documents = loader.load()

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
        chunks = text_splitter.split_documents(documents=documents)

        # Create vector store
        vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)

        # Save vector store
        vectorstore.save_local(os.path.join(db_path, f"{file_name}_vector_db"))
        print(f"Processed and saved vector store for {file_name}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def createvector_from_directory(doc_path):
    # Iterate over all PDF files in the directory
    for file in os.listdir(doc_path):
        if file.endswith(".pdf"):
            file_name = os.path.splitext(file)[0]
            file_path = os.path.join(doc_path, file)
            process_pdf(file_path, file_name)


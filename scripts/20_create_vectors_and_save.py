# This is a library to create vector embeddings from PDF and XML files and save them in a local directory using Langchain and FAISS.
# It has two main functions:
# - createvector_from_file: Processes a single PDF file, splits it into chunks, creates a vector store, and saves it locally.   
# - createvector_from_directory: Iterates over all PDF files in a specified directory and processes each one using createvector_from_file.
# |---------|-----------|--------|--------------|
import os
import sys
import re
from bs4 import BeautifulSoup
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, UnstructuredXMLLoader
from langchain_community.vectorstores import FAISS

# check if it is split to chunks and create embedding
db_path = "data"+"/" +"vector_databases"
# Ensure the vector database directory exists
os.makedirs(db_path, exist_ok=True)

# Initialize the embedding model once
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

#----------------------------------------------------------------------------------------
# Clean malformed XML attributes (e.g., missing crossorigin values)
def clean_invalid_xml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add default value for crossorigin if missing
        content = content.replace('crossorigin>', 'crossorigin="anonymous">')
        content = content.replace('crossorigin/>', 'crossorigin="anonymous"/>')

        # Escape standalone ampersands not followed by valid entities
        content = re.sub(r'&(?![a-zA-Z]+;|#[0-9]+;|#x[0-9A-Fa-f]+;)', '&amp;', content)

        # Find all XML declarations
        xml_decls = re.findall(r'<\?xml[^>]*\?>', content)

        # Keep only the first one (if any), remove all others
        if xml_decls:
            first_decl = xml_decls[0]
            content = re.sub(r'<\?xml[^>]*\?>', '', content)
            content = first_decl + '\n' + content.lstrip()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error cleaning XML file {file_path}: {e}")
#----------------------------------------------------------------------------------------
# Function to process a single file PDF or XML
def createvector_from_file(doc_path, file_name):
    try:

        # Extract the file extension
        file_ext = os.path.splitext(file_name)[1].lower()
        base_name = os.path.splitext(file_name)[0]
        vectorstore_path = os.path.join(db_path, f"{base_name}_vector_db")
        file_path = os.path.join(doc_path, file_name)

        # Skip if the vector store already exists
        if os.path.exists(vectorstore_path):
            print(f"Vector store already exists for {file_name}. Skipping.")
            return

        # Load the document based on the file extension:
        if file_ext == ".pdf":
            # Initialize the PDF loader with the file path
            loader = PyPDFLoader(file_path=file_path)
        elif file_ext == ".xml":
            clean_invalid_xml(file_path)
            # Initialize the XML loader with the file path
            loader = UnstructuredXMLLoader(file_path=file_path, mode="elements")
        else:
            print(f"Unsupported file type: {file_ext}. Only .pdf and .xml are supported.")
            return
            

        #load the content of the file into a list of documents where each document is a dictionary with the keys "page_content" and "metadata"	
        documents = loader.load()

        # Split into chunks:
        # Initialize the text splitter with chunk size and overlap
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
        # Split the documents into smaller chunks
        chunks = text_splitter.split_documents(documents=documents)

        # Create vector store
        vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)

        # Save vector store

        base_name = os.path.splitext(file_name)[0]
    
        vectorstore.save_local(vectorstore_path)
        print(f"Processed and saved vector store for {file_name}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
#----------------------------------------------------------------------------------------
def createvector_from_directory(doc_path):
    """
    Example argument "../data/test_dir/"
    """
    # Iterate over all PDF files in the directory
    for file in os.listdir(doc_path):
        if file.lower().endswith((".pdf", ".xml")):
            createvector_from_file(doc_path, file)

#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage
    doc_path = "data"+ "/" +"springer_longevity_docs"
    createvector_from_directory(doc_path)
    # createvector_from_file(doc_path, "example.pdf")

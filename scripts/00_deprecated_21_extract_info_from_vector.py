from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
#import pandas as pd
from typing import List, Dict

# Function to load vector store
def load_vector_store(vector_db_path):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    vector_store = FAISS.load_local(folder_path=vector_db_path, embeddings=embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever()
    return retriever

def extract_institution(content):
    return "fake Institution"  # Implement this function based on your criteria

def determine_peer_review_status(content):
    return "Per review not defined"  # Implement this function based on your criteria

def assess_relevance(content):
    return "relevance : unknown"  # Implement this function based on your criteria

def generate_summary(content):
    return "summary : not yet"  # Implement this function based on your criteria




def extract_document_info_from_faiss(faiss_vector_store) -> List[Dict]:
    """
    Extracts information from the single document in the FAISS vector store.

    Parameters:
    - faiss_vector_store: The FAISS vector store instance containing one document.

    Returns:
    - A list containing a dictionary with extracted information from the document.
    """
    # Access the single document directly
    doc_id = list(faiss_vector_store.docstore._dict.keys())[0]
    doc = faiss_vector_store.docstore._dict[doc_id]

    # Define default values
    default_values = {
        'Author': 'Not Available',
        'Date': 'Not Available',
        'Institution': 'Not Available',
        'Peer Reviewed': 'Not Available',
        'Text': 'Not Available'
    }

    # Extract metadata with defaults
    metadata = doc.metadata if hasattr(doc, 'metadata') else {}
    author = metadata.get('author', default_values['Author'])
    creation_date = metadata.get('creationdate', default_values['Date'])
    institution = metadata.get('institution', default_values['Institution'])
    peer_reviewed = metadata.get('peer_reviewed', default_values['Peer Reviewed'])

    # Convert creation_date to a standard format if possible
    if creation_date != default_values['Date']:
        try:
            creation_date = pd.to_datetime(creation_date, errors='coerce')
            if pd.isnull(creation_date):
                creation_date = default_values['Date']
            else:
                creation_date = creation_date.date()
        except Exception:
            creation_date = default_values['Date']

    # Extract content
    content = doc.page_content if hasattr(doc, 'page_content') else default_values['Text']

    # Compile extracted information into a dictionary
    document_info = {
        'Author': author,
        'Date': creation_date,
        'Institution': institution,
        'Peer Reviewed': peer_reviewed,
        'Text': content
    }

    return [document_info]


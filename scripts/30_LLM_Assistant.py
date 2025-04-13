
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd
import os
import re
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

def extract_file_name(path):
    """
    Extracts the folder name ending with '_vector_db' from the given path.
    Returns the folder name without the '_vector_db' suffix if the directory exists.
    Raises an exception if the directory does not exist or the pattern is not found.
    """
    # Normalize the path to handle different OS path separators
    normalized_path = os.path.normpath(path)
    
    # Check if the directory exists
    if not os.path.isdir(normalized_path):
        raise FileNotFoundError(f"Directory does not exist: {normalized_path}")
    
    # Use regex to extract the folder name ending with '_vector_db'
    match = re.search(r'([^{}]+)_vector_db$'.format(re.escape(os.sep)), normalized_path)
    if match:
        return match.group(1)
    else:
        raise ValueError("The path does not contain a folder ending with '_vector_db'.")
# end of function

import os
import re

def extract_parent_path(path):
    """
    Extracts the parent path that comes before the folder ending with '_vector_db'.
    Returns the parent path if the directory exists.
    Raises an exception if the directory does not exist or the pattern is not found.
    """
    # Normalize the path for cross-platform compatibility
    normalized_path = os.path.normpath(path)

    # Check if the directory exists
    if not os.path.isdir(normalized_path):
        raise FileNotFoundError(f"Directory does not exist: {normalized_path}")
    
    # Split the path
    base_name = os.path.basename(normalized_path)
    if not base_name.endswith('_vector_db'):
        raise ValueError("The path does not end with '_vector_db'.")

    # Get the parent path before the folder
    parent_path = os.path.dirname(normalized_path)
    return parent_path
# end of function

# LLM section



model_id = "llama3-8b-8192"
doc_ext =".pdf"


# Set the model ID and parameters
llm = ChatGroq(
    model=model_id,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


def retrieve_from_vector_db(vector_db_path):
    """
    this function splits out a retriever object from a local vector database

    """
    # instantiate embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-mpnet-base-v2'
    )
    react_vectorstore = FAISS.load_local(
        folder_path=vector_db_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = react_vectorstore.as_retriever()
    return retriever
# end of function



def connect_chains(retriever):
    """
    this function connects stuff_documents_chain with retrieval_chain
    """
    stuff_documents_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=hub.pull("langchain-ai/retrieval-qa-chat")
    )
    retrieval_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=stuff_documents_chain
    )
    return retrieval_chain
# end of function


def print_output(inquiry, retrieval_chain):
    result = retrieval_chain.invoke({"input": inquiry})
    return(result['answer'].strip("\n"))
# end of function



def make_list_from_vectordb(vectordb_location):
    """
    This function takes one vector database location and extracts a list with the fields: "File_Name","Relevance_for_longevity","Date_of_publication", "Author","Institution","Peer Reviewed","Summary"
    """
    # Assuming `vectordb` is a pre-defined variable representing the vector database
    # and `get_all_documents` is a method to fetch all documents from it.
 
    list = []

       
    # Filename:
    try:
        file_name = extract_file_name(vectordb_location)
        #print(f"Extracted file name: {file_name}")
    except Exception as e:
        print(f"Error: {e}")

    #LLM needs
    db_path = extract_parent_path(vectordb_location) + os.sep
    doc_retriever = retrieve_from_vector_db(db_path+file_name+"_vector_db")	# to be used as argument in connect_chains function
    doc_retrieval_chain = connect_chains(doc_retriever) # to be used as argument in print_output function
    
    try:
        relevance_for_longevity = print_output("Please assign a relevance between 0 and 1 of this document to longevity, and write only the number",doc_retrieval_chain)
    except Exception as e:
        print(f"Error: {e}")

    try:
        date_of_publication = print_output("if there is a date of publication of the document, Please write only the date of publication, if there is no date of publication, please write only today's date.",doc_retrieval_chain)
    except Exception as e:
        print(f"Error: {e}")

    author = print_output("Please write only the name of the author of this document, if there is no author mentioned, write only unknown",doc_retrieval_chain)
    institution = print_output("Please write just the name of the institution that published this article, if it not clear just write unclear",doc_retrieval_chain)
    peer_reviewed = print_output("if there is an indication that this document is peer reviewed, please write yes, otherwise unclear",doc_retrieval_chain)
    summary = print_output("Please write a brief summary of the document",doc_retrieval_chain)

    # Creating a dictionary for each document and appending it to the list
    document_info = {
        "File_Name": file_name,
        "Relevance_for_longevity": relevance_for_longevity,
        "Date_of_publication": date_of_publication,
        "Author": author,
        "Institution": institution,
        "Peer Reviewed": peer_reviewed,
        "Summary": summary
    }
        
    list.append(document_info)
    return list
# end of function





def build_dataframe_from_vector_dbs(root_dir, output_path ,verbose=False):
    """
    Iterates through directories inside `root_dir`, applies `make_list_from_vector_db`
    to each, and appends the results into a DataFrame.

    Parameters:
    - root_dir (str): Path to the folder containing multiple vector DB directories.
    - output_path he path and destination of the target file, including the extension csv
    - verbose (bool): If True, prints progress information.

    Returns:
    - pd.DataFrame: Combined DataFrame from all vector DB outputs.
    """
    combined_data = []

    # Get only the directories
    folder_names = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]

    for folder_name in tqdm(folder_names, desc="Processing vector DBs"):
        folder_path = os.path.join(root_dir, folder_name)
        
        try:
            result = make_list_from_vectordb(folder_path)
            combined_data.extend(result)  # assumes result is a list of dicts
            df = pd.DataFrame(combined_data)
            df.to_csv(output_path, index=False)
            if verbose:
                print(f"Processing: {folder_path}")

        except Exception as e:
            if verbose:
                print(f"Error processing {folder_path}: {e}")
            continue

    
    return df


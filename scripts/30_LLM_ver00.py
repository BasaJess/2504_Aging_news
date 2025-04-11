
from langchain.prompts.prompt import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

import os
import warnings
warnings.filterwarnings("ignore")


load_dotenv()


model_id = "llama3-8b-8192"
file_name = os.sep+ "LifespanPodcast_Episode_2"
doc_ext =".pdf"
doc_path = "data" + os.sep + "Training_docs"  #"../data/Training_docs/"
db_path = "data" + os.sep + "vector_databases"

# Set the model ID and parameters
llm = ChatGroq(
    model=model_id,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)




def load_pdf_data(pdf_file_path):
    """
    this function loads text data from pdf file
    """
    loader = PyPDFLoader(file_path=pdf_file_path)
    documents = loader.load()
    return documents


def split_to_chunks(documents, chunk_size=800, chunk_overlap=80):
    """
    this function splits documents into chunks of given size and overlap
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents=documents)##arning ,may be recursive
    return chunks


def create_embedding_vector_db(chunks, file_name, target_directory=f""+db_path):
    """
    this function uses the open-source embedding model HuggingFaceEmbeddings 
    to create embeddings and store those in a vector database called FAISS, 
    which allows for efficient similarity search
    """
    # instantiate embedding model
    embedding = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-mpnet-base-v2'
    )
    # create the vector store 
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embedding
    )
    # save vector database locally
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    vectorstore.save_local(f"{target_directory}/{file_name}_vector_db")


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


loaded_pdf =  load_pdf_data(doc_path+file_name+doc_ext)


doc_chunks = split_to_chunks(loaded_pdf)


create_embedding_vector_db(chunks=doc_chunks, file_name = file_name, target_directory=db_path)


doc_retriever = retrieve_from_vector_db(db_path+file_name+"_vector_db")	


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


doc_retrieval_chain = connect_chains(doc_retriever)


def print_output(
    inquiry,
    retrieval_chain=doc_retrieval_chain
):
    result = retrieval_chain.invoke({"input": inquiry})
    print(result['answer'].strip("\n"))


print_output("Give me the summary the text in 3 sentences.")


print_output("Give me the latest findings for longevity.")

def return_my_question():
    return "Give me the latest findings for longevity."



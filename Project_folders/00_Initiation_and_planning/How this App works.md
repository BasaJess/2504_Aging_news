# Modular
- It uses a "modular" approach to make easiet to switch pieces
- The process is driven through the scripts in the scrips folders
- The Jupyter notebooks can be and had been used as auxiliary help to call functions and test

Below a more detailed explanation of the funtionality on most of the files and their relation with the Pipeline

00_deprecated files:  to be deleted later as soon as we are sure tey are no longer needed as a reference

10_SN_Pub_retrieval: All the files with 10 at the beginning are to be used to retrieve new documents from the API's

 - For example Using the 10_SN_Pub_retrieval.fetch_papers_from_SpringerNature() Funcion
   - Retrieves
   - Stores
   - There are other functions but their are intended to be called only by the function above
   - These group of scripts stores the retrieved docs in a directory in file either PDF or XML

20_ Create_vectors_and_save
  - createvector_from_directory(doc_path) is this script Interface function
  - It uses createvector_from_file(doc_path, file_name) internally
  - The doc_path is the directory holding the PDF's or XML's stored by the 10_XXX_Scripts
  - Ir stores the vectors with the ending: "vector_db" in files in the vector_databases directory
 
31_Build_df_from_docsdb 
 - create a df from all the docs in a directory of vector_db by using the:
 - function build_dataframe_from_many_docs_vectordbs(root_dir, output_path ,verbose=False)
 - from the LLM Assistant 30_LLM_Assistant
 - It does not save the df in file, if needed or wanted, that has to be done by the caller
 - The whole functionality of this script was done previously using jupyter notebooks, now needs to be implemented

32_Data_cleaner.py
 - clean_and_save_docs_df(df)
 - saves the cleaned data in "cleaned_docs_info.csv"
 - If the caller wants to retrieve the df from file, it has to be done "manually"

34_Most_relevant_docs_list_maker.py
 - takes the data from "cleaned_docs_info.csv"

40_Stemlit_v00 : is the actual app
 - calls 34_Most_relevant_docs_list_maker.retrieve_most_relevant_docs_for_streamlit()

 Here is a graphic description

 [Pipeline](../../images/)
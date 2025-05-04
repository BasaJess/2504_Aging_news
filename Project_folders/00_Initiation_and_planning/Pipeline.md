# **Pipeline:**

Step 1\. Data fetching:

1. from APIs for Scientific Articles:
   1. arXiv API (open-access scientific papers) was used as first source and 701 pdf retrieved
   2. Springernature API (For biomedical research on a Agin and Nature Journals)
   3. www.cell.com API 
   4. bioXriv  Signer Lab has published there
   5. Semantic Scholar API (wide range of research papers)  
   6. CrossRef API (DOI-based paper research)  
2. Web Scraping  
   1. Use Scrapy or BeautifulSop for open-access journals.  
   2. Check on permissions and legal use.
   3. https://gurcohenlab.com/
   4. https://signerlab.com/

Step 2\. Preprocessing and Storage:

1. Convert PDFs or XMLS to text using pdfminer or PyMuPDF to vectors and embeddings and store them in File 
2. Clean data (keep references, figures, etc.)  
3. Store in a structured format

Step 3\. LLM for Information Extraction:

1. Using LLM, Classify if neede, assign relevance score, obtain metadata and summarize each doc in the db

Step 4\. Analysis and Insights:

1. Build a chatbot or dashboard to query the findings.
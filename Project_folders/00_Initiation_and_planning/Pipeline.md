# **Pipeline:**

Also visually describedn in the [Power Point Presentation](../08_Documentation_and_reporting/About%20staying%20young.pptx)

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

Step 2\. Storage and First LLM Processing:

1. Convert PDFs or XMLS to vectors and embeddings and store them in File 
2. Assign relevance, Extract important Information and Summarize 
3. Store in file

Step 3\. Clean data and store as a Dtaframe in file:

1. Using python scripting, Classify if needed, assign relevance score, obtain metadata and summarize each doc
2. Create a DF, clean the data
3. Store in file

Step 4\. Second LLM:

1. Retrieve thd DF from file
2. Sort by relevance and date
3. Store in file 

Step 5\. Update and upload to the streamit app

1. Update and check that the scrip for the app is correct.
1. Upload to github including necessary data since the folder data is in gitignore.
1. fon a next iteration: Build a chatbot or dashboard to query the findings.
This document shows how the NLP component can be implemented through the use of the Term Frequency-Inverse Document Frequency (TF-IDF) technique within the `compute_relevance_score` function. This function assesses the relevance of each PDF's text content to the topic of healthspan extension by calculating the importance of predefined healthspan-related keywords.

Here's how the NLP is applied:

 1. *Vectorization with TF-IDF:* The `TfidfVectorizer` from the `sklearn.feature_extraction.text` module is employed to convert the text data into numerical values. This transformation allows for the evaluation of the significance of specific terms within the documents.
 2. *Keyword Specification:* A vocabulary of healthspan-related keywords is defined, including terms such as 'healthspan', 'longevity', 'aging', and 'senescence'. The vectorizer focuses on these terms to determine their prominence in each document.
 3. *Relevance Scoring:* The TF-IDF values for the specified keywords are computed for each document. The sum of these values serves as the relevance score, indicating how pertinent the document is to the healthspan extension topic.

 By leveraging TF-IDF, a common NLP technique, the code quantifies the importance of specific terms within the documents, facilitating the identification of papers most relevant to healthspan extension. [Guide to TF-IDF](https://builtin.com/articles/tf-idf)
 
 ---
 
 #### Extract metadata and content from PDFs

```
# install libraries
pip install PyPDF2

# Extract Text and Metadata

import os
import re
from PyPDF2 import PdfReader
from datetime import datetime

def extract_pdf_info(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        metadata = reader.metadata
        title = metadata.get('/Title', 'Unknown Title')
        author = metadata.get('/Author', 'Unknown Author')
        creation_date = metadata.get('/CreationDate', '')
        mod_date = metadata.get('/ModDate', '')

        # Extract date from metadata
        date_str = creation_date or mod_date
        date_match = re.search(r"D:(\d{14})", date_str)
        if date_match:
            date = datetime.strptime(date_match.group(1), '%Y%m%d%H%M%S')
        else:
            date = None

        return {'title': title, 'author': author, 'date': date, 'text': text}

# Directory containing PDFs
pdf_dir = '/path/to/pdf_directory'

# Extract information from all PDFs
pdf_info_list = []
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        pdf_info = extract_pdf_info(pdf_path)
        pdf_info['filename'] = pdf_file
        pdf_info_list.append(pdf_info)
```
Fiter and sort by date

```
 # Filter out PDFs without a date
dated_pdfs = [pdf for pdf in pdf_info_list if pdf['date'] is not None]

# Sort PDFs by date (newest first)
sorted_pdfs = sorted(dated_pdfs, key=lambda x: x['date'], reverse=True)

# Select the 20 most recent PDFs
recent_pdfs = sorted_pdfs[:20]
```
#### Classify relevance to healthspan extension

```
# Install NLP Libraries:

pip install scikit-learn

# Define Keywords and Scoring Function:

from sklearn.feature_extraction.text import TfidfVectorizer

# Define healthspan-related keywords
healthspan_keywords = [
    'healthspan', 'longevity', 'aging', 'anti-aging', 'lifespan extension',
    'senescence', 'caloric restriction', 'telomeres', 'gerontology', 'sirtuins'
]

def compute_relevance_score(text):
    vectorizer = TfidfVectorizer(vocabulary=healthspan_keywords, stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([text])
        score = tfidf_matrix.sum()
    except ValueError:
        score = 0
    return score

# Compute relevance scores for the 20 most recent PDFs
for pdf in recent_pdfs:
    pdf['relevance_score'] = compute_relevance_score(pdf['text'])

# Filter PDFs with relevance score above a certain threshold
relevant_pdfs = [pdf for pdf in recent_pdfs if pdf['relevance_score'] > 0]

# Sort relevant PDFs by relevance score (highest first)
sorted_relevant_pdfs = sorted(relevant_pdfs, key=lambda x: x['relevance_score'], reverse=True)
```
Output the relevant papers
```
 for pdf in sorted_relevant_pdfs:
    print(f"Title: {pdf['title']}")
    print(f"Author: {pdf['author']}")
    print(f"Date: {pdf['date'].strftime('%Y-%m-%d')}")
    print(f"Filename: {pdf['filename']}")
    print(f"Relevance Score: {pdf['relevance_score']:.2f}")
    print("-" * 80)
```
##### Notes:
 - The `extract_pdf_info` function retrieves the title, author, creation or modification date, and text content from each PDF.
 - PDFs without a valid date are excluded from the sorting process.
 - The `compute_relevance_score` function calculates a TF-IDF-based score using predefined healthspan-related keywords. Adjust the `healthspan_keywords` list to better match your specific area of interest.
 - The relevance threshold can be modified to fine-tune the selection criteria.


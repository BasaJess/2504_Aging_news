### Cleanse and Normalize the Data, addressing issues like duplicates, missing values, and inconsistent formatting
---

NLP models cannot directly process raw PDF files, which are designed for visual presentation, not data extraction

 1. _Extraction:_ Getting the text out of the PDFs using libraries like `PyPDF2`, `pdfminer.six`, or `OCR` if needed.
 2. _Text Cleaning:_ Removing noise like headers, footers, special characters, and standardizing the text.
 3. _Organization (Optional but Recommended):_ Structuring the extracted text into sentences, paragraphs, or sections, and potentially extracting metadata.

Preprocessing PDF data is a crucial step for achieving good results with NLP models.


Here's a breakdown of the steps with code examples using popular libraries. Keep in mind that the specific steps and code will vary depending on the complexity and structure of your PDF files.


1. _Extraction:_
  - Install necessary libraries:
    ```
    pip install PyPDF2 pdfminer.six tabula-py
    # For OCR if needed:
    pip install pytesseract Pillow
    # You might also need to install the Tesseract OCR engine separately
    # depending on your operating system.

  - Extract text from PDFs (without tables):
    ```
    import PyPDF2
    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    pdf_file = "your_document.pdf"
    raw_text = extract_text_from_pdf(pdf_file)
    print(raw_text[:500]) # Print first 500 characters to inspect

  - Extract text from PDFs (with potential for better layout handling):
    ```
    from pdfminer.high_level import extract_text

    def extract_text_with_pdfminer(pdf_path):
        text = extract_text(pdf_path)
        return text

    pdf_file = "your_document.pdf"
    raw_text = extract_text_with_pdfminer(pdf_file)
    print(raw_text[:500])

  - Extract text from scanned PDFs (using OCR):
    ```
    from PIL import Image
    import pytesseract
    import PyPDF2

    def extract_text_from_scanned_pdf(pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                # Save each page as an image
                image = page.to_image()
                image.save(f"temp_page_{page_num}.png")
                # Use Tesseract to extract text from the image
                page_text = pytesseract.image_to_string(Image.open(f"temp_page_{page_num}.png"))
                text += page_text
                import os
                os.remove(f"temp_page_{page_num}.png") # Clean up temporary image
        return text

    pdf_file = "scanned_document.pdf"
    raw_text = extract_text_from_scanned_pdf(pdf_file)
    print(raw_text[:500])

2. _Text Cleaning:_
  - Install NLTK (for more advanced text processing):
    ```
    pip install nltk
    import nltk
    nltk.download('punkt') # Download sentence tokenizer
    nltk.download('stopwords') # Download stop words list
  - Basic Cleaning Functions:
    ```
    import re
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize

    def clean_text(text):
        # Remove headers, footers, page numbers (adjust regex based on your document structure)
        text = re.sub(r'^\s*[\d]+\s*$', '', text, flags=re.MULTILINE) # Remove lines with only numbers (likely page numbers)
        text = re.sub(r'^\s*.*?header.*?\n', '', text, flags=re.MULTILINE | re.IGNORECASE) # Example header removal
        text = re.sub(r'\n.*?footer.*?\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE) # Example footer removal

        # Handle line breaks and hyphenation
        text = re.sub(r'-\n', '', text) # Join hyphenated words split across lines
        text = re.sub(r'\n', ' ', text) # Replace newlines with spaces

        # Remove special characters and punctuation
        text = re.sub(r'[^\w\s]', '', text)

        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    cleaned_text = clean_text(raw_text)
    print(cleaned_text[:500])

  - More Advanced Cleaning (using NLTK):
    ```
    def advanced_clean_text(text):
        text = clean_text(text) # Apply basic cleaning first

        # Tokenization
        sentences = sent_tokenize(text)
        words = [word for sent in sentences for word in sent.split()]

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

        # Consider stemming or lemmatization (NLTK provides tools for this)
        # from nltk.stem import PorterStemmer
        # stemmer = PorterStemmer()
        # words = [stemmer.stem(word) for word in words]

        return " ".join(words)

    advanced_cleaned_text = advanced_clean_text(raw_text)
    print(advanced_cleaned_text[:500])

3. _Organization:_
  - Sentence Segmentation (already done in advanced_clean_text):
    ```
    sentences = sent_tokenize(cleaned_text)
    print(sentences[:5])

  - Paragraph Segmentation (can be tricky, often relies on blank lines):
    ```
    def get_paragraphs(text):
        # Split by double newlines (common paragraph separator)
        paragraphs = text.split('\n\n')
        # Clean up each paragraph
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs

    paragraphs = get_paragraphs(raw_text) # Use raw_text as cleaning might remove paragraph breaks
    print(paragraphs[:2])

  - Document Structuring (more complex, depends heavily on PDF structure):
    - This often requires more specific logic based on visual cues or consistent formatting patterns in your PDFs. You might need to identify headings, subheadings, and associate text with them. Libraries like `pdfminer.six` can sometimes provide more information about the layout that can be helpful here.

  - Metadata Extraction (if available in the PDF):
    ```
    def extract_metadata(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            info = reader.metadata
        return info

    pdf_file = "your_document.pdf"
    metadata = extract_metadata(pdf_file)
    print(metadata)

Putting it all together (Example Workflow):
```
pdf_file = "your_document.pdf"

# 1. Extract Text
raw_text = extract_text_with_pdfminer(pdf_file)

# 2. Clean Text
cleaned_text = clean_text(raw_text)
# or
advanced_cleaned_text = advanced_clean_text(raw_text)

# 3. Organize (Example: Sentence Segmentation)
sentences = sent_tokenize(cleaned_text)
print(sentences[:10])

# If you have tables:
tables = extract_tables_from_pdf(pdf_file)
for i, table in enumerate(tables):
    # Process each table (e.g., convert to string, clean)
    table_string = table.to_string()
    cleaned_table_string = clean_text(table_string)
    print(f"--- Cleaned Table {i+1} ---")
    print(cleaned_table_string)


#### Important Considerations:
 - _Complexity of PDFs:_ The more complex the layout of your PDFs (e.g., multiple columns, images with text overlays), the more challenging extraction and cleaning will be.
 - _Consistency:_ If your PDFs have a consistent structure, you can write more targeted cleaning and organization logic.
 - _Error Handling:_ Implement error handling (e.g., try-except blocks) to gracefully manage issues like corrupted PDFs or unexpected formatting.
 - _Inspection:_ Always inspect the output of each step to ensure the cleaning and organization are working as expected. Print snippets of the text or tables to verify.
 - _Iterative Process:_ Cleaning and organizing data is often an iterative process. You might need to adjust your cleaning functions based on the initial results.
 - _Task-Specific Cleaning:_ The level of cleaning required depends on your specific NLP task. For example, you might not need to remove stop words for named entity recognition.
By following these steps and adapting the code to your specific PDF data, you can effectively clean and organize your data for NLP tasks in Python. Remember to start with simpler methods and gradually increase complexity as needed


---

#### To iterate through all PDFs in a directory, we need to modify the code to:
1. Get a list of all PDF files in the directory.
2. Loop through that list, applying the extraction, cleaning, and organization functions to each PDF file.


```
import os
import PyPDF2
from pdfminer.high_level import extract_text
import re
from nltk.tokenize import sent_tokenize

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error processing {pdf_path} with PyPDF2: {e}")
        return None

def extract_text_with_pdfminer(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error processing {pdf_path} with pdfminer.six: {e}")
        return None

def clean_text(text):
    if text is None:
        return ""
    # Remove headers, footers, page numbers (adjust regex based on your document structure)
    text = re.sub(r'^\s*[\d]+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*.*?header.*?\n', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'\n.*?footer.*?\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_pdf(pdf_path):
    print(f"Processing: {pdf_path}")
    # 1. Extract Text (try different methods)
    raw_text = extract_text_with_pdfminer(pdf_path)
    if not raw_text:
        raw_text = extract_text_from_pdf(pdf_path)

    if raw_text:
        # 2. Clean Text
        cleaned_text = clean_text(raw_text)

        # 3. Organize (Example: Sentence Segmentation)
        sentences = sent_tokenize(cleaned_text)
        print(f"First 10 sentences from {pdf_path}:\n{sentences[:10]}\n{'='*50}")
        # You can do further processing here, like storing the data

    else:
        print(f"Could not extract text from {pdf_path}")

##### Specify the directory containing your PDF files
pdf_directory = "/path/to/your/pdf/directory"

###### Get a list of all files in the directory
all_files = os.listdir(pdf_directory)

###### Filter the list to include only PDF files (you might need to adjust the extension check)
pdf_files = [os.path.join(pdf_directory, f) for f in all_files if f.lower().endswith(".pdf")]

###### Iterate through the list of PDF files and process each one
for pdf_file_path in pdf_files:
    process_pdf(pdf_file_path)

print("Finished processing all PDF files.")

#### _Explanation of Changes:_
 - _import os:_ This line imports the os module, which provides functions for interacting with the operating system, including listing files in a directory.
 - pdf_directory = "/path/to/your/pdf/directory": You need to replace this placeholder with the actual path to the directory where your PDF files are located.
 - *os.listdir(pdf_directory):* This gets a list of all files and directories within the specified directory.
 - *[os.path.join(pdf_directory, f) for f in all_files if f.lower().endswith(".pdf")]:* This uses a list comprehension to:
   - Iterate through each item (f) in the all_files list.
   - Check if the lowercase version of the filename ends with ".pdf".
   - If it does, it constructs the full path to the file using os.path.join() and adds it to the pdf_files list.
 - *process_pdf(pdf_path) function:* This function encapsulates the steps of extracting, cleaning, and organizing the text for a single PDF file. This makes the main loop cleaner.
 - *for pdf_file_path in pdf_files::* This loop iterates through the pdf_files list, and for each PDF file path, it calls the process_pdf() function.
 - *Error Handling:* I've added basic try-except blocks within the extraction functions to handle potential errors that might occur when processing certain PDF files. This prevents the entire script from crashing if one file has issues.

#### How to Use:
 - Replace "/path/to/your/pdf/directory" with the correct path to your PDF folder.
 - Make sure you have the necessary libraries installed (PyPDF2, pdfminer.six, nltk).
 - Run the Python script.
 
This script will now iterate through all the PDF files in the specified directory, process each one, and print the first 10 sentences of the cleaned text for each PDF. You can then adapt the process_pdf() function to do whatever further analysis or storage you need with the processed data.


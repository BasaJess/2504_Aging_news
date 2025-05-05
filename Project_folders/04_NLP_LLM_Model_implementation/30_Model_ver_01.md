### *To develop a machine learning model that classifies research papers related to healthspan and longevity:*
---
1. *Data Collection and Preparation:*

 - Extract Text from PDFs:

 - Install Required Libraries:

```
pip install PyPDF2
```

 - Extract Text:

 
 - Extract Metadata: Metadata such as title, authors, and publication date are embedded in the PDFs, Extract them using the PdfReader's metadata attribute.
 ```
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
 - Sort and select recent documents
 ```
 # Filter out PDFs without a date
 dated_pdfs = [pdf for pdf in pdf_info_list if pdf['date'] is not None]

 # Sort PDFs by date (newest first)
 sorted_pdfs = sorted(dated_pdfs, key=lambda x: x['date'], reverse=True)

 # Select the 5 or 10 most recent PDFs
 recent_pdfs = sorted_pdfs[:10]  # Change to [:5] for the 5 most recent

 ```

 - Prepare Training Data:

   - Keyword-Based Labeling: Utilize your list of 69 healthspan-related keywords to label documents. If a document contains one or more of these keywords, label it as relevant; otherwise, label it as not relevant.

   ```
   # Define your list of healthspan-related keywords
   healthspan_keywords = ['longevity', 'aging', 'senescence', 'lifespan', 'caloric restriction', 'telomere', 'autophagy', 'gerontology', 'anti-aging', 'resveratrol', 'sirtuins', 'mTOR', 'NAD+', 'oxidative stress', 'inflammation', 'mitochondria', 'genomics', 'epigenetics', 'stem cells', 'regeneration', 'DNA repair', 'protein folding', 'calorie restriction', 'intermittent fasting', 'blue zones', 'hormesis', 'geroprotector', 'rapamycin', 'metformin', 'foxo3', 'klotho', 'amyloids', 'proteostasis', 'ubiquitin', 'chaperones', 'senolytics', 'p53', 'nf-kb', 'igf-1', 'ghrelin', 'leptin', 'adiponectin', 'melatonin', 'circadian rhythm', 'sleep', 'exercise', 'diet', 'nutrition', 'microbiome', 'gut health', 'probiotics', 'prebiotics', 'polyphenols', 'flavonoids', 'omega-3', 'antioxidants', 'vitamin D', 'hormone replacement', 'testosterone', 'estrogen', 'DHEA', 'thyroid', 'cortisol', 'stress management', 'mindfulness', 'meditation', 'cognitive function', 'neuroplasticity', 'brain health']

   def label_document(text, keywords, threshold=3):
    """Assign a label based on the presence of at least 3 healthspan-related keywords."""
    text_lower = text.lower()
    count = sum(1 for keyword in keywords if keyword in text_lower)
      return 1 if count >= threshold else 0

   # Apply labeling to each document
   for pdf in pdf_info_list:
    pdf['label'] = label_document(pdf['text'], healthspan_keywords)
   ```

   - Incorporate Additional Texts: Include the 10 podcast transcripts and the book "Lifespan" by David Sinclair in your training data. Label them as relevant to reinforce the model's understanding of the topic.



---
2. Text Preprocessing:

 - Clean the Text:
Remove special characters, numbers, and extra whitespace.

 - Convert text to lowercase.

 - Remove stopwords to reduce noise.

 - Tokenization:
Split the text into sentences and words.

 - For BERT models, use the corresponding tokenizer to prepare inputs.

```
 import string
 from nltk.corpus import stopwords
 from nltk.tokenize import word_tokenize
 import nltk

 nltk.download('punkt')
 nltk.download('stopwords')

 def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    words = word_tokenize(text)
    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

 # Apply preprocessing to each document

 for pdf in pdf_info_list:
    pdf['processed_text'] = preprocess_text(pdf['text'])

```
---
3. Model Selection and Training:

 - Choose a Pre-trained BERT Model:

 - Utilize a BERT model pre-trained on biomedical texts, such as BioBERT, to leverage domain-specific language representations.

 - Fine-Tune the Model:

 - Data Splitting: Divide your labeled dataset into training and validation sets (e.g., 80% training, 20% validation).

 - Training: Fine-tune the BERT model on your dataset. Monitor performance on the validation set to prevent overfitting.

 ```
 pip install transformers

 ```

 ```
 from transformers import BertTokenizer, BertForSequenceClassification
 from transformers import Trainer, TrainingArguments
 from torch.utils.data import Dataset
 import torch

 # Define a custom dataset
 class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

 # Prepare data
 texts = [pdf['processed_text'] for pdf in recent_pdfs]
 labels = [1 if any(keyword in pdf['processed_text'] for keyword in 
  healthspan_keywords) else 0 for pdf in recent_pdfs]

 # Initialize tokenizer
 tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

 # Create dataset
 dataset = CustomDataset(texts, labels, tokenizer, max_len=512)

 # Define training arguments
 training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
 )

 # Initialize model
 model = BertForSequenceClassification.from_pretrained('bert-base-uncased', 
num_labels=2)

 # Initialize trainer
 trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
 )

 # Train model
 trainer.train()

 ```
or

 ```
 from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
 from torch.utils.data import Dataset
 import torch

 class HealthspanDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(
            text,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long),
        }

 # Prepare data
 texts = [pdf['processed_text'] for pdf in pdf_info_list]
 labels = [pdf['label'] for pdf in pdf_info_list]

 # Initialize BioBERT tokenizer
 tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")

 # Create dataset
 dataset = HealthspanDataset(texts, labels, tokenizer, max_len=512)

 # Define training arguments
 training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
 )

 # Initialize BioBERT model
 model = AutoModelForSequenceClassification.from_pretrained("dmis-lab/biobert-base-cased-v1.1", num_labels=2)

 # Initialize trainer
 trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
 )

 # Train model
 trainer.train()

 ```


---
4. Preventing Overfitting:

 - Regularization Techniques:

 - Dropout Layers: Introduce dropout layers in your model to randomly deactivate neurons during training, which helps prevent overfitting.

 - Early Stopping: Monitor the validation loss during training and stop when it starts to increase, indicating potential overfitting.

 - Data Augmentation:

 - Synonym Replacement: Replace words with their synonyms to create variations of the text.

 - Back Translation: Translate the text to another language and back to introduce diversity.

 - Cross-Validation:

 - Use k-fold cross-validation to ensure the model generalizes well to unseen data.

 ```
 from transformers import AdamW

 # Define optimizer with weight decay
 optimizer = AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)

 # Training loop with early stopping
 from transformers import get_scheduler

 num_training_steps = len(dataset) * training_args.num_train_epochs
 lr_scheduler = get_scheduler(
    name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
 )

 for epoch in range(training_args.num_train_epochs):
    model.train()
    for batch in dataset:
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
    # Implement early stopping based on validation loss

 ```


---
5. Model Evaluation:

 - Metrics:
Assess the model using precision, recall, F1-score, and accuracy to ensure balanced performance.

 - Interpretability:

 - Analyze misclassified documents to understand and address the model's limitations.

 ```
 from sklearn.metrics import classification_report

 def evaluate_model(model, dataset):
    model.eval()
    predictions, true_labels = [], []
    for batch in dataset:
        outputs = model(**batch)
        logits = outputs.logits
        predictions

 ```
---
6. Identifying Recent Relevant Papers:

 - Extract Publication Dates:
If metadata includes publication dates, use them to sort documents.

If not, consider using external databases or repositories to retrieve publication dates based on document titles or DOIs.

 - Filter and Sort:

   - Apply the trained model to classify all documents.

   - Select the 5 or 10 most recent documents classified as relevant.

 - Retrieve Metadata:
For the selected documents, extract or retrieve metadata such as title, authors, and source.

```
 from datetime import datetime

 # Filter relevant documents
relevant_pdfs = [pdf for pdf in pdf_info_list if pdf['label'] == 1 and pdf['date'] is not None]

 # Sort relevant documents by date (newest first)
sorted_relevant_pdfs = sorted(relevant_pdfs, key=lambda x: x['date'], reverse=True)

 # Select the 5 or 10 most recent relevant documents
recent_relevant_pdfs = sorted_relevant_pdfs[:10]  # Change to [:5] for the 5 most recent

 # Retrieve texts and metadata
for pdf in recent_relevant_pdfs:
    title = pdf.get('title', 'Unknown Title')
    author = pdf.get('author', 'Unknown Author')
    date = pdf.get('date', 'Unknown Date')
    text_sample = pdf.get('text', '')[:500]  # Displaying the first 500 characters as a sample
    print(f"Title: {title}\nAuthor: {author}\nDate: {date}\nText Sample: {text_sample}\n{'-'*80}")
 
```

---
7. Automation and Scaling:

 - Pipeline Development:

 - Create a pipeline to automate text extraction, preprocessing, classification, and metadata retrieval.

 - Continuous Learning:

As new documents become available, periodically retrain the model to maintain its performance.

---
By following these steps, you'll develop a robust machine learning model capable of classifying research papers related to healthspan and longevity while mitigating overfitting risks.



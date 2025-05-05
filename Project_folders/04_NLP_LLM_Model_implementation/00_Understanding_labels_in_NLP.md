In our script the following line us used:
```
labels = [0] * len(tokenized_sentences)  # Dummy labels (Update with real labels if available)
```
This means all sentences are currently assigned a default label of 0 (which is incorrect for real classification tasks). Let's break it down.

#### What are "Real labels?"
A label is the category or class assigned to each text sample.
For example, if you are classifying scientific papers on youth longevity, your labels could be:

|Text Sample|Label (Category)|
|---|---|
|"Caloric restriction extends lifespan in mice."	|1 (Biological Studies)|
|"Exercise improves cellular aging in humans."	|2 (Lifestyle Interventions)|
|"AI models predict longevity based on DNA data."	|3 (Computational Biology)|

Examples of Real lables for this project:
1. Binary Classification (2 Classes: relevant vs. Irrelevant)
 - 0 -> Not related to youth extension.
 - 1 -> related to youth extension
```
labels = [1, 0, 1, 0, 1]  # Assign based on relevance
```
2. Multi-class Classification (Different Topics)
 - 0 -> general Aging Reserach
 - 1 -> Diet and longevity
 - 2 -> Genetics and longevity
 - 3 -> AI in longevity
 ```
 labels = [0, 1, 2, 3, 1, 0, 2]
```
3. Sentiment Classification (Positive/Negative Impact on longevity)
 - 0 -> Negative effect on lifespan
 - 1 -> neutral effect
 - 2 -> Positive effect on lifespan
 ```
 labels = [2, 0, 1, 2, 1, 0, 2]
```
---
#### Auto-labeling a dataset using NLP
- *Approach 1: Zero-shot classification (best for New Data)*
Instead of manually labeling hundreds of PDFs, we can use a pre-trained model to classify the text without fine-tuning.
  - We will use: `facebook/bart-large-mnli`
  - It can classify text into custome categories without training!
  - Steps:
    - Define our categories (e.g., "Genetics", "Diet", "AI & Longevity").
    - Use a pre-trained model to assign a probability to each category
    - Assign the lable with the highest probability
    ```
    from transformers import pipeline

    # Load zero-shot classification pipeline
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    # Define categories (You can modify these)
    categories = ["Genetics & Longevity", "Diet & Longevity", "Exercise & Aging", 
                "AI in Longevity Research", "General Aging Research"]

    # Example text (Replace this with your real text samples)
    text_samples = [
        "Caloric restriction extends lifespan in mice.",
        "Machine learning models predict aging-related diseases.",
        "Daily exercise improves mitochondrial function and aging."
    ]

    # Auto-label each text sample
    for text in text_samples:
        result = classifier(text, categories)
        label = result["labels"][0]  # Most likely category
        print(f"Text: {text}\nPredicted Label: {label}\n")
    ```
- *Approach 2: Semantic Similarity (If You Have Some Labeled Data)*
If we already have some labeled examples, we can use sentence-transformers (BERT-based embeddings) to compare new documents to labeled ones.The model will assign labels based on similarity to previously labeled samples.

The number of text samples needed depends on the task and method you're using:

🔹 For Zero-Shot Classification (No Training Needed)
✅ You can process thousands of samples with no prior labeled data since the model works out-of-the-box.
✅ Works well with 10-20 well-defined categories and any number of documents.
💡 Minimum Recommended: ~100-200 samples for initial evaluation.

🔹 For Fine-Tuning a Pretrained Model
If you want to train a model with labeled data, you'll need:
📌 Small Dataset (Good for Prototyping): 500 - 1,000 samples
📌 Moderate Dataset: 5,000 - 10,000 samples
📌 Large Dataset (More Accuracy, More Time Required): 50,000+

💡 Minimum Recommended: ~1,000 labeled samples for reasonable fine-tuning.

🔹 For Semantic Similarity Matching
If you're using sentence embeddings (like BERT or Sentence Transformers), you need:
✅ At least 50-100 labeled examples per category for meaningful similarity comparisons.
✅ The more categories you have, the more labeled samples you need.
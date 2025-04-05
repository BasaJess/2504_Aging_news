Metrics for Evaluation.

####Specific considerations for BioBert.
---
 - BioASQ Metrics...
 - Micro vs Macro Averaging ...
 - Domain-Specific Performance...
 - *Few-shot/Zer-shot Learning:*
If you are evaluating BioBERTs performance in scenarios where you have limited training data, consider metrics hat reflect the model's ability to generalize to new classes or instances.
 - *Entity Recognition/Relation Extraction:*
If BioBERT is used for tasks like NER or RE, metrics like precision, recall and F1-Score can be used to evaluate the model's ability to identif and extract relevant entities and relationships

---
####Relevance Metrics:
---

 - *Mean Reciprocal Rank (MRR):* The average of the reciprocal of the rank of the first relevant document retrieved.
 - *Precision@k:* The proportion of relevant documents within the top k retrieved documents.
 - *Recall@k:*The proportion of relevant documents retrieved within he top k documents

---
####Classification Metrics:
---

 - Accuracy, precision, recall, F-1Score AUC-ROC, Confussion Matrix
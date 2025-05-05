1. Use `BERT` embeddings and cluster them (K-Means, DBSCAN, or Agglomerative Clustering).
 - Convert the processed text into BERT Embeddings.
2. Evaluate clusters using cosine similarity and Euclidean distance.
3. Unsupervised topic modeling (e.g., LDA or BERTopic) to get a rough classification.
 - Appy K-Means clustering or Hierarchical clustering to group similar papers.
 
---

 ##### Implementation Plan:
 1. Load the preprocessed text from processed_papers.json.
 2. Use a BERT model (e.g., sentence-transformers) to generate embeddings.
 3. Apply cosine similarity & Euclidean distance to analyze similarity.
 4. Cluster documents using K-Means.
 5. Visualize the clusters (optional but useful).

 [Implementation](/notebooks/baseline_model.ipynb)
### Evaluation Metrics
---
Since our databse is unlabeled, we have few options for evaluating our BERT base model

#### 1. Unsupersived Evaluation (Baseline Model)
 - ***Topic Coherence (UMass, UCI, or NPMI):*** If we use topic modeling as a preprocessing step (e.g., clustering papers based on embeddings), coherence measures how meaningful the topics are.
 - ***Clustering metrics (Silhouette Score, Davies-Bouldin Index, Dunn Index):*** These mesure the separation and cohesion of the clusters.
   - *Silhouette Score:*
     - Measures how well each sample is clustered.
     - Ranges from -1 (bad) to 1 (good).
     - Higher values mean better separation between clusters.
   - *Davies-Bouldin Index:* 
     - Measures cluster compactness and separation.
     - Lower values indicate better clustering.
   - *Inertia (Elbow method):*
     - Measures within-cluster variance.
     - Helps determine the optimal number of clusters.  
 - ***Embedding Similarity (Cosime Similarity, Euclidian Distance):*** Measures how close soimilar papers are in the embedding space.
 - ***Qualitative Validation: Manual inspection:*** 
   - *Check Clustered Papers*(from file. e.g. clustered_papers.json)
     - Open and review grouped papers.
     - Are similar topics grouped together?
   - *Check Cluster Visualization*
     - Look at the PCA plot.
     - If clusters are well-separated, it's a good sign. 


 #### 2. Supervised Evaluation (After Fine-Tuning)
 - ***Classification Metrics (Accuracy, Precision, recall, F-1 score, AUC-ROC):*** These metrics measure classification performance.
 - ***Perplexity (for Language Models):*** Measures how well the model predicts unseen text from our fine-tuned model.

 #### 3. Information Extraction Evaluation
 - ***Named Entity recognition (NER) metrics (Precision, recall, F1-score):*** We can use NER techniques and compare against a small labeled set.
 - ***Exact Match (EM) Score:*** If extracting  structured biliographic information, EM measures how well the model retrieves exact references.
 ---
 #### Implementation:

 - Baseline:

 ```
 from sklearn.metrics import silhouette_score, davies_bouldin_score
 from sklearn.cluster import KMeans
 import numpy as np

 # Assume we have embeddings for each paper
 embeddings = np.random.rand(1000,768) # Example BERT embeddings

 # KMeans clustering
 kmeans = KMeans(n_clusters=10, random_state=42).fit(embeddings)
 labels = kmeans.labels_

 # Compute clustering metrics
 silhouette = slohouette_score(embeddings, labels)
 davies_bouldin = davies_bouldin_score(embeddings, lables)

 print(f"Silhouette Score: {silhoulette})"
 print(f"davies-Bouldin index: {davies_bouldin})
```
 - Classification Metrics (After Fine-Tuning)

 ```
 from sklearn.metrics import accuracy_score, precision_recall_fscore_support

 # Example ground truth and predictions
 y_true = [0,1,1,0,1,0,1,1,0,0] # replace with actual labels
 y_pred = [0,1,0,0,1,0,1,1,1,0] # replace with model predictions

 acuracy = accuracy_score(y_true, y_pred)
 precision, recall, fi, _ = precision_recall_fscore_support(y_true, y_pred, average="binary")

 print(f"accuracy: {accuracy}, Precision: {precission}, Recall: {recall, F1-score: {f1}})
 ```
 - Named Entity Recognition (NER) Evaluation

 ```
 from seqeval.metrics import classification-report

 # Example NER tags
 y_true = [["0", "0", "B-SOURCE", "I-SOURCE", "0"],["B-SOURCE, "I-SOURCE", "0", "0"]] 
 y_pred = [["0", "0", "B-SOURCE", "I-SOURCE", "0"],["0", "I-SOURCE", "0", "0"]] 

 print(classification_report(y_true,y_pred))
 ```
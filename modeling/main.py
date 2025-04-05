#Pseudo Code:

import requests

import json

import pdfminer.high\_level

import re

import spacy

from transformers import pipeline

import yake

def fetch\_pubmed(query, max\_results=10):

    base\_url \= "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params \= {

        "db": "pubmed",

        "term": query,

        "retmode": "json",

        "retmax": max\_results

    }

    response \= requests.get(base\_url, params=params)

    ids \= response.json().get("esearchresult", {}).get("idlist", \[\])

    

    articles \= \[\]

    for pubmed\_id in ids:

        fetch\_url \= f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

        fetch\_params \= {"db": "pubmed", "id": pubmed\_id, "retmode": "json"}

        details \= requests.get(fetch\_url, params=fetch\_params).json()

        summary \= details.get("result", {}).get(pubmed\_id, {})

        articles.append({"id": pubmed\_id, "title": summary.get("title", "N/A"), "source": "PubMed"})

    

    return articles

def fetch\_arxiv(query, max\_results=10):

    base\_url \= "http://export.arxiv.org/api/query"

    params \= {

        "search\_query": query,

        "start": 0,

        "max\_results": max\_results

    }

    response \= requests.get(base\_url, params=params)

    entries \= response.text.split("\<entry\>")\[1:\]

    

    articles \= \[\]

    for entry in entries:

        title \= entry.split("\<title\>")\[1\].split("\</title\>")\[0\].strip()

        articles.append({"title": title, "source": "arXiv"})

    

    return articles

def fetch\_semantic\_scholar(query, max\_results=10):

    base\_url \= "https://api.semanticscholar.org/graph/v1/paper/search"

    params \= {

        "query": query,

        "limit": max\_results,

        "fields": "title,url"

    }

    response \= requests.get(base\_url, params=params)

    data \= response.json()

    

    articles \= \[{"title": item\["title"\], "source": "Semantic Scholar", "url": item.get("url", "") } for item in data.get("data", \[\])\]

    return articles

def retrieve\_articles(query, max\_results=10):

    pubmed\_articles \= fetch\_pubmed(query, max\_results)

    arxiv\_articles \= fetch\_arxiv(query, max\_results)

    semantic\_scholar\_articles \= fetch\_semantic\_scholar(query, max\_results)

    

    return pubmed\_articles \+ arxiv\_articles \+ semantic\_scholar\_articles

def extract\_text\_from\_pdf(pdf\_path):

    return pdfminer.high\_level.extract\_text(pdf\_path)

def clean\_text(text):

    text \= re.sub(r'\\s+', ' ', text)  \# Remove excessive spaces

    text \= re.sub(r'\[^a-zA-Z0-9., \]', '', text)  \# Keep only alphanumeric and punctuation

    return text.strip()

def extract\_keywords(text, top\_n=5):

    kw\_extractor \= yake.KeywordExtractor()

    keywords \= kw\_extractor.extract\_keywords(text)

    return \[kw\[0\] for kw in keywords\[:top\_n\]\]

def named\_entity\_recognition(text):

    nlp \= spacy.load("en\_core\_web\_sm")

    doc \= nlp(text)

    return \[(ent.text, ent.label\_) for ent in doc.ents\]

def summarize\_text(text):

    summarizer \= pipeline("summarization")

    summary \= summarizer(text, max\_length=100, min\_length=30, do\_sample=False)

    return summary\[0\]\['summary\_text'\]

if \_\_name\_\_ \== "\_\_main\_\_":

    query \= "human youth longevity"

    articles \= retrieve\_articles(query, max\_results=5)

    print(json.dumps(articles, indent=2))

    

    sample\_text \= "Youth longevity research explores stem cell therapy, caloric restriction, and telomere extension. Studies suggest that interventions targeting aging mechanisms can extend health span."

    print("Keywords:", extract\_keywords(sample\_text))

    print("Entities:", named\_entity\_recognition(sample\_text))

    print("Summary:", summarize\_text(sample\_text))

